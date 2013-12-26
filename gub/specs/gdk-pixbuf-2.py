from gub import gnome
from gub import target

class Gdk_pixbuf_2 (target.AutoBuild):
#    source = 'http://ftp.gnome.org/pub/GNOME/platform/2.32/2.32.1/sources/gdk-pixbuf-2.22.1.tar.gz'
#    patches = ['gdk-pixbuf-mmx.patch']
    source = 'http://ftp.gnome.org/pub/GNOME/sources/gdk-pixbuf/2.24/gdk-pixbuf-2.24.0.tar.bz2'
    dependencies = ['tools::libtool', 'tools::glib', 'libtiff-devel', 'libpng', 'libjpeg-devel']
    patches = ['gdk-pixbuf-mmx.patch', 'gdk-pixbuf-2.24-gio-sniff.patch']

    configure_flags = (target.AutoBuild.configure_flags
			   + ' --disable-glibtest'
			   + ' --enable-introspection=no'
			   + ' --disable-introspection'
			   + ' --enable-gdiplus'
			   + ' --disable-modules'
			   + ' --disable-dependency-tracking'
				)
class Gdk_pixbuf_2__mingw(target.AutoBuild):
    source = 'http://ftp.gnome.org/pub/GNOME/platform/2.32/2.32.1/sources/gdk-pixbuf-2.22.1.tar.gz'
#    source = 'http://ftp.gnome.org/pub/GNOME/sources/gdk-pixbuf/2.24/gdk-pixbuf-2.24.0.tar.bz2'
    dependencies = ['tools::libtool', 'tools::glib', 'libtiff-devel', 'libpng', 'libjpeg-devel']
    patches = ['gdk-pixbuf-mmx.patch']

    configure_flags = (target.AutoBuild.configure_flags
			   + ' --disable-glibtest'
			   + ' --enable-introspection=no'
			   + ' --disable-introspection'
			   + ' --disable-gdiplus'
			   + ' --disable-modules'
			   #+ ' --without-libtiff'
			   #+ ' --without-libjpeg'
			   + ' --disable-dependency-tracking'
				)

