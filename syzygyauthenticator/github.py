"""
Google OAuthenticator with name normalization from syzygy
"""

from .syzygy import SyzygyAuthenticator
from oauthenticator import GitHubOAuthenticator 

class SyzygyGitHubOAuthenticator(GitHubOAuthenticator, SyzygyAuthenticator):
        """Syzygy Authenticator"""
        pass
