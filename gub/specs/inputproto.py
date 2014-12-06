from gub import target

class Inputproto (target.AutoBuild):
    source = 'http://www.x.org/releases/X11R7.7/src/everything/inputproto-2.2.tar.bz2'
    dependencies = ['tools::libtool']
