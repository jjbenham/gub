from gub import target

#Currently, Aubio depends on libsndfile, libsamplerate and FFTW. On
#Linux platforms, Aubio can be built using JACK, and ALSA.
class Aubio (target.WafBuild):
    #source = 'git://git.aubio.org/git/aubio'
    #branch = 'develop'
    #patches = ['libaubio-no-tests.patch']
    dependencies = ['tools::automake', 'tools::pkg-config',
                'libfftw-devel',
                'libsamplerate-devel',
                'libsndfile-devel',
                'python-devel',
                ]
    configure_command = (target.WafBuild.configure_command
                           + ' --notests'
                          + ' --prefix=%(install_prefix)s/'
                               )


    configure_flags = (target.WafBuild.configure_flags
                           + ' --notests')
    
 
class Aubio__mingw (Aubio):
    source = 'http://aubio.org/pub/aubio-0.4.0.tar.bz2'
    patches = ['libaubio-srandom-define.patch', 'libaubio-no-tests.patch']
 
    #configure_command = (target.WafBuild.configure_command
    def install (self):
	target.WafBuild.install (self)
	self.system ('''
install -m755 %(builddir)s/build/src/aubio-4.dll %(install_prefix)s/bin/
''')
 
class Aubio__linux (Aubio):
    #patches = ['libAubio-no-duplicate-definition.patch']

    def install (self):
        Aubio.install (self)
        self.system ('''
install -m755 %(builddir)s/build/src/Aubio-4.dll %(install_prefix)s/bin/
#install -m755 %(builddir)s/src/ %(install_prefix)s/bin/
''')
class Aubio__linux (Aubio):
   #patches = ['libAubio-no-duplicate-definition.patch']
   #source = 'git://git.aubio.org/git/aubio'
   #branch = 'develop'
   source = 'http://aubio.org/pub/aubio-0.4.1.tar.bz2'
#   patches = Aubio.patches + ['libAubio-wscript.patch']
#   configure_command = (' CFLAGS="-I%(system_prefix)s/include/" '
#                        + '%(builddir)s/waf distclean configure'
#

class Aubio__darwin__x86 (target.AutoBuild):
    source = 'http://aubio.org/pub/aubio-0.3.2.tar.gz'
    patches = ['libaubio-pkg-config-override.patch']
    dependencies = ['tools::automake', 'tools::pkg-config',
                'libfftw-devel',
                'libsamplerate-devel',
                'libsndfile-devel',
                'python-devel',
                ]
    force_autoupdate = True
    config_cache_overrides = (target.AutoBuild.config_cache_overrides + '''
ac_cv_path_PYTHON=${ac_cv_path_PYTHON=no}
ac_cv_path_SWIG=${ac_cv_path_SWIG=no}
''')

'''
class Aubio__darwin (Aubio):
   
   source = 'http://www.denemo.org/downloads/gub/aubio-0.4.2~alpha.tar.bz2'


   #source = 'http://www.denemo.org/downloads/gub/aubio-develop-20120330.tar.gz'
   #source = 'git://git.aubio.org/git/aubio'
   #branch = 'develop'

   patches = Aubio.patches + ['libaubio-0.4.2.no-test.patch']
   configure_flags = (Aubio.configure_flags
                           + ' --notests'
			   + ' --with-target-platform=darwin')

'''
