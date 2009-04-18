''''''

# Standard
import logging
import sys
import os
# Related
import wsgiref.handlers
import google.appengine.ext.webapp
# Local
import core.handler


def main():
    # Append the external libraries to the python path
    sys.path.append(os.path.abspath('external_lib'))
    live_server = os.environ['SERVER_SOFTWARE'].startswith('Google Apphosting/')

    def run_app():
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
            debug=not live_server
        )
        wsgiref.handlers.CGIHandler().run(application)

    if live_server:
        run_app(False)
    else:
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)

        # Enable Debugger Integration for various IDEs.
        import core.lib.ide_integration.wingide
        core.lib.ide_integration.wingide.enable_debugger_catching()

        import cProfile, pstats
        prof = cProfile.Profile()
        prof = prof.runctx('run_app()', globals(), locals())
        print '<pre>'
        stats = pstats.Stats(prof)
        stats.sort_stats('cumulative')
        stats.print_stats('rocketseat/core|rocketseat/user', 200)
        print '</pre>'

if __name__ == '__main__':
    main()
