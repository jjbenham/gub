from gub import gnome
from gub import target

class Gdk_pixbuf_2 (target.AutoBuild):
    source = 'http://ftp.gnome.org/pub/GNOME/platform/2.32/2.32.1/sources/gdk-pixbuf-2.22.1.tar.gz'
    dependencies = ['tools::libtool', 'tools::glib', 'libtiff-devel', 'libpng-devel', 'libjpeg-devel']
    #patches = ['gdk-pixbuf-mmx.patch']
    configure_flags = (target.AutoBuild.configure_flags
			   + ' --disable-glibtest'
			   + ' --enable-introspection=no'
			   + ' --disable-introspection'
			   + ' --without-libpng'
			   + ' --enable-gdiplus'
			   + ' --disable-modules'
			   + ' --disable-dependency-tracking'
				)
			#   + ' --help')


