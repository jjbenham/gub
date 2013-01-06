from gub import target

class Alsa (target.AutoBuild):
    source = 'http://mirrors.zerg.biz/alsa/lib/alsa-lib-1.0.25.tar.bz2'
    dependencies = ['libtool', 'tools::automake', 'tools::pkg-config',]
