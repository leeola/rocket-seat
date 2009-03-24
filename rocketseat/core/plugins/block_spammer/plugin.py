''''''

# Standard
# Related
# Local
import core.plugin


class Plugin(core.plugin.Plugin):
    ''''''
    
    
    def __init__(self, bootstrap):
        '''
        '''
        super(Plugin, self).__init__(bootstrap)
        
        self.events = PluginEvents(bootstrap)

class PluginEvents(core.plugin.PluginEvents):
    ''''''
    
    def core_p__bootstrap_finished(self, callback):
        '''
        '''
        pass
