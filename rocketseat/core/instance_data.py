'''The instance data objects are responsible for collecting information that
is used on every page load, by nearly all plugins.'''

# standard
import logging
# related
# local
import core.models


class PageInstanceData(object):
    ''''''

    def __init__(self, request_handler, request_method, uri_arguments):
        '''
        '''
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
        
        # Load the basic Rocket Seat Models
        self.rocketseat_models = {
            'site':core.models.SiteModel.get_by_key_name('core_site'),
            'hooks':core.models.CoreHooks.get_by_key_name('core_hooks'),
        }
        
        logging.debug('Models: %s' % str(self.rocketseat_models))

