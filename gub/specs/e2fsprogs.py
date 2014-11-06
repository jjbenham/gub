from gub import target

# FIXME: updateme and dependants, package has finally been split
# http://sourceforge.net/projects/e2fsprogs/files/
class E2fsprogs (target.AutoBuild):
    source = 'http://pkgs.fedoraproject.org/repo/pkgs/e2fsprogs/e2fsprogs-1.38.tar.gz/d774d4412bfb80d12cf3a4fdfd59de5a/e2fsprogs-1.38.tar.gz'
    configure_flags = (target.AutoBuild.configure_flags
                       + '  --enable-elf-shlibs')
    install_command = (target.AutoBuild.install_command
                + ' install-libs')
