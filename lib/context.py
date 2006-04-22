import inspect
import os
import time
import sys
import subprocess
import re
import stat

def subst_method (func):
	"""Decorator to match Context.get_substitution_dict()"""
	
	func.substitute_me = True
	return func

def is_subst_method_in_class (method_name, klass):
	bs = [k for k in klass.__bases__ if is_subst_method_in_class (method_name, k)]
	if bs:
		return True
	
	if (klass.__dict__.has_key (method_name)
	    and callable (klass.__dict__[method_name])
	    and klass.__dict__[method_name].__dict__.has_key ('substitute_me')):
		return True

	return False

def typecheck_substitution_dict (d):
	for (k, v) in d.items ():
		if type (v) != type(''):
			raise 'type', (k, v)

def recurse_substitutions (d):
	for (k, v) in d.items ():
		if type(v) != type(''):
			del d[k]
			continue

		try:
			while v.index ('%(') >= 0:
				v = v % d
		except ValueError:
			pass
		d[k] = v

	return d

class Context:
	def __init__ (self, parent = None):
		self._substitution_dict = None
		self._parent = parent

	def get_constant_substitution_dict (self):
		d = {}
		if self._parent:
			d = self._parent.get_substitution_dict ()
			d = d.copy ()
			
		ms = inspect.getmembers (self)
		vars = dict((k, v) for (k, v) in ms if type (v) == type (''))
		member_substs = dict((k, v ()) for (k, v) in ms if callable (v)
				      and is_subst_method_in_class (k, self.__class__))
		
		d.update (vars)
		d.update (member_substs)

		d = recurse_substitutions (d)
		return d

	def get_substitution_dict (self, env={}):
		if  self._substitution_dict == None:
			self._substitution_dict = self.get_constant_substitution_dict ()

		d = self._substitution_dict
		if env:
			d = d.copy ()
			(d.update ((k, v % d) for (k, v) in env.items ()
				   if type (v) == type ('')))
		return d
	
	def expand (self, s, env={}):
		d = self.get_substitution_dict (env)
		return s % d

class Os_context_wrapper (Context):
	def __init__ (self, settings):
		Context.__init__ (self, settings)
		self.os_interface = settings.os_interface
		self.verbose = settings.verbose ()
		
	def file_sub (self, re_pairs, name, to_name=None, env={}, must_succeed=False):
		substs = []
		for (frm, to) in re_pairs:
			frm = self.expand (frm, env)
			if type (to) ==type(''):
				to = self.expand (to, env)

			substs.append ((frm, to))

		if to_name:
			to_name = self.expand (to_name, env)
			
		return self.os_interface.file_sub (substs, self.expand (name, env), to_name, must_succeed)
	def log_command (self, str, env={}):
		str = self.expand (str, env)
		self.os_interface.log_command (str)
		
	def read_pipe (self, cmd, env={}, ignore_error=False):
		dict = self.get_substitution_dict (env)
		return self.os_interface.read_pipe (cmd % dict, ignore_error=ignore_error)

	def system (self, cmd, env={}, ignore_error=False):
		dict = self.get_substitution_dict (env)
		cmd = self.expand (cmd, env)
		self.os_interface.system (cmd, env=dict, ignore_error=ignore_error,
					  verbose=self.verbose)

	def shadow_tree (self, src, dest):
		src = self.expand (src)
		dest = self.expand (dest)
		self.os_interface.shadow_tree (src, dest)
		
	def dump (self, str, name, mode='w', env={}):
		return self.os_interface.dump (self.expand (str, env),
			     self.expand (name, env), mode=mode)
	
	def locate_files (self, directory, pattern):
		command = "cd %(directory)s && find -name '%(pattern)s'" % locals()
		return [f for f in  self.read_pipe (command).split ('\n') if f.strip()]

if __name__=='__main__':
	class TestBase(Context):
		@subst_method
		def bladir(self):
			return 'foo'
		
	class TestClass(TestBase):
		@subst_method
		def name(self):
			return self.__class__.__name__
		
		def bladir(self):
			return 'derivedbladir'

	p = TestClass ()

	print p.expand ('%(name)s %(bladir)s')
