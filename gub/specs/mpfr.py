from gub import tools

class Mpfr__tools (tools.AutoBuild):
    source = 'http://www.mpfr.org/mpfr-2.4.2/mpfr-2.4.2.tar.gz'
    dependencies = ['libtool', 'gmp']
