''''''

# Standard
from itertools import imap
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
        
        self.hook_cache = {}
        
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
            
            # Return the plugin scriptname and an instance of the plugin
            # as key value pairs.
            plugin = plugin_module.Plugin(bootstrap)  
            return (plugin.script_name, plugin)
        
        self.enabled_plugins = dict(map(import_and_init, enabled_plugin_paths))
    
    def hook_plugins(self, owner, hook, callback=None, **kwargs):
        '''
        Note: The caching of hooks in this may not do anything useful. Tests
        are needed to figure that out.
        '''
        # Store it locally for efficiency
        enabled_plugins = self.enabled_plugins.values()
        hook_cache = self.hook_cache
        
        # Include the owner of the hook, in the hook string.
        hook = owner+'__'+hook
        
        def hook_a_plugin(plugin):
            '''Hook a plugin, if plugin's hook has not been cached.
            '''
            # Get the hook
            plugin_hook = getattr(plugin.events, hook)
            
            # Cache it
            hook_cache[hook].append(plugin_hook)
            
            # Call it and return the result.
            return plugin_hook(callback, **kwargs)
        
        def cached_hook_a_plugin(plugin_hook):
            '''Hook a plugin, with the cached plugin hook.
            '''
            # Call the plugin hook supplied.
            return plugin_hook(callback, **kwargs)
        
        if hook_cache.has_key(hook):
            map(cached_hook_a_plugin, hook_cache[hook])
        else:
            hook_cache[hook] = []
            map(hook_a_plugin, enabled_plugins)
    
    def hook_all_plugins(self, owner, hook, callback=None, **kwargs):
        '''Hook all plugins, regardless of whether they registered for this
        hook or not.
        '''
        # Store it locally for efficiency
        enabled_plugins = self.enabled_plugins.values()
        
        # Include the owner of the hook, in the hook string.
        hook = owner+'__'+hook
        
        def hook_a_plugin(plugin):
            return getattr(plugin.events, hook)(callback, **kwargs)
        
        map(hook_a_plugin, enabled_plugins)

class Plugin(object):
    '''The plugin base class.'''
    
    
    def __init__(self, bootstrap, *args, **kwargs):
        ''''''
        super(Plugin, self).__init__(*args, **kwargs)
        
        self.bootstrap = bootstrap

class PluginHooks(object):
    ''''''
    
    
    def __init__(self, bootstrap, *args, **kwargs):
        ''''''
        super(PluginHooks, self).__init__(*args, **kwargs)
        
        self.bootstrap = bootstrap

