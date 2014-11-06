from gub import context
from gub import gnome
from gub import target

class Gtk2_x_ (target.AutoBuild):
    #source = 'http://ftp.gnome.org/pub/gnome/sources/gtk+/2.24/gtk+-2.24.24.tar.xz'
    source = 'http://ftp.gnome.org/pub/GNOME/platform/2.32/2.32.1/sources/gtk+-2.22.1.tar.gz'
    patches = [
        #'gtk+-2.15.3-substitute-env.patch',
        #'gtk+-2.21.0-substitute-env.patch',
        ]
    dependencies = ['libtool',
                'atk-devel',
		'gdk-pixbuf-2',
                'cairo-devel',
                'libjpeg-devel',
                'libpng-devel',
                'libtiff-devel',
                #'pango-devel',
                'pangocairo-devel',
                'libxext-devel',
                #, 'libxinerama-devel',
                'libxfixes-devel',
                ]
    configure_flags = (target.AutoBuild.configure_flags
                + ' --without-libjasper'
                + ' --disable-cups')
    def patch (self):
        target.AutoBuild.patch (self)
        self.file_sub ([
                (' demos ', ' '), # actually, we'd need tools::gtk+
                (' tests ', ' '),
                ], '%(srcdir)s/Makefile.in')
    configure_command = ('gdk-pixbuf-query-loaders --update-cache && export gio_can_sniff=yes; '
                + target.AutoBuild.configure_command)
    def create_config_files (self, prefix='/usr'):
        gtk_module_version = '2.10.0' #FIXME!
        etc = self.expand ('%(install_root)s/%(prefix)s/etc/gtk-2.0', locals ())
        self.dump ('''
setdir GTK_PREFIX=$INSTALLER_PREFIX
set GTK_MODULE_VERSION=%(gtk_module_version)s
set GTK_SO_EXTENSION=%(so_extension)s
''', '%(install_prefix)s/etc/relocate/gtk+.reloc', env=locals ())
        self.copy ('%(sourcefiledir)s/gdk-pixbuf.loaders', etc)
    def install (self):
        target.AutoBuild.install (self)
        self.create_config_files ()

class Gtk2_x___freebsd (Gtk2_x_):
    configure_variables = (Gtk2_x_.configure_variables
                + ' CFLAGS=-pthread')

class Gtk2_x___freebsd__x86 (Gtk2_x___freebsd):
    patches = Gtk2_x___freebsd.patches + ['gtk+-2.15.3-configure.in-have-iswalnum.patch']

class Gtk2_x_without_X11 (Gtk2_x_):
    dependencies = [x for x in Gtk2_x_.dependencies
                if 'libx' not in x]

class Gtk2_x___mingw (Gtk2_x_without_X11):
    def patch (self):
        Gtk2_x_.patch (self)
class Gtk2__mingw (Gtk2_x___mingw):
    pass


class Gtk2__darwin (Gtk2_x_without_X11):
    configure_flags = (Gtk2_x_without_X11.configure_flags
                + ' --with-gdktarget=quartz'
                )

