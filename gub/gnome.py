from gub import misc

#VERSION='2.25.5'
#VERSION='2.26.3'
#VERSION='2.26.3'
VERSION='2.32.1'

def platform_url (name, version=VERSION):
    major, minor, micro = version.split ('.')
    url = 'http://ftp.gnome.org/pub/GNOME/platform/%(major)s.%(minor)s/%(version)s/sources/' % locals ()
    raw_version_file = 'gnome-%(version)s.index' % locals ()
    return misc.latest_url (url, name, raw_version_file)
