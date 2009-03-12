''''''

# Standard
from os import path, system
from optparse import OptionParser
# Related
# Local

class UploadAppException(Exception):
    ''''''
    pass

class MissingAppNameException(UploadAppException):
    ''''''
    pass

def main():
    '''
    '''
    
    # Create the parser
    parser = OptionParser()
    
    # Add the options
    parser.add_option('-v', '--verbose',
                      action='store_false', dest='verbose', default=True,
                      help='Be verbose.')
    
    parser.add_option('-n', '--name', dest='appname',
                  help='The app name, as shown in your google appengine '+
                  'account')
    
    # Grab the arguments and commands from the parser.
    (options, args,) = parser.parse_args()
    
    rocketseat_path = path.abspath('./rocketseat')
    
    if options.appname is None:
        raise MissingAppNameException()
    
    
    
if __name__ == '__main__':
    try:
        main()
    except MissingAppNameException:
        print 'Error: The -n flag must be supplied. See --help for information'
