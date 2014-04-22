'''
TODO:
  * figure out solution pango/pangocairo, lilypond/lilypondcairo mess
  * add jack for windows?
  * relocation: non-windows dynamic relocation in main.c
  * relocation: fix locale dir
'''

from gub import misc
from gub import repository
from gub import target

class Denemo (target.AutoBuild):
    #source = 'git://git.savannah.gnu.org/denemo.git'
    #branch = 'master'
    #patches = ['denemo-audio.patch']
    source = 'http://www.denemo.org/downloads/denemo-1.1.4.tar.gz'
    patches = ['denemo-audio.patch', 'denemo-1.1.4-run-lilypond.patch', 'denemo-lilypond-path.patch']

    dependencies = [
        'lilypondcairo',
	'gtk+-devel',
	'librsvg', 
	'evince',
        'aubio-devel',
        'libgtksourceview',
 	'guile-devel',
        'portaudio-devel',
 	'libsndfile',
	'fluidsynth',
	'portmidi',
	'librubberband'
        ]
    def __init__ (self, settings, source):
        target.AutoBuild.__init__ (self, settings, source)
        if isinstance (source, repository.Git):
            source.version = misc.bind_method (repository.Repository.version_from_configure_ac, source)
    def compile (self):
        if isinstance (self.source, repository.Git):
            # FIXME: missing dependency
            # self.system ('cd %(builddir)s/src && make lylexer.c')
            target.AutoBuild.compile (self)

class Denemo__linux__x86 (Denemo):
    #dependencies = (Denemo.dependencies + ['alsa-devel'])
    #patches = Denemo.patches + ['denemo-run-lilypond.patch']

    configure_flags = (Denemo.configure_flags
                   		+ ' --enable-binreloc'
				+ ' --disable-portmidi')
    configure_variables = (Denemo.configure_variables
			   + ' CFLAGS="-D_HAVE_PORTMIDI_ -D_GUB_BUILD_ -I%(system_prefix)s/include/evince/3.0 " '			   
			   + ' LDFLAGS="-L%(system_prefix)s/lib" ')
    make_flags = Denemo.make_flags + ' LDFLAGS+="-lportmidi -lporttime"'

class Denemo__mingw (Denemo):
    dependencies = (Denemo.dependencies + ['lilypad'])
    configure_flags = (Denemo.configure_flags
		       	   + ' --disable-binreloc'
			   + ' --enable-portmidi'
			   + ' --disable-alsa'
			   + ' --enable-rubberband')
    configure_variables = (Denemo.configure_variables
			   + ' CFLAGS="-D_HAVE_PORTMIDI_ -D_GUB_BUILD_ -I%(system_prefix)s/include/evince/3.0 " '
			   + ' LDFLAGS="-L%(system_prefix)s/lib" ')
    make_flags = Denemo.make_flags + ' LDFLAGS+="-lportmidi -lporttime"'
    def __init__ (self, settings, source):
        Denemo.__init__ (self, settings, source)
        # Configure (link) without -mwindows for denemo-console.exe
        self.target_gcc_flags = '-mms-bitfields'
    def compile (self):
        Denemo.compile (self)
        self.system ('''
cd %(builddir)s && make
cd %(builddir)s/src && mv .libs/denemo.exe denemo-console.exe && rm -f denemo.exe
cd %(builddir)s/src && make AM_LDFLAGS="-mwindows" && cp -p .libs/denemo.exe denemo-windows.exe
''')
    def install (self):
        Denemo.install (self)
        self.system ('''
install -m755 %(builddir)s/src/denemo-windows.exe %(install_prefix)s/bin/denemo.exe
install -m755 %(builddir)s/src/denemo-console.exe %(install_prefix)s/bin/denemo-console.exe
''')

class Denemo__darwin (Denemo):
    dependencies = (Denemo.dependencies + [
        'fondu',
        'osx-lilypad',
        ])
    #patches = Denemo.patches + ['denemo-run-lilypond.patch']
    configure_flags = (Denemo.configure_flags
		       	   + ' --disable-binreloc'
			   + ' --enable-portmidi'
			   + ' --enable-portaudio'
			   + ' --disable-x11'
			   + ' --enable-rubberband'
			   + ' --disable-jack')

    configure_variables = (Denemo.configure_variables
                           + ' CFLAGS="-g -O0 -D_HAVE_PORTMIDI_ -D_MACH_O_ -D_GUB_BUILD_ -I%(system_prefix)s/include/evince/3.0 " '
                           + ' LDFLAGS="-L%(system_prefix)s/lib -Wl,-framework,CoreMIDI -lgcc_eh -lgcc -lc -lfftw3" ')
	 
    make_flags = Denemo.make_flags + ' LDFLAGS+="-lportmidi -lporttime"'

class Denemo__darwin__ppc (Denemo__darwin):
    # make sure that PREFIX/include/unistd.h gets included
    def patch (self):
        Denemo__darwin.patch (self)
        self.system ('''
mkdir -p %(builddir)s/src
cp -pv %(system_prefix)s/include/unistd.h %(builddir)s/src
''')
