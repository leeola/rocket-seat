''''''

# Standard
# Related
# Local


class UploadAppError(Exception):
    ''''''
    pass

class AppUploader(object):

    def __init__(self, app_name, gae_sdk_path=None, verbose=False):
        '''
        '''
        super(AppUploader, self).__init__()

        self.app_name = app_name
        self.gae_sdk_path = gae_sdk_path
        self.verbose = verbose
        
        if gae_sdk_path is not None:
            sys.path.append(gae_sdk_path)
        
        try:
            import google
        except ImportError:
            raise MissingAppEngineLibraryError()

    def upload_app(self):
        '''
        '''
        
        # Grab the rocketseat dir, as relative to this file.
        rocketseat_path = os.path.abspath('../../rocketseat')

        # Read the file
        read_file = open('%s/app.yaml' % rocketseat_path).read()

        # Open a writable object of the file
        write_file = open('%s/app.yaml' % rocketseat_path,'w')

        # Replace the default rocketseat with the users appname
        write_file.write(re.sub('rocketseat', self.app_name, read_file) )
        write_file.close()
        
        import google
        # Grab the directory of the appengine library, so appcfg.py can be run.
        appengine_dev_path = google.__file__.replace(
            '/google/__init__.pyc', '')
        
        # Catch any errors raised by appcfg.py, so that here we can restore
        # app.yaml to what it was.
        try:
            # Upload the app
            os.system(
                'python %s/appcfg.py update ../../rocketseat/' % appengine_dev_path)
        except:
            pass
        
        # Return the appname to the default rocketseat, so it can be replaced 
        # next time. (And so there are no changes to the core)
        write_file = open('%s/app.yaml' % rocketseat_path,'w')
        write_file.write(re.sub(self.app_name, 'rocketseat', read_file) )
        write_file.close()
