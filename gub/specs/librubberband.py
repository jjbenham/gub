from gub import target

class Librubberband (target.AutoBuild):
    source = 'http://denemo.org/downloads/gub/rubberband-1.8.1.tar.gz'
    dependencies = ['vamp-plugin-sdk', 'libsamplerate', 'libsndfile', 'libfftw']
#    configure_variables = (target.AutoBuild.configure_variables
# 			   + ' Vamp_CFLAGS="-I%(system_prefix)s/../vamp-sdk/" '
#			   + ' Vamp_LIBS="-L%(system_prefix)s/../vamp-plugin-sdk-2.5-binaries-win32-mingw -lvamp-sdk" ')
#    patches = ['librubberband_rubberband-c.h.patch']

