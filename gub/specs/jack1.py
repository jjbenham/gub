from gub import target

class Jack1 (target.AutoBuild):
    source = 'http://jackaudio.org/downloads/jack-audio-connection-kit-0.124.1.tar.gz'
    #patches = ['jack-1.9.10.ppoll.patch']
    dependencies = ['tools::automake', 'tools::pkg-config', 'portaudio', 'alsa', 'e2fsprogs', 'db']
    configure_variables = (target.AutoBuild.configure_variables
                           + ' CFLAGS="-D_GNU_SOURCE" ')
 
