from gub import target

class Libxext (target.AutoBuild):
    source = 'http://xorg.freedesktop.org/releases/individual/lib/libXext-1.0.99.4.tar.gz'
    dependencies = ['libtool', 'libx11-devel']
    configure_flags = (target.AutoBuild.configure_flags
                       + ' --disable-malloc0returnsnull')
