from gub import context
from gub import gnome
from gub import target

class Gtk_x_ (target.AutoBuild):
    source = 'http://ftp.gnome.org/pub/gnome/sources/gtk+/3.1/gtk+-3.1.2.tar.bz2'
    patches = ['gtk+-3-no-perf.patch']
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
                + ' --disable-cups'
		+ ' --disable-man'
		+ ' --disable-print-backend'
		+ ' --disable-modules'
		+ ' --disable-gtk3-dependency'
		+ ' --disable-glibtest'
		+ ' --disable-gtk-doc'
		+ ' --enable-explicit-deps'
		+ ' --with-included-immodules')
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
        self.system ('cd %(install_prefix)s/lib/ && ln -s libgtk-3.a libgtk-3.dll.a')

class Gtk_x___freebsd (Gtk_x_):
    configure_variables = (Gtk_x_.configure_variables
                + ' CFLAGS=-pthread')

class Gtk_x___freebsd__x86 (Gtk_x___freebsd):
    patches = Gtk_x___freebsd.patches + ['gtk+-2.15.3-configure.in-have-iswalnum.patch']

class Gtk_x_without_X11 (Gtk_x_):
    dependencies = [x for x in Gtk_x_.dependencies
                if 'libx' not in x]

class Gtk_x___mingw (Gtk_x_without_X11):
    source = 'http://ftp.gnome.org/pub/gnome/sources/gtk+/3.0/gtk+-3.0.12.tar.bz2'
#    sources = "http://ftp.acc.umu.se/pub/gnome/sources/gtk+/3.1/gtk+-3.1.4.tar.bz2" 
    def patch (self):
        Gtk_x_.patch (self)
    configure_flags = (Gtk_x_without_X11.configure_flags
		+ ' --enable-win32-backend'
		+ ' --without-x')

class Gtk_x___darwin (Gtk_x_without_X11):
    sources = "http://ftp.acc.umu.se/pub/gnome/sources/gtk+/3.1/gtk+-3.1.4.tar.bz2"
    configure_flags = (Gtk_x_without_X11.configure_flags
                + ' --with-gdktarget=quartz'
		+ ' --enable-quartz-backend'
		+ ' --without-x')

class Gtk_x___darwin__ppc (Gtk_x___darwin):
#    source = 'http://ftp.gnome.org/pub/GNOME/platform/2.28/2.28.2/sources/gtk+-2.18.5.tar.gz'
    patches = Gtk_x___darwin.patches + [
        'gtk+-2.16-darwin-ppc.patch',
        ]
