from .syzygy import SyzygyAuthenticator
from oauthenticator import GoogleOAuthenticator

from traitlets import Integer

from tornado import gen

class SyzygyGoogleOAuthenticator(SyzygyAuthenticator, GoogleOAuthenticator):
    """A version using PAM for authentication"""
    user_id = Integer(-1,
        config=True,
        help="""UIDnumber of the home directory owner"""
    )

    @gen.coroutine
    def add_user(self, user):
        """Add a new user"""
        if user.state is None:
            user.state = {}
        user.state['user_id'] = self.user_id
        self.db.commit()

        yield gen.maybe_future(super().add_user(user))

    def normalize_username(self, username):
        """Normalize a username"""
        username = username.lower()
        return username.split('@')[0]
