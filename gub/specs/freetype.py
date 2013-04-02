from gub import build
from gub import misc
from gub import target
from gub import tools

class Freetype (target.AutoBuild):
    '''Software font engine
FreeType is a software font engine that is designed to be small,
efficient, highly customizable and portable while capable of producing
high-quality output (glyph images). It can be used in graphics
libraries, display servers, font conversion tools, text image generation
tools, and many other products as well.'''
    #2.4.9-1.1
    source = 'http://download.savannah.gnu.org/releases/freetype/freetype-2.4.9.tar.bz2'
    #source = 'http://download.savannah.nongnu.org/releases/freetype/freetype-2.3.11.tar.gz&name=freetype'
    def __init__ (self, settings, source):
        target.AutoBuild.__init__ (self, settings, source)
        # Freetype stats /sbin, /usr/sbin and /hurd to determine if
        # build system is unix??
        # build.append_dict (self, {'LIBRESTRICT_ALLOW': '/sbin:/usr/sbin:/hurd'})
        if 'stat' in misc.librestrict ():
            build.add_dict (self, {'LIBRESTRICT_ALLOW': '/sbin:/usr/sbin:/hurd:${LIBRESTRICT_ALLOW-/foo}'})
    license_files = ['%(srcdir)s/docs/LICENSE.TXT']
    dependencies = ['libtool-devel', 'zlib-devel', 'tools::autoconf']
    subpackage_names = ['devel', '']
    def configure (self):
#                self.autoupdate (autodir=os.path.join (self.srcdir (),
#                                                       'builds/unix'))
        self.system ('''
        rm -f %(srcdir)s/builds/unix/{unix-def.mk,unix-cc.mk,ftconfig.h,freetype-config,freetype2.pc,config.status,config.log}
''')
        target.AutoBuild.configure (self)
        self.file_sub ([('^LIBTOOL=.*', 'LIBTOOL=%(builddir)s/libtool --tag=CXX')], '%(builddir)s/Makefile')
    def munge_ft_config (self, file):
        self.file_sub ([('\nprefix=[^\n]+\n',
                         '\nlocal_prefix=yes\nprefix=%(system_prefix)s\n'),
                        ('\nhardcode_libdir_flag_spec=.*', '\nhardcode_libdir_flag_spec=')],
                       file, must_succeed=True)

    def install (self):
        target.AutoBuild.install (self)
        # FIXME: this is broken.  for a sane target development package,
        # we want /usr/bin/freetype-config must survive.
        # While cross building, we create an  <toolprefix>-freetype-config
        # and prefer that.
        self.system ('mkdir -p %(install_prefix)s%(cross_dir)s/bin/')
        self.system ('mv %(install_prefix)s/bin/freetype-config %(install_prefix)s%(cross_dir)s/bin/freetype-config')
        self.munge_ft_config ('%(install_prefix)s%(cross_dir)s/bin/freetype-config')

class Freetype__mingw (Freetype):
    def xxconfigure (self):
        Freetype.configure (self)
        self.dump ('''
# libtool will not build dll if -no-undefined flag is not present
LDFLAGS:=$(LDFLAGS) -no-undefined
''',
             '%(builddir)s/Makefile',
             mode='a')

class Freetype__tools (tools.AutoBuild, Freetype):
    dependencies = ['libtool', 'zlib']
    # FIXME, mi-urg?
    license_files = Freetype.license_files
    def install (self):
        tools.AutoBuild.install (self)
        #self.munge_ft_config ('%(install_root)s/%(tools_prefix)s/bin/.freetype-config')
        self.munge_ft_config ('%(install_root)s/%(tools_prefix)s/bin/freetype-config')
