"""Based on https://github.com/yuvipanda/jupyterhub-dummy-authenticator
   but tuned to Callysto to account for homedirs and such"""

from traitlets import Unicode
from tornado import gen
from .syzygy import SyzygyAuthenticator

class SyzygyDummyAuthenticator(SyzygyAuthenticator):
    password = Unicode(
        None,
        allow_none=True,
        config=True,
        help="""
        Set a global password for all users wanting to log in.

        This allows users with any username to log in with the same static password.
        """
    )

    @gen.coroutine
    def authenticate(self, handler, data):
        if self.password:
            if data['password'] == self.password:
                return data['username']
            return None
        return data['username']
