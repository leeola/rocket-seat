''''''

# standard
# related
# local

# Base Errors
class RocketSeatError(Exception):
    '''The base Rocket Seat Exception, that all RS exceptions should inherit
    from.'''
    pass

class InstallError(RocketSeatError):
    '''The base install error.'''
    pass

class ThemeError(RocketSeatError):
    '''The base theme error.'''
    pass

class PluginError(RocketSeatError):
    '''The base plugin error.'''
    pass

# Install Errors
class NotInstalledError(InstallError):
    '''No installation was found of Rocket Seat.'''
    pass

# Theme Errors
class ThemeNotFoundError(ThemeError):
    '''Raised if a theme, or theme name, has been used somewhere but is
    not found on the filesystem.'''
    pass
