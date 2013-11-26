from gub import target
from gub import tools

class Portmidi (target.AutoBuild):
  source = 'http://www.denemo.org/downloads/gub/libportmidi-0.217.tar.gz'

class Portmidi__mingw (target.AutoBuild):
  source = 'http://www.denemo.org/downloads/gub/libportmidi-0.218.tar.gz'
