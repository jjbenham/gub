from gub import context
from gub import gnome
from gub import target

class Gtk_x_ (target.AutoBuild):
    source = 'http://ftp.gnome.org/pub/gnome/sources/gtk+/3.4/gtk+-3.4.2.tar.xz'
    #source = 'http://ftp.gnome.org/pub/GNOME/platform/2.31/2.31.2/sources/gtk+-2.21.0.tar.gz'
    patches = ['gtk+-3.4.2.no-xinput.patch']
#        #'gtk+-2.15.3-substitute-env.patch',
#        'gtk+-2.21.0-substitute-env.patch',
#        ]
    dependencies = ['libtool',
                'atk-devel',
                'cairo-devel',
                'libjpeg-devel',
                'libpng-devel',
                'libtiff-devel',
                'pango-devel',
                #'pangocairo-devel',
                'libxext-devel',
                #, 'libxinerama-devel',
                'libxfixes-devel',
		'gdk-pixbuf-2'
                ]
    configure_flags = (target.AutoBuild.configure_flags
                + ' --without-libjasper'
                + ' --disable-cups'
		+ ' --disable-xinput'
		+ ' --disable-xinerama'
		)
    def patch (self):
        target.AutoBuild.patch (self)
        self.file_sub ([
                (' demos ', ' '), # actually, we'd need tools::gtk+
                (' tests ', ' '),
                ], '%(srcdir)s/Makefile.in')
        self.file_sub ([('(have_xinput[_a-z0-9]*)=yes', '\\1=no'),
                        ('(have_xinput2[_a-z0-9]*)=no', '\\1=yes')],
			'%(srcdir)s/configure')


    configure_command = (' export gio_can_sniff=yes; '
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

class Gtk_x___linux__x86 (Gtk_x_):
    configure_variables = (Gtk_x_.configure_variables
                + ' CFLAGS="-L%(builddir)s/gdk/.libs -L%(builddir)s/gtk/.libs " ')
    configure_flags = (Gtk_x_.configure_flags
		+ ' --with-included-loaders=ani,icns,pcx,ras,tga,png,pnm,wbmp,xbm,xpm'
		+ ' --enable-debug=yes'
		+ ' --disable-xinput'
                )

class Gtk_x___freebsd (Gtk_x_):
    configure_variables = (Gtk_x_.configure_variables
                + ' CFLAGS=-pthread')

class Gtk_x___freebsd__x86 (Gtk_x___freebsd):
    patches = Gtk_x___freebsd.patches + ['gtk+-2.15.3-configure.in-have-iswalnum.patch']

class Gtk_x_without_X11 (Gtk_x_):
    dependencies = [x for x in Gtk_x_.dependencies
                if 'libx' not in x]

class Gtk_x___mingw (Gtk_x_without_X11):
    def patch (self):
        Gtk_x_.patch (self)

class Gtk_x___darwin (Gtk_x_without_X11):
    configure_flags = (Gtk_x_without_X11.configure_flags
                + ' --with-gdktarget=quartz'
		+ ' --with-included-loaders=ani,icns,pcx,ras,tga,png,pnm,wbmp,xbm,xpm'
		+ ' --enable-debug=yes'		
                )

class Gtk_x___darwin__ppc (Gtk_x___darwin):
#    source = 'http://ftp.gnome.org/pub/GNOME/platform/2.28/2.28.2/sources/gtk+-2.18.5.tar.gz'
    patches = Gtk_x___darwin.patches + [
        'gtk+-2.16-darwin-ppc.patch',
        ]
