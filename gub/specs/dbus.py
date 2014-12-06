from gub import target

class Dbus (target.AutoBuild):
    source = 'http://dbus.freedesktop.org/releases/dbus/dbus-1.8.2.tar.gz'
    dependencies = ['tools::automake', 'tools::pkg-config',
                ]
    config_cache_overrides = target.AutoBuild.config_cache_overrides + '''
ac_cv_have_abstract_sockets=${ac_cv_have_abstract_sockets=yes}
'''
    configure_flags = (target.AutoBuild.configure_flags
                       + '  --with-x=yes'
		       + '  --disable-inotify'
                       )
