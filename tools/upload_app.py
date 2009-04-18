'''The upload app is a basic wrapper for the standard SDK uploader. It provides
a means to save settings (such as appname, and sdk path), and in the future
will ensure the upload destination is ready to recieve a newer version of
Rocket Seat. (Eg, assuring that pickled objects in memcache are removed, etc.)
'''

# Standard
import os
import sys
import optparse
import cPickle
# Related
# Local
import lib.upload

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

def main():
    app_uploader_cli = AppUploaderCLI()

    try:
        app_uploader_cli.parse_arguments()
    except MissingAppNameError:
        print 'Error: The -n flag must be supplied. See --help for information'
        return

    try:
        app_uploader = lib.upload.AppUploader(
            app_uploader_cli.settings['app_name'],
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
