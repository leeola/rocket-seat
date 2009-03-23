''''''

# standard
# related
# local

class RocketSeatError(Exception):
    '''The base Rocket Seat Exception, that all RS exceptions should inherit
    from.'''
    pass

class NotInstalledError(RocketSeatError):
    '''No installation was found of Rocket Seat.'''
    pass

