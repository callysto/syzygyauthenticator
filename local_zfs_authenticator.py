"""
A authenticator to create zfs homedir for users
"""

import os
import pwd

from traitlets import Unicode

from jupyterhub.auth import PAMAuthenticator

class LocalZFSAuthenticator(PAMAuthenticator):

    homedir_string = Unicode('/tank/home/USERNAME',
       help="String template for absloute path to user home directory"
    ).tag(config=True)
   
    def system_user_exists(self, user):
        try:
            pwd.getpwnam(user.name)
        except KeyError:
            self.log.info('User "%s" not in LDAP' % user.name)
            return False
        else:
            self.log.info('User "%s" in LDAP' % user.name)
            return False

    def add_system_user(self, user):
        """Create storage for users in ZFS"""
        if not os.path.isdir(self.homedir_string.replace('USERNAME', user.name)):
            self.log.info("User exists but has no homedir, adding %s" % self.homedir_string)
            super().add_system_user(user)
