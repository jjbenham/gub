from gub import target

class Libx11 (target.AutoBuild):
    source = 'http://ftp.de.debian.org/debian/pool/main/libx/libx11/libx11_1.5.0.orig.tar.gz'
    dependencies = ['tools::pkg-config', 'libtool', 'inputproto-devel', 'kbproto-devel', 'libxcb-devel', 'xextproto-devel', 'xproto-devel', 'xtrans-devel']
    configure_flags = (target.AutoBuild.configure_flags
                + ' --disable-xf86bigfont'
                + ' --disable-malloc0returnsnull')
#    def patch (self):
#        self.file_sub ([('pkg-config', '$PKG_CONFIG')],
#                       '%(srcdir)s/configure')
    def compile (self):
        self.system ('cd %(builddir)s && make -C src/util makekeys CC=gcc CFLAGS= makekeys_CFLAGS= LDFLAGS=')
        target.AutoBuild.compile (self)
