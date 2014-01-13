from gub import tools

class Intltool (tools.AutoBuild):
    source = 'ftp://ftp.gnome.org/pub/GNOME/sources/intltool/0.40/intltool-0.40.5.tar.gz'
    dependencies = [
            'tools::perl-xml-parser',
	    'tools::intltool'
            ]
class Intltool__tools (tools.AutoBuild):
    source = 'ftp://ftp.gnome.org/pub/GNOME/sources/intltool/0.40/intltool-0.40.5.tar.gz'
    dependencies = [
           'tools::perl-xml-parser'
			]            
    configure_flags = (tools.AutoBuild.configure_flags
                       + ' --build=%(build_architecture)s'
                       + ' --host=%(build_architecture)s'
                       + ' --target=%(build_architecture)s'
                       )
