''''''

# standard
import sys
import logging
# related
import google.appengine.ext.webapp
# local
import core.instance_data


class PageHandler(google.appengine.ext.\
                  webapp.RequestHandler):
    ''''''


    def get(self, uri_arguments=None):
        # Create Instance Data
        page_data = core.instance_data.PageInstanceData(
            self, 'get', uri_arguments)

        try:
            maintenance = page_data.rocketseat_models['site'].maintenance
        except:
            # Rocket Seat is not installed, show install information by
            # creating the instance handler, and passing off this request to it
            install_handler = InstallHandler()
            install_handler.get(uri_arguments)
        else:
            if not maintenance:
                # Rocket Seat is not set to maintenance mode, continue normally.
                pass
            else:
                # Rocket Seat is down for maintenance, display maintenance page.
                pass

    def post(self, uri_arguments=None):
        pass

class InstallHandler(google.appengine.ext.\
                     webapp.RequestHandler):
    ''''''


    def get(self, uri_arguments=None):
        # Create Instance Data
        page_data = core.instance_data.PageInstanceData(
            self, 'get', uri_arguments)
        
        if uri_arguments is not None and \
           page_data.uri_arguments[0].lower() == 'install':
            pass
        else:
            pass

    def post(self, uri_arguments=None):
        pass

class UnhandledHandler(google.appengine.ext.\
                       webapp.RequestHandler):
    '''Isn't this an oxymoron?'''


    def get(self, uri_arguments=None):
        pass

    def post(self, uri_arguments=None):
        pass
