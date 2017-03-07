from .syzygy import SyzygyAuthenticator

from tornado import gen
from traitlets import Unicode, Set

from jupyterhub.handlers import BaseHandler, LoginHandler


class ShibLoginHandler(LoginHandler):

    def get(self):
        next_url = self.get_argument('next', '')
        if not next_url.startswith('/'):
            next_url = ''

        username = self.authneticator.normalize_username(
            self.request.headers-get(self.authenticator.shibIDAttribute, ''))
        userEntitlements = set(self.request.handlers.get(
            self.authenticator.shibUserEntitlements, '').split(';'))
        validEntitlements = self.authenticator.shibValidEntitlements

        entitlement = userEntitlements & validEntitlements

        if entitlement:
            self.log.info("User %s authorized with entitlement %s in %s",
                username, entitlement, validEntitlements)
            user = self.user_from_username(username)
            self.set_login_cookie(user)

        else:
            self.log.info("Missing entilement for user (%s): '%s' not in '%s')",
                username, userEntitlement, validEntitlement)

            raise web.HTTPError(403, """You have authenticated successfully to your institution, but
                                you do not currently have the entitlements needed to access this
                                application.  Please contact jupyter@pims.math.ca to enqure about
                                access.""")

class ShibLogoutHandler(BaseHandler):
    def get(self):
        user = self.get_current_user()
        
        self.clear_login_cookie()
        for name in user.other_user_cookies:
            self.clear_login_cookie(name)
        user.other_user_cookies = set([])

        self.log.info("Logout dest: %s -> %s", user.name, logoutURL)
        self.redirect(logoutURL)


class ShibAuthenticator(SyzygyAuthenticator):
    
    shibIDAttribute = Unicode('X-Proxy-REMOTE-USER',
        help="HTTP header to inspect for the authenticated username."
    ).tag(config=True)

    shibUserEntitlements = Unicode('eduPersonEntitlement',
        help="HTTP header containing user's entitlements."
    ).tag(config=True)

    shibValidEntitlements = Set(
        help="set containing entitlements sufficient to allow access"
    ).tag(config=True)

   
    def normalize_username(self, username):
        username = username.split('@')[0]
        username = username.lower()
        username = username.replace('.','-')
        username = self.username_map.get(username, username)
        return username

    def get_handlers(self, app):
        return [
            (r'/login', ShibLoginHandler),
            (r'/logout', ShibLogoutHandler),
        ]

    @gen.coroutine
    def authenticate(self, *args):
        raise NotImplementedError()
