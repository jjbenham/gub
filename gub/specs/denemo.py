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
#    source = 'git://git.savannah.gnu.org/denemo.git'
#    branch = 'master'
    patches = ['denemo-audio.patch']
#    subpackage_names = ['']
    dependencies = [
        'cross/gcc-c++-runtime',
        'tools::automake',
        'tools::gettext',
        'tools::libtool',
        'tools::pkg-config',
 	'glib-devel',
	'tools::glib',
       	'cairo',
        'lilypondcairo',
	'gtk+-devel',
	'librsvg', 
	'evince',
        'libaubio-devel',
        'libgtksourceview',
 	'guile-devel',
        'portaudio-devel',
 	'libsndfile',
	'fluidsynth',
	'portmidi',
	'librubberband'
        ]
    configure_flags = (target.AutoBuild.configure_flags
                       + ' --enable-fluidsynth'
                       )
#    configure_variables = (target.AutoBuild.configure_variables
# 			   + ' CFLAGS="-O0 -g -I%(system_prefix)s/include/evince/2.30 " '
#			   + ' LDFLAGS="-L%(system_prefix)s/lib -levview -levdocument" ')

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
    #source = 'http://www.denemo.org/downloads/denemo-1.0.0~rc10.tar.gz'
    #source = 'git://git.savannah.gnu.org/denemo.git'
    #branch = 'master'
    patches = ['denemo.prefop.c.patch', 'denemo.main.c-envelope.patch']
    #branch = 'linux'
    #dependencies = + ['alsa-devel']

    configure_flags = (Denemo.configure_flags
                   		+ ' --enable-binreloc'
				+ ' --enable-portmidi'
			        + ' --enable-alsa')
    configure_variables = (target.AutoBuild.configure_variables
			+ ' CFLAGS="-I%(system_prefix)s/include/evince/2.30 " '
			+ ' LDFLAGS="-L%(system_prefix)s/lib -levview -levdocument" ')



class Denemo__mingw__windows (Denemo):
 source = 'http://www.denemo.org/downloads/denemo-1.1.4.tar.gz'
 #source = 'http://git.savannah.gnu.org/cgit/denemo.git/snapshot/denemo-master.tar.gz'
 #source = 'git://git.savannah.gnu.org/denemo.git'
 #branch = 'master'
 dependencies = [x for x in Denemo.dependencies
                    if x.replace ('-devel', '') not in [
            'lash',
            ]] + ['lilypad']

class Denemo__mingw__console (Denemo__mingw__windows):
    #patches = ['portmidi-denemo-test.patch']
    configure_flags = (Denemo__mingw__windows.configure_flags
		       	   + ' --disable-binreloc'
			   + ' --enable-portmidi'
			   + ' --enable-rubberband')

    configure_variables = (Denemo.configure_variables
			+ ' CFLAGS="-I%(system_prefix)s/include/evince/2.32 -I%(system_prefix)s/../vamp-sdk/" '
			+ ' LDFLAGS="-L%(system_prefix)s/lib -levview -levdocument -L%(system_prefix)s/../vamp-plugin-sdk-2.5-binaries-win32-mingw -lvamp-sdk" ')

    def __init__ (self, settings, source):
        Denemo__mingw__windows.__init__ (self, settings, source)
        # Configure (link) without -mwindows for denemo-console.exe
        self.target_gcc_flags = '-mms-bitfields'
    def compile (self):
        Denemo__mingw__windows.compile (self)
        self.system ('''
cd %(builddir)s && make
cd %(builddir)s/src && mv .libs/denemo.exe denemo-console.exe && rm -f denemo.exe
cd %(builddir)s/src && make AM_LDFLAGS="-mwindows" && cp -p .libs/denemo.exe denemo-windows.exe
''')
    def install (self):
        Denemo__mingw__windows.install (self)
        self.system ('''
install -m755 %(builddir)s/src/denemo-windows.exe %(install_prefix)s/bin/denemo.exe
install -m755 %(builddir)s/src/denemo-console.exe %(install_prefix)s/bin/denemo-console.exe
''')

# Use console for debugging for Windows.
#Denemo__mingw = Denemo__mingw__windows
Denemo__mingw = Denemo__mingw__console

class Denemo__darwin (Denemo):
    source = 'git://git.savannah.gnu.org/denemo.git'
    branch = 'darwin'
    dependencies = [x for x in Denemo.dependencies
                    if x.replace ('-devel', '') not in [
            'libxml2', # Included in darwin-sdk, hmm?
            'portaudio'
	    ]] + [
        'fondu',
        'osx-lilypad',
        ]
    #patches = ['denemo-utils-apple.c']

    configure_flags = (Denemo.configure_flags
	#		   + ' --enable-debug'
		       	   + ' --disable-binreloc'
			   + ' --disable-portmidi'
			   + ' --with-static-portmidi'
			   + ' --disable-portaudio'
			   + ' --disable-x11'
			   + ' --disable-jack')
	
    configure_variables = (Denemo.configure_variables
 			   + ' CFLAGS="-g -O0 -D__APPLE__ -I%(system_prefix)s/include/evince/2.30 -D__APPLE__" '
			   + ' LDFLAGS="-L%(system_prefix)s/lib -levview -levdocument -D__APPLE__" ')

class Denemo__darwin__ppc (Denemo__darwin):
    # make sure that PREFIX/include/unistd.h gets included
    def patch (self):
        Denemo__darwin.patch (self)
        self.system ('''
mkdir -p %(builddir)s/src
cp -pv %(system_prefix)s/include/unistd.h %(builddir)s/src
''')
