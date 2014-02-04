import os
#
from gub import context
from gub import cross
from gub import misc
from gub import repository
from gub import target

# Hmm? TARGET_CFLAGS=-O --> target.py

'''
URG glibc-2.3 has this beauty
in sysdeps/unix/sysv/linux/configure.in
  
# The Linux kernel headers can be found in
#   /lib/modules/$(uname -r)/build/include
# Check whether this directory is available.
if test -z "$sysheaders" &&
   test "x$cross_compiling" = xno &&
   test -d /lib/modules/`uname -r`/build/include; then
  sysheaders="/lib/modules/`uname -r`/build/include"
  ccheaders=`$CC -print-file-name=include`
  dnl We do not have to use -nostdinc.  We just want one more directory
  dnl to be used.
  SYSINCLUDES="-I $sysheaders"
fi

Which makes, that when we are not cross compiling, eg: target/linux-64
on a x86_64, we will try to include /lib/modules/.../build/include,
and LD_PRELOAD will make us barf.

We should be able to silence this using --with-headers.  So,
while --with-headers adds no new include path, it tells configure
to *not* look in /.
'''

# FIXME: also cross.
# cross/gcc can only depend on glibc-core if glibc-core is also a
# cross package.  With glibc as cross package, all packages
# automagically depend on it, which is nice.
# See cross.py:set_cross_dependencies ()
class Glibc (target.AutoBuild, cross.AutoBuild):
    source = 'http://lilypond.org/download/gub-sources/glibc-2.3-20070416.tar.bz2'
    patches = [
        'glibc-2.3-powerpc-initfini.patch',
        'glibc-2.3-powerpc-socket-weakalias.patch',
        'glibc-2.3-powerpc-lround-weakalias.patch',
        'glibc-2.3-nptl-no-versioning.patch',
        'glibc-2.3-slibdir.patch',
        'glibc-2.3-assert-dl_next_tls_modid.patch',
        'glibc-2.3-binutils-2.19-i386.patch',
        ]
    dependencies = ['cross/gcc', 'glibc-core', 'tools::gzip', 'tools::perl', 'linux-headers']
    configure_flags = (target.AutoBuild.configure_flags + misc.join_lines ('''
--disable-profile
--disable-debug
--without-cvs
--without-gd
--with-headers=%(system_prefix)s/include
''')
                + '%(enable_add_ons)s')
    make_flags = ' SHELL=/bin/bash'
    install_flags = (target.AutoBuild.install_flags
                     + ' install_root=%(install_root)s'
                     # glibc-2.3.6' Makerules file has a cross-compiling
                     # check that changes symlink install behaviour.  ONLY
                     # if $(cross_compiling)==no, an extra
                     # `install-symbolic-link' target is created upon with
                     # `install' is made to depend.  This means we do not
                     # get symlinks with install-lib-all when it so happens
                     # that build_architecture == target_architecture.  Try
                     # to cater for both here: make the symlink as well as
                     # append to the symlink.list file.
                     + ''' make-shlib-link='ln -sf $(<F) $@; echo $(<F) $@ >> $(common-objpfx)elf/symlink.list' ''')
    configure_command = 'BUILD_CC=gcc ' + target.AutoBuild.configure_command
    config_cache_overrides = (target.AutoBuild.config_cache_overrides + '''
use_default_libc_cv_slibdir=%(prefix_dir)s/slib
libc_cv_rootsbindir=%(prefix_dir)s/sbin
''')
    def get_conflict_dict (self):
        return {'': ['glibc-core'], 'devel': ['glibc-core'], 'doc': ['glibc-core'], 'runtime': ['glibc-core']}
    def patch (self):
        target.AutoBuild.patch (self)
    def get_add_ons (self):
        return ('linuxthreads', 'nptl')
    @context.subst_method
    def enable_add_ons (self):
        add_ons = ''
        for i in self.get_add_ons ():
            add_ons += ' --enable-add-ons=' + i
        return add_ons
    def linuxthreads (self):
        return repository.get_repository_proxy (self.settings.downloads,
                                                self.expand ('http://ftp.gnu.org/pub/gnu/glibc/glibc-linuxthreads-%(version)s.tar.bz2&strip_components=0'))
    def download (self):
        target.AutoBuild.download (self)
        if self.version () == '2.3.6':
            self.linuxthreads ().download ()
    def untar (self):
        target.AutoBuild.untar (self)
        if self.version () == '2.3.6':
            self.linuxthreads ().update_workdir (self.expand ('%(srcdir)s/urg-do-not-mkdir-or-rm-me'))
            self.system ('mv %(srcdir)s/urg-do-not-mkdir-or-rm-me/* %(srcdir)s')
    # Disable librestrict.so, as it causes crashes on Fedora 9 and 10.
    def LD_PRELOAD (self):
        return ''

class Glibc__linux__mipsel (Glibc):
    patches = Glibc.patches + [
        'glibc-2.3-mips-syscall.patch',
        ]
    def get_add_ons (self):
        return ('linuxthreads',)
