''''''

# Standard
import logging
from sys import path
from os.path import abspath
# Related
import wsgiref.handlers
import google.appengine.ext.webapp
# Local
import core.handler


# Later in development, this will be renamed to main() for caching.
# Currently it is not main() so that it can be profiled on every load.
def execute_app():
    # Append the external libraries to the python path
    path.append(abspath('external_lib'))

    application = google.appengine.ext.webapp.WSGIApplication(
        [
            (r'/install', core.handler.InstallHandler),
            (r'/install/(.+)', core.handler.InstallHandler),

            (r'/update', core.handler.UnhandledHandler),
            (r'/update/(.+)', core.handler.UnhandledHandler),

            (r'/json', core.handler.UnhandledHandler),
            (r'/json/(.+)', core.handler.UnhandledHandler),

            (r'/feed', core.handler.UnhandledHandler),
            (r'/feed/(.+)', core.handler.UnhandledHandler),

            (r'/dev_utils', core.handler.DevUtils),
            (r'/dev_utils/(.+)', core.handler.DevUtils),

            # Grab the page with no arguments.
            (r'/', core.handler.PageHandler),
            # Grab the page with any arguments given.
            (r'/(.+)', core.handler.PageHandler),
            ],
        debug=True
    )
    wsgiref.handlers.CGIHandler().run(application)

def profile_app():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    import cProfile, pstats
    prof = cProfile.Profile()
    prof = prof.runctx('execute_app()', globals(), locals())
    print '<pre>'
    stats = pstats.Stats(prof)
    stats.sort_stats('cumulative')
    stats.print_stats('rocketseat/core|rocketseat/user', 200)
    print '</pre>'

if __name__ == '__main__':
    profile_app()

