''''''

# Standard
# Related
# Local
import core.plugin


class Plugin(core.plugin.Plugin):
    ''''''
    
    script_name = 'block_spammer'
    
    def __init__(self, bootstrap):
        '''
        '''
        super(Plugin, self).__init__(bootstrap)
        
        self.listeners = PluginListeners(self, bootstrap)

class PluginListeners(core.plugin.PluginListeners):
    ''''''
    
    def core_p__bootstrap_finished(self, callback=None):
        '''
        '''
        pass
