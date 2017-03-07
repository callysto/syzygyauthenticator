from .syzygy import SyzygyAuthenticator
from oauthenticator import GoogleOAuthenticator

from traitlets import Integer

from tornado import gen

class SyzygyGoogleOAuthenticator(SyzygyAuthenticator, GoogleOAuthenticator):
    """A version using PAM for authentication"""

    logoutURL = Unicode('/logout',
        help="logout URL"
    ).tag(config=True)

    def SyzygyGoogleOAuthenticatorLogoutHandler(BaseHandler):
        def get(self):
            user = self.get_current_user()
            if user:
                self.log.info("User %s logged out", user.name)
                self.clear_login_cookie()
                for name in user.other_user_cookies:
                    self.clear_logout_cookie(name)
                user.other_user_cookies = set([])
                self.statsd.incr('logout')
            self.redirect(self.authenticator.logoutURL)

    def normalize_username(self, username):
        """Normalize a username"""
        username = username.lower()
        return username.split('@')[0]
