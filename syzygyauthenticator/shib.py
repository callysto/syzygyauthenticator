from jhub_remote_user_authenticator import remote_user_auth as jhub_remote_user
from .syzygy import SyzygyAuthenticator, SyzygyLocalAuthenticator


class RemoteUserLoginHandler(jhub_remote_user.RemoteUserLoginHandler):

    pass


class RemoteUserAuthenticator(SyzygyAuthenticator,
                              jhub_remote_user.RemoteUserAuthenticator):

    def get_handlers(self, app):
        return default_handlers


class RemoteUserLocalAuthenticator(SyzygyLocalAuthenticator,
                                   jhub_remote_user.RemoteUserLocalAuthenticator):
    """A version mixing in local user creation"""

    def get_handlers(self, app):
        return default_handlers

default_handlers = [
    (r"/login", RemoteUserLoginHandler),
]
