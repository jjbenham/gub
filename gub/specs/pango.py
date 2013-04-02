import re
#
from gub import gnome
from gub import misc
from gub import loggedos
from gub import target

pango_module_version_regexes = [
    (r'^1\.14', '1.5.0'),
    (r'^1\.20', '1.6.0'),
    (r'^1\.22', '1.6.0'),
    (r'^1\.24', '1.6.0'),
    (r'^1\.26', '1.6.0'),
    (r'^1\.27', '1.6.0'),
    (r'^1\.30', '1.6.0'),
    (r'^1\.32', '1.8.0')
    ]

class Pango (target.AutoBuild):
    source = 'http://ftp.gnome.org/pub/gnome/sources/pango/1.34/pango-1.34.0.tar.xz'
    #patches = ['pango-1.20-substitute-env.patch', 'pango-1.32.configure-with-cairo.patch']
    patches = ['pango-1.34.no_win_32.patch']
    dependencies = [
            'tools::glib', 
            'freetype-devel',
            'fontconfig-devel',
            'glib-devel',
            'libtool',
	    'cairo'
            ]
    def get_conflict_dict (self):
        return {'': ['pangocairo', 'pangocairo-devel', 'pangocairo-doc'], 'devel': ['pangocairo', 'pangocairo-devel', 'pangocairo-doc'], 'doc': ['pangocairo', 'pangocairo-devel', 'pangocairo-doc'], 'runtime': ['pangocairo', 'pangocairo-devel', 'pangocairo-doc']}
    def module_version (self):
        result = None
        version = self.version()
        for regex, candidate in pango_module_version_regexes:
            if re.match(regex, version):
                result = candidate
                break
        #assert result #FIXME
        #return result
	return "1.8.0"
    def install (self):
        target.AutoBuild.install (self)
        self.create_config_files ()
        self.fix_config_files ()
    def create_config_files (self, prefix='/usr'):
        pango_module_version = self.module_version ()
        etc = self.expand ('%(install_root)s/%(prefix)s/etc/pango', locals ())
        self.dump ('''[Pango]
ModuleFiles = $PANGO_PREFIX/etc/pango/pango.modules
ModulesPath = $PANGO_PREFIX/lib/pango/%(pango_module_version)s/modules
''' % locals (), etc + '/pangorc')
        self.dump ('''
setfile PANGO_RC_FILE=$INSTALLER_PREFIX/etc/pango/pangorc
setdir PANGO_PREFIX=$INSTALLER_PREFIX/
set PANGO_MODULE_VERSION=%(pango_module_version)s
''', '%(install_prefix)s/etc/relocate/pango.reloc', env=locals ())
        self.copy ('%(sourcefiledir)s/pango.modules', etc)
    def fix_config_files (self, prefix='/usr'):
        etc = self.expand ('%(install_root)s/%(prefix)s/etc/pango', locals ())
        self.system ('mkdir -p %(etc)s' , locals ())
        def fix_prefix (logger, file_name):
            loggedos.file_sub (logger, [('/' + prefix + '/', '$PANGO_PREFIX/')],
                               file_name)
        self.map_locate (fix_prefix, etc, '*')


class Pango__linux (Pango):
    def untar (self):
        Pango.untar (self)
        # FIXME: --without-cairo switch is removed in 1.10.1,
        # pango only compiles without cairo if cairo is not
        # installed linkably on the build system.  UGH.
        self.file_sub ([('(have_cairo[_a-z0-9]*)=false', '\\1=true'),
                        ('(cairo[_a-z0-9]*)=false', '\\1=true'),
			('(pango_os_win32[_a-z0-9]*)=yes', '\\1=no'),
			('(pango_platform_win32[_a-z0-9]*)=yes', '\\1=no'),
			('(have_freetype[_a-z0-9]*)=true', '\\1=false')],
                        '%(srcdir)s/configure')

class Pango__freebsd (Pango__linux):
    dependencies = Pango__linux.dependencies + ['libiconv-devel']

class Pango__darwin (Pango):
    def configure (self):
        Pango.configure (self)
        self.file_sub ([('nmedit', '%(target_architecture)s-nmedit')],
                       '%(builddir)s/libtool')
    def install (self):
        Pango.install (self)                
        # FIXME: PANGO needs .so, NOT .dylib?
        self.dump ('''
set PANGO_SO_EXTENSION=.so
''', '%(install_prefix)s/etc/relocate/pango.reloc', env=locals (), mode='a')

class Pango__mingw (Pango):
        # FIXME: need -lpthread now?
        # /home/janneke/vc/gub/target/mingw/root/usr/cross/bin/i686-mingw32-ld: cannot find -lpthread
    dependencies = (Pango.dependencies
                + ['pthreads-w32-devel'])
    def create_config_files (self, prefix='/usr'):
        Pango.create_config_files (self, prefix)
        etc = self.expand ('%(install_root)s/%(prefix)s/etc/pango', locals ())
        self.dump ('''
${PANGO_PREFIX}/lib/pango/${PANGO_MODULE_VERSIOn}/modules/pango-basic-win32${PANGO_SO_EXTENSION} BasicScriptEngineWin32 PangoEngineShape PangoRenderWin32 common:
''', '%(etc)s/pango.modules', env=locals (), mode='a')
        Pango.fix_config_files (self, prefix)
