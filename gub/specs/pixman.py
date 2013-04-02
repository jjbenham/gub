from gub import target

class Pixman (target.AutoBuild):
    source = 'http://www.cairographics.org/releases/pixman-0.26.0.tar.gz'
    dependencies = ['libtool','libpng']

class Pixman__linux__ppc (Pixman):
    patches = ['pixman-0.13.2-auxvec.patch']
