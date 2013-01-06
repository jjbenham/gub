from gub import target
from gub import tools

class Libice (target.AutoBuild):
  source = 'http://xorg.freedesktop.org/archive/individual/lib/libICE-1.0.6.tar.bz2'
  
  dependencies = []
  #patches = ['evince-no-gnome-doc-utils.patch']#['evince-icon.patch', 'evince-po.patch'] 
 # configure_flags = (tools.AutoBuild.configure_flags
			   #+ ' --with-libintl-prefix=%(install_prefix)s'
 #                          + ' --without-help'
#			   + ' --without-libgnome')
#  configure_variables = (tools.AutoBuild.configure_variables
#                           + ' CPPFLAGS="-D_WIN32_WINNT=0x0501"')


