''''''

# Standard
import logging
# Related
import wsgiref.handlers
import google.appengine.ext.webapp
# Local
import core.handlers


def execute_app():
    application = google.appengine.ext.webapp.WSGIApplication(
        [
            # Grab the page with no arguments.
            (r'/', core.handlers.PageHandler),
            # Grab the page with any arguments given.
            (r'/(.+)', core.handlers.PageHandler),
            
            (r'/install', core.handlers.InstallHandler),
            (r'/install(.+)', core.handlers.InstallHandler),
            
            (r'/update', core.handlers.UnhandledHandler),
            (r'/update(.+)', core.handlers.UnhandledHandler),
            
            (r'/json', core.handlers.UnhandledHandler),
            (r'/json(.+)', core.handlers.UnhandledHandler),
            
            (r'/feed', core.handlers.UnhandledHandler),
            (r'/feed(.+)', core.handlers.UnhandledHandler),
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

