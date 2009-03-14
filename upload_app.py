''''''

# Standard
import os
import sys
import optparse
import re
# Related
# Local

class UploadAppException(Exception):
    ''''''
    pass

class MissingAppNameException(UploadAppException):
    ''''''
    pass

class MissingAppEngineLibrary(UploadAppException):
    ''''''
    pass

def main():
    '''
    '''
    
    # Create the parser
    parser = optparse.OptionParser()
    
    # Add the options
    parser.add_option('-v', '--verbose',
                      action='store_false', dest='verbose', default=True,
                      help='Be verbose.')
    
    parser.add_option('-n', '--name', dest='appname',
                  help='The app name, as shown in your google appengine '+
                  'account')
    
    parser.add_option('-g', '--gae', dest='gae_location',
                  help='The location of a GAE SDK installation.')
    
    # Grab the arguments and commands from the parser.
    (options, args,) = parser.parse_args()
    
    # Grab the rocketseat dir, as relative to this file.
    rocketseat_path = os.path.abspath('./rocketseat')
    
    if options.gae_location is not None:
        sys.path.append(options.gae_location)
    
    try:
        import google
    except ImportError:
        raise MissingAppEngineLibrary()
    
    # Grab the directory of the appengine library, so appcfg.py can be run.
    appengine_dev_path = google.__file__.replace('/google/__init__.pyc', '')
    
    if options.appname is None:
        raise MissingAppNameException()
    
    # Read the file
    read_file = open('%s/app.yaml' % rocketseat_path).read()
    
    # Open a writable object of the file
    write_file = open('%s/app.yaml' % rocketseat_path,'w')
    
    # Replace the default rocketseat with the users appname
    write_file.write( re.sub('rocketseat', options.appname, read_file)  )
    write_file.close()
    
    # Upload the app
    os.system('python %s/appcfg.py update rocketseat/' % appengine_dev_path)
    
    # Return the appname to the default rocketseat, so it can be replaced next
    # time.
    write_file = open('%s/app.yaml' % rocketseat_path,'w')
    write_file.write( re.sub(options.appname, 'rocketseat', read_file)  )
    write_file.close()
    
if __name__ == '__main__':
    try:
        main()
    except MissingAppNameException:
        print 'Error: The -n flag must be supplied. See --help for information'
    except MissingAppEngineLibrary:
        print '''Error: Cannot find the Google AppEngine SDK. Either install
        it or if it indeed exists on disk, give the location of the sdk 
        in the form of the -g option. See --help for more details.'''
