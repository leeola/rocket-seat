''''''

# standard
# related
from google.appengine.ext import db
# local


class Events(db.Model):
    '''The events model (or rather, those who inherit from it) is responsible
    for holding all events, and a list of plugins who will be called
    upon the triggering of each hook.

    Currently this base model does not define any inherited values.'''
    pass

class CoreEvents(Events):
    '''A model responsible for holding lists of modules which are registered 
    for rocket seat events.

    Just like plugins, the text preceeding the double underscores describes
    the hooks owner, or caller.
    
    The following is a list of event prefixes, and what they mean.
     - core: These are generic core events, not specific to any handler.
     - core_p: This event is specific to hooks triggered by the Page Handler.
    '''
    # As a side note, these are ordered by timeline and not by alpha.

    #: Ask each plugin if they want to register for this specific page load.
    core__bootstrap_finished = db.StringListProperty()
    
    #: If a plugin has CSS to add to the page, do so on this event.
    #: Expected Return: A tuple of tuples, in the same format used for user
    #: themes.
    #: @also: L{core.themes.usability.theme.css_files}
    core_p__add_plugin_css = db.StringListProperty()

    #: These two are called _after_ a plugin is installed/uninstalled.
    core__plugin_installed_hook = db.StringListProperty()
    core__plugin_uninstalled_hook = db.StringListProperty()
    
    #: These two are called _after_ a plugin is enabled/disabled.
    core__plugin_enabled_hook = db.StringListProperty()
    core__plugin_disabled_hook = db.StringListProperty()

class RocketSeatConfig(db.Model):
    '''A model containing configuration information about the site itself; 
    such as, sitename, plugins, etc.'''

    # A list of enabled plugins in the form of the module path
    enabled_plugins = db.StringListProperty()

    # The active theme python path.
    active_theme = db.StringProperty(default='core.themes.raw')
    
    # Is the site undergoing maintenance?
    undergoing_maintenance = db.BooleanProperty(default=True)

class UserAccount(db.Model):
    '''A model that holds a single user's rocketseat account data.
    '''

    # The name alias for this user.
    alias = db.StringProperty(required=True)

    # A list of permissions. Any permission found here will give the user 
    # access to whatever that permission grants, such as common "user, admin, 
    # moderator" permissions.
    permission_groups = db.StringListProperty(default=['user'])
