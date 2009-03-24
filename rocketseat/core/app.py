''''''

# Standard
import logging
# Related
import wsgiref.handlers
import google.appengine.ext.webapp
# Local
import core.handler


def execute_app():
    application = google.appengine.ext.webapp.WSGIApplication(
        [
            # Grab the page with no arguments.
            (r'/', core.handler.PageHandler),
            # Grab the page with any arguments given.
            (r'/(.+)', core.handler.PageHandler),
            
            (r'/install', core.handler.InstallHandler),
            (r'/install(.+)', core.handler.InstallHandler),
            
            (r'/update', core.handler.UnhandledHandler),
            (r'/update(.+)', core.handler.UnhandledHandler),
            
            (r'/json', core.handler.UnhandledHandler),
            (r'/json(.+)', core.handler.UnhandledHandler),
            
            (r'/feed', core.handler.UnhandledHandler),
            (r'/feed(.+)', core.handler.UnhandledHandler),
            ],
        debug=True
        )
    wsgiref.handlers.CGIHandler().run(application)

def profile_app():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    
    import cProfile, pstats
    prof = cProfile.Profile()
    prof = prof.runctx("execute_app()", globals(), locals())
    print "<pre>"
    stats = pstats.Stats(prof)
    #stats.sort_stats("time")
    stats.sort_stats("cumulative")
    stats.print_stats('rocketseat', 200)
    print "</pre>"

if __name__ == "__main__":
    profile_app()

