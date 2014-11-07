from gub import target

class Libgtksourceview2 (target.AutoBuild):
    source = 'http://ftp.gnome.org/pub/gnome/sources/gtksourceview/2.6/gtksourceview-2.6.2.tar.gz'
    dependencies = [
	'tools::intltool',
        'gtk2',
        ]
