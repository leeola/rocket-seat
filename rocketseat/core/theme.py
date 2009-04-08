''''''


# Standard
import os.path
# Related
import mako.template
# Local
import core.error


def find_theme_abs_path(theme_script_name):
    '''Find the themes absolute path, as found by os.path.abspath()

    @param theme_script_name: The script name of the theme.
    '''
    if os.path.exists('../user/themes/%s' % theme_script_name):
        return os.path.abspath('../themes/%s' % theme_script_name)
    elif os.path.exists('themes/%s' % theme_script_name):
        return os.path.abspath('themes/%s' % theme_script_name)
    else:
        raise core.error.ThemeNotFoundError(theme_script_name)

def find_theme_rel_path(theme_script_name):
    '''Find the themes relative path

    @param theme_script_name: The script name of the theme.
    '''
    if os.path.exists('../user/themes/%s' % theme_script_name):
        return '../themes/%s' % theme_script_name
    elif os.path.exists('themes/%s' % theme_script_name):
        return 'themes/%s' % theme_script_name
    else:
        raise core.error.ThemeNotFoundError(theme_script_name)

class Theme(object):
    '''A class representing the instance of the loaded theme.'''


    def __init__(self, theme_script_name):
        '''
        '''
        self.theme_script_name = theme_script_name
        
        if os.path.exists('../user/themes/%s' % theme_script_name):
            self.user_theme = True
            self.theme_abs_path = os.path.abspath(
                '../user/themes/%s' % theme_script_name)
        elif os.path.exists('themes/%s' % theme_script_name):
            self.user_theme = False
            self.theme_abs_path = os.path.abspath(
                'themes/%s' % theme_script_name)
        else:
            raise core.error.ThemeNotFoundError(theme_script_name)
        
        self.cache_abs_path = os.path.abspath(
            'template_cache')
        print self.cache_abs_path
    
    def render(self):
        '''
        '''
        mytemplate = mako.template.Template(
            filename='%s/base.html' % self.theme_abs_path,
            module_directory=self.cache_abs_path)
        return mytemplate.render()
