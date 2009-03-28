'''
'''

# Standard
import os
import sys
import optparse
import re
import cPickle
# Related
# Local

class UploadAppError(Exception):
    ''''''
    pass

class UploadAppCLIError(Exception):
    ''''''
    pass

class MissingAppNameError(UploadAppCLIError):
    ''''''
    pass

class MissingAppEngineLibraryError(UploadAppCLIError):
    ''''''
    pass

class NoSettingsFileError(UploadAppCLIError):
    ''''''
    pass

class AppUploaderCLI(object):
    '''
    '''

    def __init__(self):
        '''
        '''
        # Load Saved Settings
        if os.path.exists('.upload_app_cfg'):
            self.load_settings_file()
        else:
            self.create_default_settings()

        # Create the parser 
        self.argument_parser = optparse.OptionParser()

        # Add the options
        self.argument_parser.add_option(
            '-v', '--verbose', action='store_true', dest='verbose', 
            default=False, help='Be verbose.')

        self.argument_parser.add_option(
            '-n', '--name', dest='app_name', help='''The app name, as shown in
            your google appengine account''')

        self.argument_parser.add_option(
            '-g', '--gae', dest='gae_sdk_path', help='''The location of a GAE
            SDK installation.''')

        self.argument_parser.add_option(
            '-s', '--save', action='store_true', dest='save_settings', 
            default=False, help='''Save the settings of this cli to a settings
            file (.upload_app_cfg).''')

        self.argument_parser.add_option(
            '-d', '--dont_upload', action='store_true', dest='dont_upload', 
            default=False, help='''Do not upload the app. This is useful for
            simply assigning saved settings, without uploading the app.''')

    def create_default_settings(self):
        '''
        '''
        self.settings = {
            'gae_sdk_path':None,
            'app_name':None,
            'verbose':False,
        }

    def load_settings_file(self):
        '''
        '''
        if not os.path.exists('.upload_app_cfg'):
            raise NoSettingsFileError()

        file_object = open('.upload_app_cfg', 'r')
        self.settings = cPickle.load(file_object)
        file_object.close()

    def parse_arguments(self):
        '''
        '''
        (self.option_results, 
         self.parser_arguments,) = self.argument_parser.parse_args()

        if self.option_results.gae_sdk_path:
            self.settings['gae_sdk_path'] = os.path.abspath(
                self.option_results.gae_sdk_path)

        if self.option_results.app_name:
            self.settings['app_name'] = self.option_results.app_name

        if self.option_results.verbose:
            self.settings['verbose'] = self.option_results.verbose

        if self.option_results.save_settings:
            self.save_settings_to_file()

        if self.settings['app_name'] is None:
            raise MissingAppNameError()


    def save_settings_to_file(self):
        '''
        '''
        # pickle the settings dict to the .upload_app_cfg file.
        file_object = open('.upload_app_cfg', 'w')
        cPickle.dump(self.settings, file_object)
        file_object.close()


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
        rocketseat_path = os.path.abspath('./rocketseat')

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
                'python %s/appcfg.py update rocketseat/' % appengine_dev_path)
        except:
            pass
        
        # Return the appname to the default rocketseat, so it can be replaced 
        # next time. (And so there are no changes to the core)
        write_file = open('%s/app.yaml' % rocketseat_path,'w')
        write_file.write(re.sub(self.app_name, 'rocketseat', read_file) )
        write_file.close()

def main():
    app_uploader_cli = AppUploaderCLI()

    try:
        app_uploader_cli.parse_arguments()
    except MissingAppNameError:
        print 'Error: The -n flag must be supplied. See --help for information'
        return

    try:
        app_uploader = AppUploader(app_uploader_cli.settings['app_name'],
                                   app_uploader_cli.settings['gae_sdk_path'],
                                   app_uploader_cli.settings['verbose'])
    except MissingAppEngineLibraryError:
        print '''The AppEngine SDK cannot be found. If it is installed, please
        supply the path to the -g argument.'''
    else:
        if not app_uploader_cli.option_results.dont_upload:
            app_uploader.upload_app()

if __name__ == '__main__':
    main()
