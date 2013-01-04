import os
#
from gub import cross
from gub import misc
from gub import tools

class Nsis (tools.SConsBuild):
    source = 'http://surfnet.dl.sourceforge.net/sourceforge/nsis/nsis-2.46-src.tar.bz2'
    #source = ':pserver:anonymous@nsis.cvs.sourceforge.net:/cvsroot/nsis&module=NSIS&tag=HEAD'
    dependencies = ['mingw::cross/gcc']
    scons_flags = misc.join_lines ('''
DEBUG=no
NSIS_CONFIG_LOG=yes
SKIPUTILS="NSIS Menu"
''')
    def __init__ (self, settings, source):
        tools.AutoBuild.__init__ (self, settings, source)
        if 'x86_64-linux' in self.settings.build_architecture:
            self.dependencies += ['linux-x86::glibc']
            cross.change_target_package_x86 (self, self.add_mingw_env ())
        if 'stat' in misc.librestrict ():
            self.compile_command = ('LIBRESTRICT_IGNORE=%(tools_prefix)s/bin/python '
                                    + tools.SConsBuild.compile_command)
    def add_mingw_env (self):
        # Do not use 'root', 'usr', 'cross', rather use from settings,
        # that enables changing system root, prefix, etc.
        mingw_dir = (self.settings.alltargetdir + '/mingw'
                     + self.settings.root_dir)
        mingw_bin = (mingw_dir
                     + self.settings.prefix_dir
                     + self.settings.cross_dir
                     + '/bin')
        tools_dir = (self.settings.alltargetdir + '/tools'
                     + self.settings.root_dir)
        tools_bin = (tools_dir
                     + self.settings.prefix_dir
                     + '/bin')
        return {'PATH': mingw_bin + ':' + tools_bin + ':' + os.environ['PATH'] }
    def patch (self):
        self.system ('mkdir -p %(allbuilddir)s', ignore_errors=True)
        self.system ('ln -s %(srcdir)s %(builddir)s')
        if 'x86_64-linux' in self.settings.build_architecture:
            self.file_sub ([('''^Export\('defenv'\)''', '''
import os
defenv['CC'] = os.environ['CC']
defenv['CXX'] = os.environ['CXX']
defenv['C_INCLUDE_PATH'] = ''
defenv['CPLUS_INCLUDE_PATH'] = ''
defenv['CFLAGS'] = ''
# SCons will add double quotes when LINKFLAGS contains whitespace,
# so start and end with double quotes as so to disarm them
#defenv['LINKFLAGS'] = '"%(rpath)s -Wl,-rpath -Wl,%(alltargetdir)s/%(build_platform)s%(root_dir)s%(prefix_dir)s/lib"'
# Nsis is built 32 bit -- this won't work for non-GNU/Linux build hosts
defenv['LINKFLAGS'] = '"%(rpath)s -Wl,-rpath -Wl,%(alltargetdir)s/linux-x86%(root_dir)s%(prefix_dir)s/lib"'

Export('defenv')
''')],
                       '%(srcdir)s/SConstruct')
    # this method is overwritten for x86-64_linux
    def build_environment (self):
        return self.add_mingw_env ()
    def compile (self):
        self.system ('cd %(builddir)s && %(compile_command)s',
                     self.build_environment ())
    def install (self):
        self.system ('cd %(builddir)s && %(install_command)s ',
                     self.build_environment ())
        self.system ('cp -p %(nsisdir)s/FontName.dll %(install_prefix)s/share/nsis/Plugins')
