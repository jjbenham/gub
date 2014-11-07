from gub import target
from gub import tools 

class Libpng (target.AutoBuild):
    source = 'http://surfnet.dl.sourceforge.net/sourceforge/libpng/libpng-1.2.8-config.tar.gz'
    patches = ['libpng-pngconf.h-setjmp.patch']
    dependencies = ['zlib-devel','tools::libtool']
    def name (self):
        return 'libpng'
    def patch (self):
        target.AutoBuild.patch (self)
        self.file_sub ([('(@INSTALL.*)@PKGCONFIGDIR@',
                r'\1${DESTDIR}@PKGCONFIGDIR@')],
               '%(srcdir)s/Makefile.in')
        self.file_sub ([('(@INSTALL.*)@PKGCONFIGDIR@',
                r'\1${DESTDIR}@PKGCONFIGDIR@')],
               '%(srcdir)s/Makefile.am')
    configure_command = ('LIBRESTRICT_ALLOW=/var/mail '
                         + target.AutoBuild.configure_command)
    ## need to call twice, first one triggers spurious Automake stuff.
    compile_command = '(%s) || (%s)' % (target.AutoBuild.compile_command,
                                        target.AutoBuild.compile_command)
    
class Libpng__tools (tools.AutoBuild, Libpng):
    dependencies = ['tools::libtool', 'tools::autoconf', 'tools::automake']
    def patch (self):
        Libpng.patch (self)
