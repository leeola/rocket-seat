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
            # Rocket Seat is not installed, show install information.
            pass
        
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
        pass

    def post(self, uri_arguments=None):
        pass

class UnhandledHandler(google.appengine.ext.\
                       webapp.RequestHandler):
    '''So wait.. how do i handle something that is unhandled?'''


    def get(self, uri_arguments=None):
        pass

    def post(self, uri_arguments=None):
        pass
