''''''


# Standard
import sys
import logging
# Related
# Local




def enable_debugger_catching():
    '''To allow WingIDE to catch rocketseat exceptions, run this function.
    '''
    
    logging.root.addHandler(WingIDEDebuggerExceptionHandler(
        level=logging.ERROR))

class WingIDEDebuggerExceptionHandler(logging.Handler):
    '''This class is an overload to the Logging Handler which enables WingIDE
    to catch the exception instead of displaying it to the clients browser.
    '''


    def filter(self, record):
        '''Only interested if exc_info is set.
        '''

        return (record.exc_info is not None)


    def emit(self, record):
        '''Call the except hook with the record's exception.
        '''

        try:
            etype, value, tb = record.exc_info
        except:
            return

        sys.excepthook(etype, value, tb)
