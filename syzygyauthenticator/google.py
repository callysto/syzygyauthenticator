from .syzygy import SyzygyAuthenticator
from oauthenticator import GoogleOAuthenticator

from traitlets import Integer

from tornado import gen

class SyzygyGoogleOAuthenticator(SyzygyAuthenticator, GoogleOAuthenticator):
    """A version using PAM for authentication"""
    def normalize_username(self, username):
        """Normalize a username"""
        username = username.lower()
        return username.split('@')[0]
