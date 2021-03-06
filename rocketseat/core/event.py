''''''

# Standard
# Related
# Local


class EventsController(object):
    ''''''
    
    
    def __init__(self, events_entity, plugins):
        ''''''
        
        self.events_entity = events_entity
        self.plugins = plugins
        
        self.listener_cache = {}
        self.event_subscribers = {
            # Enter fake subscription details for early no-db testing.
            'core_p__bootstrap_finished':('block_spammer',),
        }
    
    def call_listeners(self, owner_name, event_name, callback=None, **kwargs):
        '''
        @note: The caching of listener in this may not do anything useful. Tests
        are needed to figure that out.
        
        @returns: A list of values returned from each listener called.
        '''
        # Store it locally for efficiency
        plugins = self.plugins.values()
        listener_cache = self.listener_cache
        
        # Include the owner of the event, in the event string.
        full_event_name = owner_name+'__'+event_name
        
        def call_a_listener(plugin):
            '''Call a listener that has not been cached, and cache it.
            '''
            if plugin.script_name in self.event_subscribers[full_event_name]:
                # Get the listener function
                plugin_listener = getattr(plugin.listeners, full_event_name)
                
                # Cache it
                listener_cache[full_event_name].append(plugin_listener)
                
                # Call it and return the result.
                return plugin_listener(callback, **kwargs)
        
        def call_a_cached_listener(listener):
            '''
            '''
            
            # Call the listener supplied.
            return listener(callback, **kwargs)
        
        if listener_cache.has_key(full_event_name):
            # It is important to note that if we are using the cache,
            # We are not checking if the listener is subscribed to the event.
            # It is assumed that if the listener was run once, and cached,
            # that it is subscribed already.
            return map(call_a_cached_listener, listener_cache[full_event_name])
        else:
            listener_cache[full_event_name] = []
            return map(call_a_listener, plugins)
    
    def call_all_listeners(self, owner_name, event_name, 
                           callback=None, **kwargs):
        '''Call an event on all plugins, regardless of whether they registered 
        for this event or not.
        
        Note: This is to only be used for a small set of events. These events
        are also required, because this function does not try/except any
        plugins that may not have the listener function defined.
        
        @returns: A list of values returned from each listener called.
        '''
        # Store it locally for efficiency
        plugins = self.plugins.values()
        
        # Include the owner of the event, in the event string.
        full_event_name = owner_name+'__'+event_name
        
        def call_a_listener(plugin):
            return getattr(plugin.listeners, 
                           full_event_name)(callback, **kwargs)
        
        return map(call_a_listener, plugins)
    
    def clear_cache(self):
        '''
        '''
        
        self.listener_cache = {}
        self.event_subscribers = {}
        
    def subscribe_to_event(self, event_owner_name, event_name, script_name):
        '''
        '''
        pass
