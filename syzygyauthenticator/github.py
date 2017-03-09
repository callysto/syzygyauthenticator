from .syzygy import SyzygyAuthenticator
from oauthenticator.github import GitHubOAuthenticator

from jupyterhub.handlers import BaseHandler

from traitlets import Integer, Unicode

from tornado import gen

class SyzygyGitHubOAuthenticatorLogoutHandler(BaseHandler):
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

class SyzygyGitHubOAuthenticator(SyzygyAuthenticator, GitHubOAuthenticator):
    logout_handler = SyzygyGitHubOAuthenticatorLogoutHandler

    logoutURL = Unicode('/logout',
        help="logout URL"
    ).tag(config=True)

    def normalize_username(self, username):
        """Normalize a username"""
        username = username.lower()
        return username.split('@')[0]

    def get_handlers(self, app):
        return [
            (r'/logout', self.logout_handler),
            (r'/oauth_login', self.login_handler),
            (r'/oauth_callback', self.callback_handler),
        ]
