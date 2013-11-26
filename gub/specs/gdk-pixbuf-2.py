from gub import gnome
from gub import target

class Gdk_pixbuf_2 (target.AutoBuild):
    source = 'http://ftp.gnome.org/pub/GNOME/platform/2.32/2.32.1/sources/gdk-pixbuf-2.22.1.tar.gz'
    dependencies = ['tools::libtool', 'glib-devel', 'libtiff-devel', 'libpng-devel', 'libjpeg-devel']
    patches = ['gdk-pixbuf-mmx.patch']

