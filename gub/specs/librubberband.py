from gub import target

class Librubberband (target.AutoBuild):
#     source = 'https://bitbucket.org/breakfastquay/rubberband/get/tip.tar.bz2'
#     source = 'http://code.breakfastquay.com/attachments/download/34/rubberband-1.8.1.tar.bz2'
     source = 'http://denemo.org/downloads/gub/rubberband-1.8.1.tar.gz'
     dependencies = ['vamp-plugin-sdk', 
		     'libsamplerate', 
		     'libsndfile', 
		     'libfftw', 
		     'ladspa']
     configure_variables = (target.AutoBuild.configure_variables
			   + ' CFLAGS="" '
			   + ' LIBS="-L%(system_prefix)s/lib -lgcc -lfftw3" ')

