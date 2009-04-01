''''''

# Standard
# Related
# Local


def initialize_plugins(bootstrap):
    '''Initialize all of the plugins that are enabled.

    Returns: A dict of key:value pairs in the form of 
    plugin_script_name:plugin.
    
    Todo: Optimize this.
    '''

    plugin_paths = bootstrap.enabled_plugin_paths
    
    def import_and_init(plugin_path):
        # Import the plugin module from the plugin path
        plugin_module = __import__(plugin_path+'.plugin',
                                   fromlist=['a'])

        # Return the plugin scriptname and an instance of the plugin
        # as key value pairs.
        plugin = plugin_module.Plugin(bootstrap)  
        return (plugin.script_name, plugin)

    return dict(map(import_and_init, plugin_paths))

class Plugin(object):
    '''The plugin base class.'''


    def __init__(self, bootstrap, *args, **kwargs):
        ''''''
        super(Plugin, self).__init__(*args, **kwargs)

        self.bootstrap = bootstrap
        self.listeners = None

class PluginListeners(object):
    ''''''


    def __init__(self, plugin, bootstrap, *args, **kwargs):
        ''''''
        super(PluginListeners, self).__init__(*args, **kwargs)

        self.plugin = plugin
        self.bootstrap = bootstrap

