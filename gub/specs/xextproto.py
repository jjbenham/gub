from gub import target

class Xextproto (target.AutoBuild):
    source = 'http://www.x.org/releases/X11R7.7/src/everything/xextproto-7.2.1.tar.bz2'
    dependencies = ['tools::libtool']
