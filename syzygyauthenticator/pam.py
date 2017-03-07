from .syzygy import SyzygyLocalAuthenticator
from jupyterhub.auth import PAMAuthenticator

from traitlets import default
from shutil import which
from tornado import gen

import pwd 

class SyzygyPAMAuthenticator(SyzygyLocalAuthenticator, PAMAuthenticator):
    """A version using PAM for authentication"""

    @default('create_homedir_cmd')
    def _create_homedir_cmd_default(self):
        if which('zfs'):
            return ['/opt/syzygyauthenticator/zfs-homedir.sh', self.homedir_string, self.user.name ]
        else:
            raise ValueError("I don't know how to create homedir storage on this system")

    @gen.coroutine
    def add_user(self, user):
        """Add a new user"""
        if user.state is None:
            user.state = {}
        user.state['user_id'] = pwd.getpwnam(user.name).pw_uid
        self.db.commit()

        yield gen.maybe_future(super().add_user(user))
