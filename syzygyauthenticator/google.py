"""
Google OAuthenticator with name normalization from syzygy
"""

from .syzygy import SyzygyAuthenticator
from oauthenticator import GoogleOAuthenticator 

class SyzygyGoogleOAuthenticator(GoogleOAuthenticator, SyzygyAuthenticator):
        """Syzygy Authenticator"""
        pass
