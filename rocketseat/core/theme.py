''''''


# Standard
import os.path
# Related
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
        if os.path.exists('../user/themes/%s' % theme_script_name):
            self.user_theme = True
        elif os.path.exists('themes/%s' % theme_script_name):
            self.user_theme = False
        else:
            raise core.error.ThemeNotFoundError(theme_script_name)
        
    
    def get_uri(self):
        '''Return the uri of this theme.'''
        if self.user_theme:
            return '/user/themes/%s/' % self.script_name
        else:
            return '/core/themes/%s/' % self.script_name
