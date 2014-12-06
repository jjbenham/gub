from gub import target

class Jack (target.WafBuild):
    source = 'https://dl.dropboxusercontent.com/u/28869550/jack-1.9.10.tar.bz2'
    patches = ['jack-1.9.10.ppoll.patch']
    dependencies = ['tools::automake', 'tools::pkg-config','dbus', 'portaudio', 'alsa']
 
