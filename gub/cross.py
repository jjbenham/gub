import md5
import os
import re
#
from gub.syntax import printf
from gub import build
from gub import context
from gub import logging
from gub import misc
from gub import repository
from gub import target
from gub import tools

class AutoBuild (build.AutoBuild):
    """Package for cross compilers/linkers etc.
    """
    configure_flags = (build.AutoBuild.configure_flags
                       + misc.join_lines ('''
--program-prefix=%(target_architecture)s-
--prefix=%(cross_prefix)s
--target=%(target_architecture)s
--with-sysroot=%(system_root)s
--disable-multilib
--disable-silent-rules
'''))
#--with-slibdir=%(prefix_dir)s/slib
    install_flags = ''' DESTDIR=%(install_root)s prefix=%(prefix_dir)s%(cross_dir)s install'''
    subpackage_names = ['doc', '']
    def get_substitution_dict (self, env={}):
        dict = {
            'C_INCLUDE_PATH': '%(tools_prefix)s/include'
            + misc.append_path (os.environ.get ('C_INCLUDE_PATH', '')),
            'CPLUS_INCLUDE_PATH': '%(tools_prefix)s/include'
            + misc.append_path (os.environ.get ('CPLUS_INCLUDE_PATH', '')),
            'LIBRARY_PATH': '%(tools_prefix)s/lib'
            + misc.append_path (os.environ.get ('LIBRARY_PATH', '')),
            'PATH': '%(cross_prefix)s/bin:%(tools_archmatch_prefix)s/bin:%(tools_prefix)s/bin:%(tools_cross_prefix)s/bin:' + os.environ['PATH'],
        }
        dict.update (env)
        d = build.AutoBuild.get_substitution_dict (self, dict).copy ()
        return d
    @context.subst_method
    def rpath (self):
        return r'-Wl,-rpath -Wl,%(tools_prefix)s/lib'
    def install_license (self):
        self.runner.harmless ('not installing license file for cross package: %(name)s' % self.get_substitution_dict ())
# ugh, mis-used in specs/gcc.py for CROSS/gcc.py to be ROOT/usr/lib
#    def install_prefix (self):
#        return '%(install_root)s%(prefix_dir)s%(cross_dir)s'

def change_target_package (package):
    tools.package_auto_dependency_dict (package)

# GUB compatibility problems:
# python: 2.4, import *dbm
# git: wget http://github.com/janneke/gub/tarball/master
# librestrict
# GNU make
# GNU tar --strip-component
# /usr/bin/install: coreutils
# SVN
bootstrap_names = [
    'system::gcc',
    'tools::librestrict',
#    'tools::binutils',
#    'tools::gcc',
    'tools::make',
    'tools::libtool',
    'tools::file',
    'tools::zlib',
    ]

if 'stat' in misc.librestrict ():
    bootstrap_names += [
        'tools::bash',
        'tools::coreutils',
        'tools::diff',
        'tools::findutils',
        'tools::gawk',
        'tools::grep',
#        'tools::gub-utils',
        'tools::sed',
        ]

def set_cross_dependencies (package_object_dict):
    packs = list (package_object_dict.values ())

    cross_packs = [p for p in packs if isinstance (p, AutoBuild)]
    sdk_packs = [p for p in packs if isinstance (p, build.SdkBuild)]
    tools_packs = [p for p in packs if isinstance (p, tools.AutoBuild)]
    other_packs = [p for p in packs if (not isinstance (p, AutoBuild)
                                        and not isinstance (p, build.SdkBuild)
                                        and not isinstance (p, build.BinaryBuild)
                                        and not isinstance (p, tools.AutoBuild)
                                        and not p.platform_name () in bootstrap_names)]

    pack_names = [p.platform_name () for p in packs]
    extra_cross_names = []
    sets = dict ()
    for p in packs:
        sets[p.settings.platform] = p.settings
    for p in list (sets.keys ()):
        extra_cross_names += [n for n in get_build_dependencies (sets[p]) if n not in pack_names]

    # Run something like lilypond/SConscript's configure
    # to figure-out if we need a new, Git, Make, Patch, Python, etc?
    # Building make & patch is cheap and dependable.
    bazaar_packs = [p for p in packs if isinstance (p.source, repository.Bazaar)]
    cvs_packs = [p for p in packs if isinstance (p.source, repository.CVS)]
    git_packs = [p for p in packs if isinstance (p.source, repository.Git)]
    patch_packs = [p for p in packs if p.patches]
    perl_packs = [p for p in packs if (isinstance (p, tools.CpanBuild)
                                         or isinstance (p, target.CpanBuild))]
    python_packs = [p for p in packs if (isinstance (p, tools.PythonBuild)
                                         or isinstance (p, target.PythonBuild))]
    scons_packs = [p for p in packs if (isinstance (p, tools.SConsBuild)
                                        or isinstance (p, target.SConsBuild))]
    
    subversion_packs = [p for p in packs if isinstance (p.source, repository.Subversion)]
    #tar_packs = [p for p in packs if (isinstance (p.source, repository.TarBall)
    #                                  and p.platform_name () not in
    #                                  (bootstrap_names + ['tools::tar']))]
    #bzip2_packs = [p for p in tar_packs if p.source.source.endswith ('bz2')]

    sdk_names = [s.platform_name () for s in sdk_packs]
    cross_names = [s.platform_name () for s in cross_packs]
    # No implicit dependencies on other platform's cross_names or sdk_names
    # try:
    # bin/gub -p tools linux-x86::cross/gcc mingw::cross/gcc
    # bin/gub -p tools linux-x86::cross/gcc
    def update_packs (packs=[], add=[]):
        for p in packs:
            if not misc.list_in (add, p.get_platform_build_dependencies ()):
                old_callback = p.get_build_dependencies
                p.get_build_dependencies = misc.MethodOverrider (old_callback,
                                                                 lambda x,y: x+y, (add,))

# OOPS
#    update_packs (other_packs,
#                  [n for n in cross_names if p.settings.platform in n])
#    update_packs (other_packs + cross_packs,
#                  [n for n in sdk_names if p.settings.platform in n])    
#    update_packs (other_packs + cross_packs + tools_packs, bootstrap_names)
    for p in other_packs:
        add = [n for n in cross_names if p.settings.platform in n]
        if not misc.list_in (add, p.get_platform_build_dependencies ()):
            old_callback = p.get_build_dependencies
            p.get_build_dependencies = misc.MethodOverrider (old_callback,
                                                             lambda x,y: x+y, (add,))
    for p in other_packs + cross_packs:
        add = [n for n in sdk_names if p.settings.platform in n]
        if not misc.list_in (add, p.get_platform_build_dependencies ()):
            old_callback = p.get_build_dependencies
            p.get_build_dependencies = misc.MethodOverrider (old_callback,
                                                             lambda x,y: x+y, (add,))
    for p in other_packs + cross_packs + tools_packs:
        add = bootstrap_names
        if (p.platform_name () not in bootstrap_names
            and not misc.list_in (add, p.get_platform_build_dependencies ())):
            old_callback = p.get_build_dependencies
            p.get_build_dependencies = misc.MethodOverrider (old_callback,
                                                             lambda x,y: x+y, (add,))

    extra_names = []
    rsync_packs = bazaar_packs or cvs_packs or subversion_packs
    for packs, names in (
        #(bzip2_packs, ['tools::bzip2']),
        (git_packs, ['tools::git']),
        #(patch_packs, ['tools::patch']),
        (perl_packs, ['tools::perl']),
        (rsync_packs, ['tools::rsync']),
        (scons_packs, ['tools::scons']),
        (subversion_packs, ['tools::subversion']),
        #(tar_packs, ['tools::tar']),
        ):
        if packs:
            extra_names += names
            update_packs (packs, names)

    if python_packs or scons_packs:
        extra_names += ['tools::python']
        update_packs (python_packs, ['tools::python'])

    return extra_cross_names + extra_names

cross_module_checksums = {}
cross_module_cache = {}
def get_cross_module (settings):
    platform = settings.platform
    if platform in cross_module_cache:
        return cross_module_cache[platform]

    base = re.sub ('[-0-9].*', '', platform)
    gubdir = settings.gubdir
    for name in platform, base:
        file_name = '%(gubdir)s/gub/%(name)s.py' % locals ()
        if os.path.exists (file_name):
            break

    logging.info ('module name: ' + name + '\n')
    module = misc.load_module (file_name, base)

    cross_module_checksums[platform] = md5.md5 (open (file_name).read ()).hexdigest ()
    cross_module_cache[platform] = module
    return module

def get_build_dependencies (settings):
    mod = get_cross_module (settings)
    return bootstrap_names + [misc.with_platform (n, settings.platform) for n in mod.get_cross_build_dependencies (settings)]

def setup_linux_x86 (logger, name, x86_cross):
    '''Hack for using 32 bit compiler on linux-64.

    Use linux-x86 cross compiler to compile non-64-bit-clean packages such
    as nsis and odcctools.  A plain 32 bit compiler could also be used,
    but we do not have such a beast.  Make sure to have 32-bit
    compatibility installed:
        apt-get install ia32-libs
    '''

    x86_bindir = x86_cross + '/bin'
    x86_cross_bin = x86_cross + '/i686-linux' + '/bin'

    compiler = x86_bindir + '/i686-linux-gcc'
    if not os.path.exists (compiler):
        printf ('error: cannot find 32 bit compiler: %(compiler)s\n' % locals ())
        raise Exception ('Package %(name)s depends on target/linux-x86.' % locals ())
    if os.system ('''echo 'int main () { return 0; }' > 32bit.c && %(compiler)s -o 32bit 32bit.c && ./32bit''' % locals ()):
        printf ('error: cannot run 32 bit executable: 32bit\n')
        raise Exception ('Package %(name)s depends on 32 bit libraries''' % locals ())
    os.system ('rm -f 32bit 32bit.c')

    def check_link (src, dest):
        dest = x86_cross_bin + '/' + dest
        if not os.path.exists (dest):
            # duh, must chdir for relative link
            #src = '../../bin/i686-linux-' + src
            src = x86_bindir + '/i686-linux-' + src
            os.link (src, dest)

    check_link ('cpp', 'cpp')
    check_link ('gcc', 'cc')
    check_link ('g++', 'c++')
    check_link ('gcc', 'gcc')
    check_link ('g++', 'g++')


def change_target_package_x86 (package, env={'PATH': os.environ['PATH']}):

    x86_dir = package.settings.alltargetdir + '/linux-x86'
    x86_cross = (x86_dir
                 + package.settings.root_dir
                 + package.settings.prefix_dir
                 + package.settings.cross_dir)
    x86_bindir = x86_cross + '/bin'
    x86_cross_bin = x86_cross + '/i686-linux' + '/bin'
    env['CC'] = x86_cross_bin + '/gcc'
    env['CXX'] = x86_cross_bin + '/g++'
    # FIXME: should only remove any %(tools_prefix)s elements from these...
    env['C_INCLUDE_PATH'] = ''
    env['CPLUS_INCLUDE_PATH'] = ''
    env['LIBRARY_PATH'] = ''
    env['LIBRESTRICT_ALLOW'] = package.settings.targetdir
    env['PATH'] = x86_cross_bin + ':' + env['PATH']

    def build_environment (e):
        return env
    
    def patch (foo):
        package.func (setup_linux_x86, package.__class__.__name__, x86_cross)

    # FIXME: we could also add [, build_environment ()] by default
    # to build.py's compile [and install?] functions
    def configure (foo):
        package.system ('mkdir -p %(builddir)s')
        package.system ('cd %(builddir)s && %(configure_command)s', env)
        
    def compile (foo):
        package.system ('cd %(builddir)s && %(compile_command)s', env)
            
    package.build_environment \
        = misc.MethodOverrider (package.nop, build_environment)
    package.patch \
        = misc.MethodOverrider (package.patch, patch)
    package.configure \
            = misc.MethodOverrider (package.nop, configure)
    package.compile \
        = misc.MethodOverrider (package.nop, compile)
