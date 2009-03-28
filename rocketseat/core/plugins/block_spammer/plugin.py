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
        
        self.events = PluginHooks(bootstrap)

class PluginHooks(core.plugin.PluginHooks):
    ''''''
    
    def core_p__bootstrap_finished(self, callback=None):
        '''
        '''
        pass
