'''The request bootstrap objects are responsible for collecting information 
that is used on every page load, by nearly all plugins.'''

# standard
from exceptions import TypeError
# related
# local
import core.error
import core.model
import core.plugin
import core.theme

class RequestBootstrap(object):
    '''The base request bootstrap. No installation is needed at this level.'''
    
    def __init__(self, request_handler, request_method, uri_arguments):
        '''
        '''
        super(RequestBootstrap, self).__init__(
            request_handler, request_method, uri_arguments)
        
        if uri_arguments is None:
            self.uri_arguments = uri_arguments
        else:
            self.uri_arguments = uri_arguments.split('/')
        
        self.request_method = request_method
        if request_method == 'post':
            self.post_data = request_handler.request.params
        else:
            self.post_data = None
        
        # This is commented out due to it not having the ability to be cached
        # in memcache. I am waiting to re-implement this until its usage
        # can more accurately be determined.
        #self.request_handler = request_handler
    
    def shutdown(self):
        '''Close or Save any objects held within the bootstrap object that
        cannot be stored (Pickled) inside of memcache.
        
        @see: startup
        '''
        pass
    
    def startup(self):
        '''This is called when the bootstrap object is brought out of memcache.
        This allows the bootstrap to take in, or create, and objects needed
        but were not stored on the memcache. Eg: the ones which were
        shut down.
        '''
        pass

class NotInstalledRequestBootstrap(RequestBootstrap):
    '''The bootstrap with generic config data required to run the installation.
    '''
    
    def __init__(self, request_handler, request_method, uri_arguments):
        '''
        '''
        super(NotInstalledRequestBootstrap, self).__init__(
            request_handler, request_method, uri_arguments)
        
        # Fake a value, removeme
        self.active_theme = 'core.themes.usability'

class InstalledRequestBootstrap(RequestBootstrap):
    '''The bootstrap with generic config data. This requires an installation.
    '''

    def __init__(self, request_handler, request_method, uri_arguments):
        '''
        '''
        super(InstalledRequestBootstrap, self).__init__(
            request_handler, request_method, uri_arguments)
        
        self.rs_config_ent = core.model.RocketSeatConfig.get_by_key_name(
            'core_site')
        self.core_events_ent = core.model.CoreEvents.get_by_key_name(
            'core_events')
        
        ##try:
            ##self.undergoing_maintenance = self._rs_config_ent[
                ##'core_site'].undergoing_maintenance
        ##except TypeError:
            ##raise core.error.NotInstalledError()
        
        # Fake values, removeme
        self.undergoing_maintenance = False
        self.enabled_plugin_paths = (
            'core.plugins.block_spammer',
        )
        
        self.plugins = core.plugin.initialize_plugins(
            self)

class PageRequestBootstrap(InstalledRequestBootstrap):
    '''The bootstrap from a page request.'''

    def __init__(self, request_handler, request_method, uri_arguments):
        '''
        '''
        super(PageRequestBootstrap, self).__init__(
            request_handler, request_method, uri_arguments)
        
        ##try:
            ##self.active_theme = self._rs_config_ent['core_site'].active_theme
        ##except TypeError:
            ##raise core.error.NotInstalledError()
        
        # Fake a value, removeme
        self.theme_script_name = 'usability'
        
        self.theme = core.theme.Theme(self.theme_script_name)
