from gub import target
from gub import tools

class Evince (target.AutoBuild):
  source = 'http://ftp.gnome.org/pub/GNOME/sources/evince/3.2/evince-3.2.1.tar.xz'
  dependencies = ['intltool',
		  'libxml2-devel',
		  'poppler'
			]

  patches = ['evince-3.2.1-strip.patch']
  configure_flags = (tools.AutoBuild.configure_flags
                           + ' --without-help'
			   + ' --without-libgnome'
			   + ' --without-gconf'
                           + ' --without-keyring'
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
  def install (self):
	target.AutoBuild.install (self)
        self.system ('cd %(install_prefix)s/lib/ && ln -s libevview3.a libevview3.dll.a')
	self.system ('cd %(install_prefix)s/lib/ && ln -s libevdocument3.a libevdocument3.dll.a')

class Evince__darwin__x86 (Evince):
  configure_variables = (tools.AutoBuild.configure_variables
                           + ' CFLAGS="-g -O0" ')

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
#  configure_variables = (Evince.configure_variables
#                           + ' CFLAGS="-g -O0" ')
  #make_flags = ' -DHAVE_POPPLER_PAGE_RENDER=1'

  #dependencies = ['libsm']

               
