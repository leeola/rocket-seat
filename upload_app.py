'''

Note: This module is hacked together heh. If it grows at all, it should be 
rewritten to be.. readable.
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

class InvalidGAEPathError(UploadAppError):
    ''''''
    pass

class UploadAppCLIError(Exception):
    ''''''
    pass

class MissingAppNameError(UploadAppCLIException):
    ''''''
    pass

class MissingAppEngineLibraryError(UploadAppCLIException):
    ''''''
    pass

class NoSettingsFileError(UploadAppCLIException):
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
        if os.path.exists('.upload_app_cfg'):
            raise NoSettingsFileError()
        
        file_object = open('.upload_app_cfg', 'w')
        cPickle.dump(self.settings, file_object)
        file_object.close()
    
    def parse_arguments(self):
        '''
        '''
        (self.option_results, self.parser_arguments,) = parser.parse_args()
        
        if self.option_results['gae_sdk_path']:
            self.settings['gae_sdk_path'] = self.option_results['gae_sdk_path']
        
        if self.option_results['app_name']:
            self.settings['app_name'] = self.option_results['app_name']
        
        if self.option_results['verbose']:
            self.settings['verbose'] = self.option_results['verbose']
        
        if self.option_results['save_settings']:
            self.save_settings_to_file()
        
        if self.settings['gae_sdk_path'] is None:
            raise MissingAppEngineLibraryError()
        
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

    def __init__(self, app_name, gae_sdk_path, verbose=False):
        super(UploadApp, self).__init__()
        
        self.app_name = app_name
        self.gae_sdk_path = gae_sdk_path
        self.verbose = verbose
        
        try:
            import google
        except ImportError:
            raise InvalidGAEPathError()

    def upload_app(self):
        pass

if __name__ == '__main__':
    app_uploader_cli = AppUploaderCLI()
    
    try:
        app_uploader_cli.parse_arguments()
    except MissingAppNameError:
        print 'Error: The -n flag must be supplied. See --help for information'
    except MissingAppEngineLibraryError:
        print 'Error: The -g flag must be supplied. See --help for informaton'
    
    try:
        app_uploader = AppUploader(app_uploader_cli.settings['app_name'],
                                   app_uploader_cli.settings['gae_sdk_path'],
                                   app_uploader_cli.settings['verbose'])
    except InvalidGAEPathError:
        print ''''''
    
    if not app_uploader_cli.option_results['dont_upload']:
        app_uploader.upload_app()
    
