from gub import tools

class Mpfr__tools (tools.AutoBuild):
    source = 'http://www.mpfr.org/mpfr-2.3.2/mpfr-2.3.2.tar.bz2'
    dependencies = ['libtool', 'gmp']
