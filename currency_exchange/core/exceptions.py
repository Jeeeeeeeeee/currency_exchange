"""
doc string goes here
"""

__all__ = ['BackendException', 'BackendConnectionError', 'BackendReadError', 'BackendParseError',
           'BackendUnhandledException', 'BackendReadTimeoutError',
           'ServiceException']

# Standard library imports.

# Related third party imports.

# Local application/library specific imports.


class BackendException(Exception):
    pass


class ServiceException(Exception):
    pass


class BackendConnectionError(BackendException):
    pass


class BackendReadTimeoutError(BackendException):
    pass


class BackendReadError(BackendException):
    pass


class BackendParseError(BackendException):
    pass


class BackendUnhandledException(BackendException):
    pass
