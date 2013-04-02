from gub import target

class Xproto (target.AutoBuild):
    source = 'http://xorg.freedesktop.org/archive/individual/proto/xproto-7.0.23.tar.bz2'
    dependencies = ['tools::libtool']
