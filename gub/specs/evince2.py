from gub import target
from gub import tools

class Evince2 (target.AutoBuild):
  source = 'http://ftp.gnome.org/pub/GNOME/sources/evince/2.32/evince-2.32.0.tar.bz2'
#  patches = ['evince-2.32.0-configure.patch'] 
  patches = ['evince-4-Makefile.patch', 'evince-2.32.0-configure.patch', 'evince-3.2.1-backenddir.patch']
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
			   + ' --disable-tests'
                          # + ' --with-platform=gnome'
			   + ' --with-smclient-backend=quartz'
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
#  def compile (self):
#  	self.system ('cd %(builddir)s/libdocument && make')
#        self.system ('cd %(builddir)s/libview && make')
#  	self.system ('cd %(builddir)s/backend && make')

#  def install (self):
	#self.system ('mkdir -p %(install_prefix)s/lib/pkgconfig')
        #self.system ('cd %(builddir)s/libdocument && make DESTDIR=%(install_root)s install')
        #self.system ('cd %(builddir)s/libview && make DESTDIR=%(install_root)s install')
	#self.system ('cd %(builddir)s/backend && make DESTDIR=%(install_root)s install')
 #       self.system ('cd %(builddir)s/ && make DESTDIR=%(install_root)s/ install')

        #self.system ('cd %(builddir)s/ && cp -pv evince-document-2.32.pc %(install_root)s/usr/lib/pkgconfig')
        #self.system ('cd %(builddir)s/ && cp -pv evince-view-2.32.pc %(install_prefix)s/lib/pkgconfig')
#	self.system ('install -m755 %(builddir)s/evince-view-2.32.pc  %(install_prefix)s/lib/pkgconfig')

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

               
