from gub import target

class Libgtksourceview (target.AutoBuild):
    source = 'http://ftp.gnome.org/pub/gnome/sources/gtksourceview/3.2/gtksourceview-3.2.3.tar.xz'
    patches = ['gtksourceview-3.2.3.no.po.patch']
    dependencies = [
            'gtk+-devel',
            'libxml2-devel',
            'tools::intltool',
            ]
    configure_flags = (target.AutoBuild.configure_flags
			+ ' --enable-static'
			+ ' --disable-shared'
                       	)
class Libgtksourceview__mingw (Libgtksourceview):
    def install (self):
        target.AutoBuild.install (self)
        self.system ('cd %(install_prefix)s/lib/ && ln -s libgtksourceview-3.0.a libgtksourceview-3.0.dll.a')

