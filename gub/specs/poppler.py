from gub import target

class Poppler (target.AutoBuild):
    #source = 'http://poppler.freedesktop.org/poppler-0.22.2.tar.gz'
    source = 'http://cgit.freedesktop.org/poppler/poppler/snapshot/poppler-0.18.4.tar.gz'
    dependencies = ['tools::libtool', 'tools::glib', 'glib-devel',
                'zlib-devel',
                'fontconfig-devel',
                #'gtk+-devel',
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

class Poppler__darwin (Poppler):
    dependencies = [x for x in Poppler.dependencies
                if x.replace ('-devel', '') not in [
                'libxml2', # Included in darwin-sdk, hmm?
                ]]
