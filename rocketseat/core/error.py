''''''

# standard
# related
# local

class RocketSeatError(Exception):
    '''The base Rocket Seat Exception, that all RS exceptions should inherit
    from.'''
    pass

class InstallError(RocketSeatError):
    '''The base install error.'''
    pass

class PluginError(RocketSeatError):
    '''The base plugin error.'''
    pass

# Install Errors
class InstallError(RocketSeatError):
    '''The base installer error.'''
    pass

class NotInstalledError(InstallError):
    '''No installation was found of Rocket Seat.'''
    pass

# Theme Errors
class ThemeError(RocketSeatError):
    '''The base theme error.'''
    pass

class ThemeNotFoundError(ThemeError):
    '''Raised if a theme, or theme name, has been used somewhere but is
    not found on the filesystem.'''
    pass

class MissingTemplateInOverride(ThemeError):
    '''Raised if a L{theme template override <core.theme.CoreTemplateOverride>}
    is not given a template_string or a template_file.
    '''
    pass
