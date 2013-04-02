from gub import gnome
from gub import target

class Atk (target.AutoBuild):
    source = 'http://ftp.gnome.org/pub/GNOME/platform/2.32/2.32.1/sources/atk-2.6.0.tar.xz'
    dependencies = ['tools::libtool', 'glib-devel']

class Atk__mingw (Atk):
    patches = [
        #'atk-mingw.patch',
        ]
    def patch (self):
        #target.AutoBuild.patch (self)
        self.file_sub ([('\$\(srcdir\)/atk.def', 'atk.def')], '%(srcdir)s/atk/Makefile.in', must_succeed=True)
