from gub import target

class Libgtksourceview2 (target.AutoBuild):
    source = 'http://ftp.gnome.org/pub/gnome/sources/gtksourceview/2.11/gtksourceview-2.11.2.tar.gz'
    dependencies = [
        'gtk2',
        ]
