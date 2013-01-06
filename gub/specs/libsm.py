from gub import target
from gub import tools

class Libsm (target.AutoBuild):
  source = 'http://cgit.freedesktop.org/xorg/lib/libSM/snapshot/libSM-1_0_1.tar.gz'
  
  dependencies = ['libice']
  #patches = ['evince-no-gnome-doc-utils.patch']#['evince-icon.patch', 'evince-po.patch'] 
 # configure_flags = (tools.AutoBuild.configure_flags
			   #+ ' --with-libintl-prefix=%(install_prefix)s'
 #                          + ' --without-help'
#			   + ' --without-libgnome')
#  configure_variables = (tools.AutoBuild.configure_variables
#                           + ' CPPFLAGS="-D_WIN32_WINNT=0x0501"')


