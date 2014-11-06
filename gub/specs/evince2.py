from gub import target
from gub import tools

class Evince2 (target.AutoBuild):
  source = 'http://www.denemo.org/downloads/gub/evince-2.30.3.tar.bz2'
  
  dependencies = ['intltool',
#		  'libxml2-devel',
		  'gtk2',
		  'poppler']

#  patches = ['evince_stripped.patch']
  configure_flags = (tools.AutoBuild.configure_flags
                           + ' --without-help'
			   + ' --without-libgnome'
			   + ' --without-gconf'
                           + ' --without-keyring'
                           + ' --with-platform=gnome'
			   + ' --with-smclient-backend=no'
			   + ' --disable-help'
			   + ' --disable-thumbnailer'
			   + ' --disable-nautilus'
			   + ' --disable-dbus'
			   + ' --disable-gtk-doc'
			   + ' --disable-previewer'
			   + ' --disable-nls'
			   + ' --disable-scrollkeeper'
			   + ' --disable-tiff'
			   + ' --disable-comics'
			   + ' --without-gtk-unix-print')

class Evince2__darwin__x86 (Evince2):
  configure_variables = (tools.AutoBuild.configure_variables
                           + ' CFLAGS="-g -O0" ')

class Evince2__linux__x86 (Evince2):
  configure_variables = (tools.AutoBuild.configure_variables
                           + ' CFLAGS="-g -O0 -DHAVE_POPPLER_PAGE_RENDER" ')

class Evince2__mingw (Evince2):
#  patches = ['evince-icon.patch']
  configure_flags = (Evince2.configure_flags
                           + ' --with-platform=win32'
			   + ' --with-smclient-backend=win32')

  configure_variables = (Evince2.configure_variables
                           + ' CPPFLAGS="-D_WIN32_WINNT=0x0501"')
class Evince2__linux__x86 (Evince2):
  configure_flags = (Evince2.configure_flags
                           + ' --with-platform=gnome'
			   + ' --with-smclient-backend=xsmp')
  dependencies = ['libsm']

               
