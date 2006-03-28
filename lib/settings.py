import os
import re
import oslog

import gub

from context import *

platforms = {
	'arm': 'arm-linux',
	'cygwin': 'i686-cygwin',
	'darwin-ppc': 'powerpc-apple-darwin7',
	'darwin-x86': 'i686-apple-darwin8',
	'debian': 'i686-linux',
	'freebsd': 'i686-freebsd4',
	'linux': 'i686-linux',
	'local': 'local',
	'mingw': 'i686-mingw32',
}

distros = ('cygwin', 'debian')
			
class Settings (Context):
	def __init__ (self, platform):
		Context.__init__ (self)
		self.platform = platform
		self.target_architecture = platforms[self.platform]

		self.is_distro = platform in distros

		self.target_gcc_flags = '' 
		self.topdir = os.getcwd ()
		self.logdir = self.topdir + '/log'
		self.downloaddir = self.topdir + '/downloads'
		self.patchdir = self.topdir + '/patches'
		self.sourcefiledir = self.topdir + '/sourcefiles'
		self.specdir = self.topdir + '/specs'
		self.nsisdir = self.topdir + '/nsis'
		self.gtk_version = '2.8'

		self.tool_prefix = self.target_architecture + '-'
		self.targetdir = self.topdir + '/target/' + self.platform

		## Patches are architecture dependent, 
		## so to ensure reproducibility, we unpack for each
		## architecture separately.
		self.allsrcdir = os.path.join (self.targetdir, 'src')
		
		self.allbuilddir = self.targetdir + '/build'
		self.statusdir = self.targetdir + '/status'

		## Safe uploads, so that we can rm -rf target/*
		## and still cheaply construct a (partly) system root
		## from .gub packages.
		self.uploads = self.topdir + '/uploads'
		#self.gub_uploads = self.uploads + '/gub'
		self.gub_uploads = self.uploads + '/' + self.platform
		self.gub_cross_uploads = '%s/%s-cross' % (self.uploads, self.platform)

		self.distcc_hosts = ''
		# FIXME: rename to target_root?
		self.system_root = self.targetdir + '/system'
		self.crossprefix = self.system_root + '/usr/cross'
		self.installdir = self.targetdir + '/install'
		self.buildtools = self.topdir + '/target/local/system/usr/'
		self.cross_distcc_bindir = self.topdir + '/target/cross-distcc/bin/'
		self.native_distcc_bindir = self.topdir + '/target/native-distcc/bin/'
		
		# INSTALLERS
		self.installer_root = self.targetdir + '/installer'
		self.installer_db = self.targetdir + '/installerdb'
		##self.installer_uploads = self.targetdir + '/uploads'
		self.installer_uploads = self.uploads
		self.bundle_version = None
		self.bundle_build = None
		self.package_arch = re.sub ('-.*', '', self.target_architecture)
		self.package_arch = re.sub ('i[0-9]86', 'i386', self.package_arch)
		
		self.keep_build = False
		self.use_tools = False
		self.build_autopackage = self.allbuilddir + '/autopackage'

		if not os.path.isdir ('log'):
			os.mkdir ('log')
			
		self.os_interface = oslog.Os_commands ('log/build-%s.log'
						       % self.target_architecture)
		self.create_dirs ()
		self.build_architecture = self.os_interface.read_pipe ('gcc -dumpmachine',
							 silent=True)[:-1]

		
	def verbose (self):
		try:
			return self.options.verbose
		except AttributeError:
			return False
	
 	def create_dirs (self): 
		for a in (
			'downloaddir',
			'logdir',
			'gub_uploads',
			'gub_cross_uploads',
			'installer_uploads',
			'specdir',
			'allsrcdir',
			'statusdir',
			'system_root',
			'crossprefix',
			'targetdir',
			'buildtools',
			'topdir',
			):
			dir = self.__dict__[a]
			if os.path.isdir (dir):
				continue

			self.os_interface.system ('mkdir -p %s' % dir)

