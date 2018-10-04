from .syzygy import SyzygyAuthenticator

from jupyterhub.handlers import BaseHandler
from tornado import web
from traitlets import Unicode, Set


class RemoteUserLoginHandler(BaseHandler):

    async def get(self):
        self.statsd.incr('login.request')
        user = self.get_current_user()

        if user:
            self.set_login_cookie(user)
            self.redirect(self.get_next_url(user), permanent=False)
        else:
            username = self.request.headers.get(self.authenticator.shibIDAttribute, '')
            if not username:
               raise web.HTTPError(403)
            else:
                self.log.info("User %s authorized", username)

                user = self.user_from_username(username)
                self.set_login_cookie(user)
                self.redirect(self.get_next_url(user), permanent=False)


class RemoteUserLogoutHandler(BaseHandler):

    def get(self):
        user = self.get_current_user()
        shibLogoutURL = self.authenticator.shibLogoutURL

        shibReturnURL = self.authenticator.shibReturnURL
        if shibReturnURL != "":
            shibLogoutURL = "%s?return=%s" % (shibLogoutURL, shibReturnURL)
        
        self.clear_login_cookie()

        self.log.info("Logout dest: %s" % shibLogoutURL)
        self.redirect(shibLogoutURL)


class RemoteUserAuthenticator(SyzygyAuthenticator):
    """
    Accept the authenticated user attribute from the shibboleth headers.
    """
    shibIDAttribute = Unicode('REMOTE_USER',
        help="HTTP header to inspect for the authenticated username."
    ).tag(config=True)
    shibLogoutURL = Unicode('/Shibboleth.sso/Logout',
        help="Shibboleth logout handler."
    ).tag(config=True)
    shibReturnURL = Unicode('', help="A URL to redirect the user after logout").tag(config=True)

    def get_handlers(self, app):
        return default_handlers


default_handlers = [
    (r"/login", RemoteUserLoginHandler),
    (r"/logout", RemoteUserLogoutHandler)
]
