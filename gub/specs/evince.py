from gub import target
from gub import tools

class Evince (target.AutoBuild):
  source = 'http://www.denemo.org/downloads/gub/evince-2.30.3.tar.bz2'
  
  dependencies = ['intltool',
#		  'libxml2-devel',
		  'poppler-devel']

  #patches = ['evince_stripped.patch']
  configure_flags = (tools.AutoBuild.configure_flags
                           + ' --without-help'
			   + ' --without-libgnome'
			   + ' --without-gconf'
                           + ' --without-keyring'
#                           + ' --with-platform=gnome'
#			   + ' --with-smclient-backend=no'
			   + ' --disable-help'
			   + ' --disable-thumbnailer'
			   + ' --disable-nautilus'
			   + ' --disable-dbus'
			   + ' --disable-gtk-doc'
			   + ' --disable-previewer'
			   + ' --disable-nls'
			   + ' --disable-scrollkeeper'
			   + ' --without-gtk-unix-print'
			   + ' --disable-tiff'
			   + ' --disable-comics'
			   + ' --disable-tests'	
			   + ' --disable-dvi')

#evince-document-2.30.pc target/darwin-x86/root/usr/lib/pkgconfig/x11.pc
#evince-view-2.30.pc
#
#    def get_subpackage_definitions (self):
#        s = target.AutoBuild.get_subpackage_definitions (self)
#        s['doc'].append (self.settings.prefix_dir + '/lib/tk8.4/demos')
#        return s
 
class Evince__mingw (Evince):
#  patches = ['evince-icon.patch']
  configure_flags = (Evince.configure_flags
                           + ' --with-platform=win32'
			   + ' --with-smclient-backend=win32')

  configure_variables = (Evince.configure_variables
                           + ' CPPFLAGS="-D_WIN32_WINNT=0x0501"')

class Evince__linux__x86 (Evince):
  configure_flags = (Evince.configure_flags
                           + ' --with-platform=gnome'
			   + ' --with-smclient-backend=xsmp')
  dependencies = ['libsm', 'poppler-devel']

class Evince__darwin (Evince):
  dependencies = [x for x in Evince.dependencies
	                   if x.replace ('-devel', '') not in [
                	   'libxml2', # Included in darwin-sdk, hmm?
                	   ]] + ['libxdmcp']

#  configure_flags = (Evince.configure_flags
 #                          + ' --with-platform=gnome'
#			   + ' --with-smclient-backend=quartz')

                
