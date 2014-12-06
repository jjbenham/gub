#
from gub import context
from gub import target

class Libxcb (target.AutoBuild):
    #source = 'http://xcb.freedesktop.org/dist/libxcb-0.9.93.tar.gz'
    #1.1.92 removes libxcb-xlib, which libx11-1.1.15 needs?
    source = 'http://www.x.org/releases/X11R7.7/src/everything/libxcb-1.8.1.tar.bz2'
    '''
xproto.c:3056: error: conflicting types for 'xcb_get_atom_name_name'
/home/janneke/vc/gub/target/linux-64/src/libxcb-1.1.93/src/xproto.h:6867: error: previous declaration of 'xcb_get_atom_name_name' was here
'''
    #source = 'http://xcb.freedesktop.org/dist/libxcb-1.1.91.tar.gz'
    '''
xproto.c: In function 'xcb_configure_window_checked':
xproto.c:2479: error: 'xcb_configure_window_request_t' has no member named 'pad1'
'''
    #patches = ['libxcb-1.1.93.patch']
    dependencies = ['tools::libtool', 'libpthread-stubs-devel', 'libxau-devel', 'xcb-proto-devel', 'libxslt']
    parallel_build_broken = True

    configure_variables = (target.AutoBuild.configure_variables
                           + ' PKG_CONFIG_PATH=%(system_prefix)s/lib/pkgconfig')

class Libxcb__freebsd (Libxcb):
    patches = Libxcb.patches + ['libxcb-0.9.93-freebsd.patch']
    configure_variables = (Libxcb.configure_variables
                + ' LDFLAGS=-pthread')

class Libxcb__mingw (Libxcb):
    patches = []
    dependencies = [x for x in Libxcb.dependencies
                if 'libpthread-stubs' not in x]
