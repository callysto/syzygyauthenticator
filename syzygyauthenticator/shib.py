from .syzygy import SyzygyAuthenticator

from jupyterhub.handlers import BaseHandler
from tornado import web
from traitlets import Unicode, Set


class RemoteUserLoginHandler(BaseHandler):

    async def get(self):
        self.statsd.incr('login.request')
        user = self.current_user

        if user:

            self.set_login_cookie(user)
            self.redirect(self.get_next_url(user), permanent=False)
        else:
            # c.ShibAuthenticator.shibIDAttribute   <- user@place style username
            # c.ShibAuthenticator.shibValidEntitlements  <- entitlements considered "valid"
            # c.ShibAuthenticator.shibUserEntitlements<- current user's attributes
            username = self.authenticator.normalize_username(
                self.request.headers.get(self.authenticator.shibIDAttribute, ''))
            userEntitlements = set(self.request.headers.get(
                self.authenticator.shibUserEntitlements, '').split(';'))
            validEntitlements = self.authenticator.shibValidEntitlements

            # Set intersection, any userentitlement in validEntitlements is enough
            entitlement = userEntitlements & validEntitlements

            if entitlement and self.authenticator.check_whitelist(username):
                self.log.info("User %s authorized with entitlement %s in %s",
                              username, entitlement, validEntitlements)
                user = self.user_from_username(username)
                self.set_login_cookie(user)
                self.redirect(self.get_next_url(user), permanent=False)

            else:
                self.log.info("Missing entitlement user (%s): '%s' not in '%s')", 
                              username, userEntitlements, validEntitlements)
                raise web.HTTPError(403, """You have authenticated successfully to your institution, but
                                you do not currently have the entitlements needed to access this
                                application.  Please contact jupyter@pims.math.ca to enquire about
                                access.""")

            auth_instant = self.request.headers.get(self.authenticator.shibAuthInstant, '')
            self.log.info("Authentication instant: %s", auth_instant)


class RemoteUserLogoutHandler(BaseHandler):

    def get(self):
        user = self.get_current_user()
        shibLogoutURL = self.authenticator.shibLogoutURL
        
        self.clear_login_cookie()

        self.log.info("Logout dest: %s" % shibLogoutURL)
        self.redirect(shibLogoutURL)


class RemoteUserAuthenticator(SyzygyAuthenticator):
    """
    Accept the authenticated user attribute from the shibboleth headers.
    """
    shibIDAttribute = Unicode('REMOTE-USER',
        help="HTTP header to inspect for the authenticated username."
    ).tag(config=True)
    shibUserEntitlements = Unicode('eduPersonEntitlement',
        help="HTTP header containing user's entitlements."
    ).tag(config=True)
    shibValidEntitlements = Set(
        help="set containing entitlements sufficient to allow access"
    ).tag(config=True)
    shibLogoutURL = Unicode('/Shibboleth.sso/Logout',
        help="Shibboleth logout handler."
    ).tag(config=True)
    shibAuthInstant = Unicode('Shib-Authentication-Instant',
        help="HTTP header containing ISO timestamp of authentication instant at IdP"
    ).tag(config=True)

    def normalize_username(self, username):
        """Normalize the username - just toss away everything after @ and cast
        to lowercase"""
        username = username.split('@')[0]
        username = username.lower()
        username = username.replace('.','-')
        username = self.username_map.get(username, username)
        return username

    def get_handlers(self, app):
        return default_handlers


default_handlers = [
    (r"/login", RemoteUserLoginHandler),
    (r"/logout", RemoteUserLogoutHandler)
]
