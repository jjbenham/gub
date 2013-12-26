from gub import gnome
from gub import target

class Atk (target.AutoBuild):
    source = 'http://ftp.acc.umu.se/pub/gnome/sources/atk/2.4/atk-2.4.0.tar.xz'
    dependencies = ['tools::libtool', 'glib-devel']

class Atk__mingw (Atk):
    patches = [
        #'atk-mingw.patch',
        ]
    def patch (self):
        #target.AutoBuild.patch (self)
        self.file_sub ([('\$\(srcdir\)/atk.def', 'atk.def')], '%(srcdir)s/atk/Makefile.in', must_succeed=True)
