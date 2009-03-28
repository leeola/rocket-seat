''''''

# standard
# related
import google.appengine.ext.webapp
from google.appengine.api import memcache
# local
import core.error
import core.request_bootstrap


class PageHandler(google.appengine.ext.\
                  webapp.RequestHandler):
    ''''''

    def get(self, uri_arguments=None):
        '''
        '''
        # Grab the data from the cache
        page_bootstrap = memcache.get('page_bootstrap')
        
        try:
            # Create Bootstrap Data
            if page_bootstrap is None:
                page_bootstrap = core.request_bootstrap.PageRequestBootstrap(
                    self, 'get', uri_arguments)
                memcache.add('page_bootstrap', page_bootstrap, 60)
            
        except core.error.NotInstalledError:
            # Rocket Seat is not installed, show install information by
            # creating the instance handler, and passing off this request to it
            install_handler = InstallHandler()
            install_handler.get(uri_arguments)
        else:
            if not page_bootstrap.undergoing_maintenance:
                # Rocket Seat is not undergoing maintenance, continue normally.
                
                page_bootstrap.plugin_manager.hook_plugins(
                    'core_p', 'bootstrap_finished'
                )
            else:
                # Rocket Seat is down for maintenance, display maintenance page.
                pass

    def post(self, uri_arguments=None):
        '''
        '''
        pass

class InstallHandler(google.appengine.ext.\
                     webapp.RequestHandler):
    ''''''

    def get(self, uri_arguments=None):
        '''
        '''
        # Create Bootstrap, compatible with no RS installation.
        bootstrap = core.request_bootstrap.RequestBootstrap(
            self, 'get', uri_arguments)
        
        if uri_arguments is not None and \
           bootstrap.uri_arguments[0].lower() == 'install':
            pass
        else:
            pass

    def post(self, uri_arguments=None):
        '''
        '''
        pass

class UnhandledHandler(google.appengine.ext.\
                       webapp.RequestHandler):
    '''Isn't this an oxymoron?'''

    def get(self, uri_arguments=None):
        '''
        '''
        pass

    def post(self, uri_arguments=None):
        '''
        '''
        pass

class DevUtils(google.appengine.ext.\
                       webapp.RequestHandler):
    '''This is a temporary solution to implement some simple dev actions, such
    as removing the cache manually, etc.'''

    def get(self, uri_arguments=None):
        '''
        '''
        uri_arguments = uri_arguments.split('/')
        
        if uri_arguments is None:
            return
        
        if uri_arguments[0] == 'empty_memcache':
            memcache.delete('page_bootstrap')

    def post(self, uri_arguments=None):
        '''
        '''
        pass
