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

class CSSFile(object):
    '''An object L{the theme class <Theme>} can interact with more easily.
    '''
    
    
    def __init__(self, file_location, ie_only=False,
                 media='screen, projection'):
        '''
        '''
        self.file_location = file_location
        self.ie_only = ie_only
        self.media = media
    
    def render_html(self, base_theme_static_uri=None):
        '''
        @param base_theme_static_uri: If supplied, the uri for the css file
        will have this inserted before it.
        '''
        if base_theme_static_uri is not None:
            if not self.ie_only:
                return '''<link rel="stylesheet"
                href="%s/%s" type="text/css"
                media="%s" />''' % (base_theme_static_uri,
                                                self.file_location,
                                                self.media)
            else:
                return '''<!--[if IE]><link rel="stylesheet"
                href="%s/%s" type="text/css"
                media="%s" /><![endif]-->''' % (base_theme_static_uri,
                                                self.file_location,
                                                self.media)


class JSFile(object):
    '''
    '''

    def __init__(self):
        '''
        '''
        pass

class Theme(object):
    '''A class representing the instance of the loaded theme.'''


    def __init__(self, theme_script_name):
        '''
        '''
        self.theme_script_name = theme_script_name
        #self.core_event_controller = core_event_controller

        if os.path.exists('../user/themes/%s' % theme_script_name):
            self.user_theme = True
            self.theme_rel_path = '../user/themes/%s' % theme_script_name
            self.theme_py_path = 'user.themes.%s' % theme_script_name
            self.theme_static_uri = '/static/themes/user/%s' % theme_script_name
        elif os.path.exists('themes/%s' % theme_script_name):
            self.user_theme = False
            self.theme_rel_path = 'themes/%s' % theme_script_name
            self.theme_py_path = 'core.themes.%s' % theme_script_name
            self.theme_static_uri = '/static/themes/core/%s' % theme_script_name
        else:
            raise core.error.ThemeNotFoundError(theme_script_name)
        
        # Import the user theme module, and grab the settings from it.
        theme_module = __import__('%s.theme' % self.theme_py_path,
                                  fromlist=['a'])
        
        #: A list of L{css file <CSSFile>} like objects.
        self.css_files = list(theme_module.css_files)
        #: A list of L{js file <JSFile>} like objects.
        self.js_files = list(theme_module.js_files)
        
        self._rendered_css_html = None
        self._rendered_js_html = None
        self._rendered_blocks_html = ''
        
        ## Trigger the event, so other plugins can add to the css.
        #plugin_css = event_controller.call_listeners(
            #'core_p', 'add_plugin_css')
        
        self.regions = theme_module.regions
        
    
    def render(self):
        '''Render the entire page, through a cascading series of calls to
        this class and render listeners.
        '''
        
        
        
        template = mako.template.Template(
            filename='%s/base.html' % self.theme_rel_path)
        return template.render(
            base_body='Nothing',
            page_title='Rocket Seat CMS',
            site_name='Dont crash me',
            site_js='',
            site_css=self.rendered_css_html,
        )

    def add_block_content(self):
        '''
        '''
        pass
    
    def render_css_html(self):
        '''Render the html for the css files stored in this theme.
        
        @returns: A string of the rendered css links, eg:
        	<link rel="stylesheet" 
                href="/static/themes/core/usability/css/style.css"
                type="text/css" media="screen, projection" />
        
        '''
        # Store it locally for speed.
        theme_static_uri = self.theme_static_uri
        
        def render_css(css_file):
            return css_file.render_html(base_theme_static_uri=theme_static_uri)
        
        rendered_css_list = map(render_css, self.css_files)
        return ''.join(rendered_css_list)
    
    def render_js_html(self):
        '''
        '''
        pass
    
    def _get_rendered_css_html(self):
        '''Get self._rendered_css_html.
        '''
        if self._rendered_css_html is None:
            self._rendered_css_html = self.render_css_html()
        return self._rendered_css_html
    
    rendered_css_html = property(_get_rendered_css_html)
    
    def _get_rendered_js_html(self):
        '''Get self._rendered_js_html.
        '''
        if self._rendered_js_html is None:
            self._rendered_js_html = self.render_js_html()
        return self._rendered_js_html
    
    rendered_js_html = property(_get_rendered_js_html)
    
    
