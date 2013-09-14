from gub import target
from gub import build

class Vamp_plugin_sdk (target.AutoBuild):
    source = 'http://code.soundsoftware.ac.uk/attachments/download/690/vamp-plugin-sdk-2.5.tar.gz'
    dependencies = ['libsndfile']

