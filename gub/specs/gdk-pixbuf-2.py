from gub import gnome
from gub import target

class Gdk_pixbuf_2 (target.AutoBuild):
    source = 'http://ftp.gnome.org/pub/GNOME/sources/gdk-pixbuf/2.24/gdk-pixbuf-2.24.0.tar.bz2'
    dependencies = ['tools::libtool', 'tools::glib', 'libtiff-devel', 'libpng-devel', 'libjpeg-devel']
    patches = ['gdk-pixbuf-2.24-gio-sniff.patch']
    configure_flags = (target.AutoBuild.configure_flags
			   + ' --disable-glibtest'
			   + ' --enable-introspection=no'
			   + ' --disable-introspection'
			   #+ ' --without-libpng'
			   + ' --enable-gdiplus'
			   + ' --disable-modules'
			   + ' --disable-dependency-tracking'
				)
			#   + ' --help')


