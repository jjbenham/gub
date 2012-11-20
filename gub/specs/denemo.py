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
#    source = ''
    source = 'git://git.savannah.gnu.org/denemo.git'
    branch = 'apple'
#    branch = 'master'
#    patches = ['denemo-SIGCHLD.patch']
    subpackage_names = ['']
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
	'fluidsynth'
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
    #dependencies = ['alsa-devel']
    configure_flags = (Denemo.configure_flags
                   		+ ' --enable-binreloc'
				+ ' --disable-portmidi'
		#		+ ' --enable-debug'
			        + ' --enable-alsa'
				+ ' --with-pmidi-platform=linux')
    configure_variables = (target.AutoBuild.configure_variables
 			   + ' CFLAGS="-I%(system_prefix)s/include/evince/2.30 " '
			   + ' LDFLAGS="-L%(system_prefix)s/lib -levview -levdocument" ')



class Denemo__mingw__windows (Denemo):
    dependencies = [x for x in Denemo.dependencies
                    if x.replace ('-devel', '') not in [
            'lash',
            ]] + ['lilypad']
    configure_flags = (Denemo.configure_flags
			+ ' --enable-binreloc'
			+ ' --disable-portmidi'
			+ ' --with-pmidi-platform=mingw')
    configure_variables = (Denemo.configure_variables
 			   + ' CFLAGS="-I%(system_prefix)s/include/evince/2.30" '
			   + ' LDFLAGS="-L%(system_prefix)s/lib -levview -levdocument" ')
    
    def __init__ (self, settings, source):
        Denemo.__init__ (self, settings, source)
        # Configure (link) without -mwindows for denemo-console.exe
        self.target_gcc_flags = '-mms-bitfields'

    #make_flags = ''

class Denemo__mingw__console (Denemo__mingw__windows):
    configure_flags = (Denemo__mingw__windows.configure_flags
                         #  .replace(' --enable-binreloc', ' --disable-binreloc')
		       	   + ' --disable-binreloc'
			   + ' --enable-debug'
			   + ' --disable-portmidi'
			   + ' --enable-win32portmidi')
		            
    #configure_variables = (Denemo__mingw__windows.configure_variables
 			   #+ ' PKG_CONFIG_PATH=%(system_prefix)s/lib/pkgconfig'
 			   #+ ' EVINCE_2_30_CFLAGS="-I%(system_prefix)s/include/evince/2.30" EVINCE_2_30_LIBS="-L%(system_prefix)s/lib -levview -levdocument"')
    def __init__ (self, settings, source):
        Denemo__mingw__windows.__init__ (self, settings, source)
        # Configure (link) without -mwindows for denemo-console.exe
        self.target_gcc_flags = '-mms-bitfields'
    def compile (self):
        Denemo__mingw__windows.compile (self)
        self.system ('''
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
    dependencies = [x for x in Denemo.dependencies
                    if x.replace ('-devel', '') not in [
            'libxml2', # Included in darwin-sdk, hmm?
            'portaudio'
	    ]] + [
        'fondu',
        'osx-lilypad',
        ]
    configure_flags = (Denemo.configure_flags
		       	   + ' --enable-binreloc'
#			   + ' --enable-debug'
			   + ' --disable-portmidi'
			   + ' --with-pmidi-platform=darwin'
			   + ' --disable-portaudio'
			   + ' --disable-jack')
	
    configure_variables = (Denemo.configure_variables
 			   + ' CFLAGS="-I%(system_prefix)s/include/evince/2.30 -DWITHOUT_SCREENSHOT -DUNUSED__APPLE" '
			   + ' LDFLAGS="-L%(system_prefix)s/lib -levview -levdocument -DWITHOUT_SCREENSHOT -DUNUSED__APPLE" '
					
#	  		 + ' EVINCE_2_30_CFLAGS="-I%(system_prefix)s/include/evince/2.30" EVINCE_2_30_LIBS="-L%(system_prefix)s/lib -levview -levdocument"'
)

class Denemo__darwin__ppc (Denemo__darwin):
    # make sure that PREFIX/include/unistd.h gets included
    def patch (self):
        Denemo__darwin.patch (self)
        self.system ('''
mkdir -p %(builddir)s/src
cp -pv %(system_prefix)s/include/unistd.h %(builddir)s/src
''')
