from gub import target

class Libxrender (target.AutoBuild):
    source = 'http://xorg.freedesktop.org/releases/individual/lib/libXrender-0.9.8.tar.bz2'
    dependencies = ['tools::libtool', 'libx11-devel', 'libxdmcp-devel', 'renderproto-devel']
    configure_flags = (target.AutoBuild.configure_flags
                       + ' --disable-malloc0returnsnull')
