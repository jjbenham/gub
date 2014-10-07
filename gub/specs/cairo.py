from gub import target

class Cairo (target.AutoBuild):
    source = 'http://www.cairographics.org/releases/cairo-1.12.16.tar.xz'
    def patch (self):
        target.AutoBuild.patch (self)
        self.system ('rm -f %(srcdir)s/src/cairo-features.h')
    dependencies = [
                'fontconfig-devel',
                'ghostscript-devel',
                'libpng-devel',
                'pixman-devel',
		'glib',
                'zlib-devel']
class Cairo__linux (Cairo):
    source = 'http://www.cairographics.org/releases/cairo-1.12.2.tar.xz'
    dependencies = (Cairo.dependencies + ['libxrender-devel'])

class Cairo_without_X11 (Cairo):
    configure_flags = (Cairo.configure_flags
                + ' --disable-xlib'
                + ' --disable-xlib-xrender'
                + ' --disable-xcb'
                )

class Cairo__mingw (Cairo_without_X11):
    configure_flags = (Cairo_without_X11.configure_flags
                + ' --enable-win32=yes'
                + ' --enable-win32-font=yes'
                + ' --enable-ft'
                + ' LDFLAGS=-lpthread'
                )
    dependencies = (Cairo_without_X11.dependencies
                    + ['pthreads-w32-devel'])

class Cairo__darwin (Cairo_without_X11):
     source = 'http://www.cairographics.org/releases/cairo-1.10.2.tar.gz'
     configure_flags = (Cairo_without_X11.configure_flags
                + ' --enable-quartz'
		+ ' --enable-quartz-font'
                + ' --enable-freetype'
                + ' --enable-quartz-image'
		+ ' --enable-png'
	        + ' --enable-pdf'
		+ ' --enable-gobject=yes'
                )

class Cairo__darwin__ppc (Cairo__darwin):
    patches = Cairo__darwin.patches + [
        'cairo-1.8.8-darwin-ppc.patch',
        ]
