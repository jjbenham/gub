from gub import target
from gub import build

class Vamp_plugin_sdk (build.BinaryBuild, build.SdkBuild):
    source = 'http://code.soundsoftware.ac.uk/attachments/download/694/vamp-plugin-sdk-2.5-binaries-win32-mingw.zip'
    #source = 'http://code.soundsoftware.ac.uk/attachments/download/690/vamp-plugin-sdk-2.5.tar.gz'
    dependencies = ['vamp-dev']
    def untar (self):
        build.BinaryBuild.untar (self)
#        self.system ('''
#cd  %(srcdir)s/vamp-plugin-sdk-2.4-binaries-win32-mingw && mkdir usr && mv *.dll *.a usr/
#''')

