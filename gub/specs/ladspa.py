from gub import build

class Ladspa (build.BinaryBuild, build.SdkBuild):
    source = "http://www.ladspa.org/download/ladspa_sdk.tgz"
    def install (self):
        self.system ('''
mkdir -p %(install_prefix)s/include
cp %(srcdir)s/src/ladspa.h %(install_prefix)s/include
''', locals ())
 
