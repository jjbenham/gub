from gub import build

class Vamp_dev (build.BinaryBuild, build.SdkBuild):
    source = 'http://code.soundsoftware.ac.uk/attachments/download/690/vamp-plugin-sdk-2.5.tar.gz'

#    source = 'http://code.soundsoftware.ac.uk/attachments/download/694/vamp-plugin-sdk-2.5-binaries-win32-mingw.zip'
    def untar (self):
        build.BinaryBuild.untar (self)
#        self.system ('''
#cd  %(srcdir)s/ && mkdir usr && mv *.dll *.a usr/
#''')

