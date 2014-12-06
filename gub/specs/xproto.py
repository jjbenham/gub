from gub import target

class Xproto (target.AutoBuild):
    source = 'http://www.x.org/releases/X11R7.7/src/everything/xproto-7.0.23.tar.bz2'
    dependencies = ['tools::libtool']
