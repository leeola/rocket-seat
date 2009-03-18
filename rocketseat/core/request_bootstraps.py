'''The request bootstrap objects are responsible for collecting information 
that is used on every page load, by nearly all plugins.'''

# standard
import logging
import exceptions
# related
# local
import core.models
import core.errors

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
        
        self.request_handler = request_handler

class InstalledRequestBootstrap(RequestBootstrap):
    '''The bootstrap with generic config data. This requires an installation.
    '''

    def __init__(self, request_handler, request_method, uri_arguments):
        '''
        '''
        super(InstalledRequestBootstrap, self).__init__(
            request_handler, request_method, uri_arguments)
        
        self._rs_config_ent = core.models.RocketSeatConfig.get_by_key_name(
            'core_site')
        self._core_hooks_ent = core.models.CoreHooks.get_by_key_name(
            'core_hooks')
        
        ##try:
            ##self.undergoing_maintenance = self._rs_config_ent[
                ##'core_site'].undergoing_maintenance
        ##except exceptions.TypeError:
            ##raise core.errors.NotInstalledError()
        
        # Fake a value, removeme
        self.undergoing_maintenance = False
        

class PageRequestBootstrap(InstalledRequestBootstrap):
    '''The bootstrap from a page request.'''

    def __init__(self, request_handler, request_method, uri_arguments):
        '''
        '''
        super(PageRequestBootstrap, self).__init__(
            request_handler, request_method, uri_arguments)
        
        ##try:
            ##self.active_theme = self._rs_config_ent['core_site'].active_theme
        ##except exceptions.TypeError:
            ##raise core.errors.NotInstalledError()
        
        # Fake a value, removeme
        self.active_theme = 'core.themes.raw'
        

