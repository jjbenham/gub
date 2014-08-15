from gub import target
from gub import tools

class Evince2 (target.AutoBuild):
  source = 'http://ftp.gnome.org/pub/GNOME/sources/evince/2.32/evince-2.32.0.tar.bz2'
  
  dependencies = [
		  #'intltool',
		  'tools::intltool',
		  'gtk2',
		  'poppler-devel']
  patches = ['evince-4-Makefile.patch']
  configure_flags = (tools.AutoBuild.configure_flags
			   #+ ' --with-libintl-prefix=%(install_prefix)s'
                           #+ ' --enable-static'
			   + ' --without-libgnome'
			   + ' --without-gconf'
                           + ' --without-keyring'
                           + ' --with-platform=win32'
			   + ' --with-smclient-backend=win32' #not sure what this is
			   + ' --disable-help'
			   + ' --disable-thumbnailer'
			   + ' --disable-nautilus'
			   + ' --disable-dbus'
			   + ' --disable-gtk-doc'
			   #+ ' --disable-pdf' #FIXME probably need pdf support
			   + ' --disable-previewer' #not sure if this is needed
			   + ' --disable-nls'
			   + ' --without-gtk-unix-print')

  configure_variables = (tools.AutoBuild.configure_variables
                           + ' CPPFLAGS="-D_WIN32_WINNT=0x0501"')


