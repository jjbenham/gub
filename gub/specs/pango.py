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
    (r'^1\.28', '1.6.0')
    ]

class Pango (target.AutoBuild):
    #source = 'http://ftp.acc.umu.se/pub/GNOME/sources/pango/1.29/pango-1.29.5.tar.xz'
    #source = 'http://ftp.gnome.org/pub/GNOME/sources/pango/1.34/pango-1.34.1.tar.xz'
    source = 'http://ftp.acc.umu.se/pub/GNOME/sources/pango/1.30/pango-1.30.1.tar.xz'
    patches = ['pango-1.20-substitute-env.patch']
    dependencies = [
            'tools::glib', 
            'freetype-devel',
            'fontconfig-devel',
            'glib-devel',
            'libtool',
	    'libxml2-devel',
	    'cairo-devel'
            ]
    configure_flags = (target.AutoBuild.configure_flags
                + misc.join_lines ('''
--without-x
'''))
    def module_version (self):
        result = None
        version = self.version()
        for regex, candidate in pango_module_version_regexes:
            if re.match(regex, version):
                result = candidate
                break
        #assert result
        return "1.6.0" #result
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

class Pango__darwin (Pango):
    configure_flags = (target.AutoBuild.configure_flags
                + misc.join_lines ('''
--with-cairo
--enable-static
--with-included-modules=yes
--with-dynamic-modules=no
'''))

class Pango__linux (Pango):
  pass

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
