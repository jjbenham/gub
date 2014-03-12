from gub import target

#Currently, aubio depends on libsndfile, libsamplerate and FFTW. On
#Linux platforms, aubio can be built using JACK, and ALSA.

class Libaubio (target.WafBuild):
    source = 'http://aubio.org/pub/aubio-0.4.0.tar.bz2'
    patches = ['libaubio-srandom-define.patch']
    dependencies = ['tools::automake', 'tools::pkg-config',
                'libfftw-devel',
                'libsamplerate-devel',
                'libsndfile-devel',
                'python-devel',
                ]
    configure_flags = (target.WafBuild.configure_flags
                           + ' --notests')
    def install (self):
        target.WafBuild.install (self)
        self.system ('''
install -m755 %(builddir)s/build/src/aubio-4.dll %(install_prefix)s/bin/
#install -m755 %(builddir)s/src/ %(install_prefix)s/bin/
''')

#--notests
#    force_autoupdate = True
#    config_cache_overrides = (target.AutoBuild.config_cache_overrides + '''
#ac_cv_path_PYTHON=${ac_cv_path_PYTHON=no}
#ac_cv_path_SWIG=${ac_cv_path_SWIG=no}
#''')
