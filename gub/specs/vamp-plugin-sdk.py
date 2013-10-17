from gub import target
from gub import build

class Vamp_plugin_sdk (target.AutoBuild):
    source = 'http://denemo.org/downloads/gub/vamp-plugin-sdk-2.5.tar.gz'
    dependencies = ['libsndfile']

