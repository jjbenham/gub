from gub import target
from gub import tools

class Evince (target.AutoBuild):
  source = 'http://www.denemo.org/downloads/gub/evince-2.30.3.tar.bz2'
  
  dependencies = ['intltool',
		  'libxml2-devel',
		  'poppler-devel']

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

#class Evince__darwin__x86 (Evince):
#  configure_variables = (tools.AutoBuild.configure_variables
#                           + ' CFLAGS="-g -O0" ')

class Evince__linux__x86 (Evince):
  configure_variables = (tools.AutoBuild.configure_variables
                           + ' CFLAGS="-g -O0 -DHAVE_POPPLER_PAGE_RENDER" ')

#  def compile (self):
#  	self.system ('cd %(builddir)s/libdocument && make')
#        self.system ('cd %(builddir)s/libview && make')
#  	self.system ('cd %(builddir)s/backend && make')
#  def install (self):
#        self.system ('cd %(builddir)s/libdocument && make DESTDIR=%(install_root)s install')
#        self.system ('cd %(builddir)s/libview && make DESTDIR=%(install_root)s install')
#	self.system ('cd %(builddir)s/backend && make DESTDIR=%(install_root)s install')
#	self.system ('cd %(builddir)s/ && make DESTDIR=%(install_root)s/ install')

#        self.system ('cd %(builddir)s/ && cp -pv evince-document-2.30.pc %(install_root)s/usr/lib/pkgconfig')
#        self.system ('cd %(builddir)s/ && cp -pv evince-view-2.30.pc %(install_prefix)s/lib/pkgconfig')
#	self.system ('install -m755 %(builddir)s/evince-view-2.30.pc  %(install_prefix)s/lib/pkgconfig')

#	also need evince-view.h and evince-document.h to be installed
#gub/specs/zlib.py:        self.system ('cd %(srcdir)s/contrib/minizip && cp ioapi.h iowin32.h mztools.h unzip.h zip.h %(install_prefix)s/include')

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
  dependencies = ['libsm']

               
