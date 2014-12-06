from gub import target

class Libx11 (target.AutoBuild):
    source = 'http://xorg.freedesktop.org/releases/individual/lib/libX11-1.4.99.1.tar.bz2'
    dependencies = ['tools::pkg-config', 'libtool', 'inputproto-devel', 'kbproto-devel', 'libxcb-devel', 'xextproto-devel', 'xproto-devel', 'xtrans-devel']
    configure_flags = (target.AutoBuild.configure_flags
                + ' --disable-xf86bigfont'
                + ' --disable-malloc0returnsnull')
    configure_variables = (target.AutoBuild.configure_variables
                        + ' CFLAGS="-I%(system_prefix)s/include" ')

    def patch (self):
        self.file_sub ([('pkg-config', '$PKG_CONFIG')],
                       '%(srcdir)s/configure')
    def compile (self):
        self.system ('cd %(builddir)s && make -C src/util makekeys CC=gcc makekeys_CFLAGS=')
        target.AutoBuild.compile (self)
