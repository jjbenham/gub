from gub import build
from gub import context
from gub import misc
from gub import tools

class ImageMagick__tools (tools.AutoBuild):
    source = 'http://ftp.nluug.nl/ImageMagick/ImageMagick-6.8.7-5.tar.bz2'
    dependencies = [
            'automake',
            'bzip2',
            'fontconfig',
            'ghostscript',
            'libpng',
            'libjpeg',
            'libtiff',
            'libxml2',
            'libtool',
            'perl',
            'zlib',
            ]
    configure_flags = (tools.AutoBuild.configure_flags
                + misc.join_lines ('''
--without-magick-plus-plus
--without-perl
'''))

class ImageMagick__tools__autoupdate (ImageMagick__tools):
    def autoupdate (self):
        self.system ('''
cd %(autodir)s && libtoolize --copy --force --automake --ltdl
cd %(autodir)s && autoheader -I m4 -I %(system_prefix)s/share/aclocal
cd %(autodir)s && aclocal -I m4 -I %(system_prefix)s/share/aclocal
cd %(autodir)s && autoconf -I m4 -I %(system_prefix)s/share/aclocal
cd %(autodir)s && automake --add-missing --copy --foreign
''')
    def configure (self):
        tools.AutoBuild.configure (self)
        self.file_sub ([('(( *)install_libdir="\$2")',
                         r'''\1
\2if test -z "$install_libdir"; then
\2    install_libdir=%(system_prefix)s/lib;
\2fi
''')],
                       '%(builddir)s/libtool')

# Hmm, see LilyPond
Imagemagick__tools = ImageMagick__tools
