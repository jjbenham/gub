from gub import target

class Poppler (target.AutoBuild):
    source = 'http://poppler.freedesktop.org/poppler-0.20.0.tar.gz'
    dependencies = ['tools::libtool', 'tools::glib',
                'zlib-devel',
                'fontconfig-devel',
                'libpng',
                'libjpeg-devel',
                'libxml2-devel',
                ]
    configure_flags = (target.AutoBuild.configure_flags
                + ' --disable-poppler-qt'
                + ' --disable-poppler-qt4'
                + ' --enable-xpdf-headers'
                + ' --disable-gtk-test'
		+ ' --disable-libjpeg')
                # FIXME: poppler, librsvg, cairo, gtk dependencies?
                # gtk+ depends on pango, pango on cairo, cairo on poppler, and poppler on gtk+ and cairo
                # TRIED: removing gtk+ dependency from poppler -- no go
                # TRY: removing poppler from cairo...
                #+ ' --disable-gdk'
                #+ ' --disable-splash-output'
                #+ ' --disable-cairo' ? 

class Poppler__mingw (Poppler):
    #patches = ['poppler-0.11.2-mingw.patch']
    pass


