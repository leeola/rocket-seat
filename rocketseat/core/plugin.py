''''''

# Standard
# Related
# Local


class PluginManager(object):
    '''This manages each plugin instances.'''
    
    def __init__(self, bootstrap):
        ''''''
        
        if 0:
            from core.request_bootstrap import InstalledRequestBootstrap
            assert isinstance(bootstrap, InstalledRequestBootstrap)
        
        self.bootstrap = bootstrap
        
        self.init_plugins()
    
    def init_plugins(self):
        '''Initialize all of the plugins that are enabled.
        
        Todo: Optimize this.
        '''
        bootstrap = self.bootstrap
        
        # Grab the enabled plugin module paths.
        enabled_plugin_paths = bootstrap.enabled_plugin_paths
        
        def import_and_init(plugin_path):
            # Import the plugin module from the plugin path
            plugin_module = __import__(plugin_path+'.plugin',
                                       fromlist=['a'])
            
            # Return an instance of the plugin
            return plugin_module.Plugin(bootstrap)    
        
        self.enabled_plugins = map(import_and_init, enabled_plugin_paths)
    
    def hook_plugins(self, owner, hook, callback=None, **kwargs):
        '''
        '''
        # Store it locally for efficiency
        enabled_plugins = self.enabled_plugins
        
        # Include the owner of the hook, in the hook string.
        hook = owner+'__'+hook
        
        def hook_a_plugin(plugin):
            return getattr(plugin.events, hook)(callback, **kwargs)
        
        map(hook_a_plugin, enabled_plugins)

class PluginEvents(object):
    ''''''
    
    
    def __init__(self, bootstrap, *args, **kwargs):
        ''''''
        super(PluginEvents, self).__init__(*args, **kwargs)
        
        self.bootstrap = bootstrap

class Plugin(object):
    '''The plugin base class.'''
    
    
    def __init__(self, bootstrap, *args, **kwargs):
        ''''''
        super(Plugin, self).__init__(*args, **kwargs)
        
        self.bootstrap = bootstrap

