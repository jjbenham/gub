from gub import tools

class M4__tools (tools.AutoBuild):
    source = 'http://ftp.gnu.org/gnu/m4/m4-1.4.16.tar.xz'
    config_cache_overrides = tools.AutoBuild.config_cache_overrides + '''
gl_cv_lib_sigsegv=${gl_cv_lib_sigsegv=no}
'''
    def config_cache_settings (self):
        # tools return '' by default, to allow MI
        return self.config_cache_overrides
    configure_variables = (tools.AutoBuild.configure_variables
                           + ' CFLAGS=" -std=gnu89" ')


