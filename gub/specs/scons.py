from gub import tools

class Scons__tools (tools.PythonBuild):
    source = 'http://surfnet.dl.sourceforge.net/sourceforge/scons/scons-2.2.0.tar.gz'
    license_files = ['%(srcdir)s/LICENSE.txt']
