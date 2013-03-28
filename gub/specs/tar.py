#
from gub import repository
from gub import tools

class Tar__tools (tools.AutoBuild):
    source = 'http://ftp.gnu.org/gnu/tar/tar-1.26.tar.bz2'
    configure_variables = (tools.AutoBuild.configure_variables
                           + ' CFLAGS=" -std=gnu89" ')

#    patches = ['tar-1.22-AT_FDCWD.patch']
#    def __init__ (self, settings, source):
#        tools.AutoBuild.__init__ (self, settings, source)
#        if isinstance (self.source, repository.TarBall):
#            self.source._unpack = self.source._unpack_promise_well_behaved
#    configure_variables = (tools.AutoBuild.configure_variables
 #                         + ' CFLAGS=" -I%(system_prefix)s/include/linux " ')
