"""
A authenticator to create zfs homedir for users
"""

import os
import pwd
from shutil import which
import pipes

from subprocess import Popen, PIPE, STDOUT

from tornado import gen

from traitlets import Unicode, default, Bool, Integer
from jupyterhub.traitlets import Command

from jupyterhub.auth import Authenticator, LocalAuthenticator

class SyzygyAuthenticator(Authenticator):

    user_id = Integer(-1,
        config=True,
        help="""UIDnumber of the home directory owner"""
    )

    homedir_string = Unicode('/tank/home/USERNAME',
       help="String template for absloute path to user home directory"
    ).tag(config=True)

    create_user_homedir = Bool(False,
        help="""
            If set to True, will attempt to create storage for users

            Mutually exclusive with create_system_users
            """
    ).tag(config=True)

    create_homedir_cmd = Command(
        help="""The command to use for creating users as a list of strings.

        For each element in the list, the string USERNAME will be replaced with
        the user's username.
        """
    ).tag(config=True)
    
    @default('create_homedir_cmd')
    def _create_homedir_cmd_default(self):
        if which('zfs'):
            return ['/opt/syzygyauthenticator/zfs-homedir.sh', self.homedir_string, 'jupyter']
        else:
            raise ValueError("I don't know how to create homedir storage on this system")

    def user_homedir_exists(self, user):
       homedir = self.homedir_string.replace('USERNAME', user.name)
       if os.path.isdir(homedir):
           self.log.info('User "%s" has homedir (%s)' % (homedir, user.name))
           return True
       else:
           self.log.info('User "%s" has no homedir (%s)' % (user.name, homedir))
           return False

    @gen.coroutine
    def add_user(self, user):
        """Hook called whenever a new user is added

            This authenticator will _always_ call add_system_user. Decisions
            about what actions new users should trigger (e.g. homedir 
            creation) are taken there.
        """
        homedir_exists = yield gen.maybe_future(self.user_homedir_exists(user))
        if not homedir_exists:
            if self.create_user_homedir:
                yield gen.maybe_future(self.add_user_homedir(user))
            else:
                raise KeyError('User %s homedir does not exist and create_user_homedir unset')
       
        if user.state is None:
            user.state = {}
        user.state['user_id'] = self.user_id
        self.db.commit()
        self.log.info('User "%s" has uid (%s)' % (user.name, user.state['user_id']))

        yield gen.maybe_future(super().add_user(user))
    
    def add_user_homedir(self, user):
        """Create storage for users in ZFS"""

        name = user.name
        self.log.info("User exists but has no homedir, adding %s" % self.homedir_string.replace('USERNAME', user.name))
      
        cmd = [ arg.replace('USERNAME', name) for arg in self.create_homedir_cmd ]
        self.log.info("Adding homedir: %s", ' '.join(map(pipes.quote, cmd)))
        p = Popen(cmd, stdout=PIPE, stderr=STDOUT)
        p.wait()
        if p.returncode:
            err = p.stdout.read().decode('utf8', 'replace')
            raise RuntimeError("Failed to add homedir storage for user: %s: %s"
                % (name, err))

    def pre_spawn_start(self, user, spawner):
        """Make sure that user_id is available in all cases"""
        #spawner.load_state(user.state)

class SyzygyLocalAuthenticator(SyzygyAuthenticator, LocalAuthenticator):
	"""A version mixing in local user creation"""
	pass
