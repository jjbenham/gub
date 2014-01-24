from gub import target

class Librsvg (target.AutoBuild):
    source = 'http://ftp.gnome.org/pub/GNOME/sources/librsvg/2.26/librsvg-2.26.0.tar.gz'
    dependencies = ['tools::libtool',
                'fontconfig-devel',
                'glib-devel',
                'gtk+-devel',
                'libxml2-devel']
    configure_flags = (target.AutoBuild.configure_flags
                       	+ ' --enable-static'
			+ ' --disable-shared'
                       	)

