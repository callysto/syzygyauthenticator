"""
An Authenticator to create ZFS based home directories for users
"""

import os
import pipes
import pwd

from traitlets import Unicode, Integer
from jupyterhub.traitlets import Command

from jupyterhub.auth import Authenticator, LocalAuthenticator

from shutil import which
from subprocess import Popen, PIPE, STDOUT

class LocalZFSAuthenticator(Authenticator):
    user_id = Integer(-1,
        config=True,
        help="""User ID of the jupyter home directories owner"""
    )
    homedir_string = Unicode('/home/USERNAME',
        help="String representing the absolute path of a user homedir"
    ).tag(config=True)
    create_homedir_command = Command(
        help="""The command to use for creating user homedirs

        USERNAME will be replaced with the actual username."""
    ).tag(config=True)
    @default('create_homedir_cmd')
    def _create_homedir_cmd_default(self):
        if which('zfs'):
            return ['zfs', 'create', '-o', 'quota=1G', 'tank/home/USERNAME']
        else:
            raise ValueError("I don't know how to create non zfs homedir storage")

    @gen.coroutine
    def add_user(self, user):
        """Add a new user"""
        self.log.info("Add user: %s", user.name)
        homedir_exists = yield gen.maybe_future(self.user_homedir_exists(user))
        if not homedir_exists:
            self.log.info("System User %s with uid %i should be added", user.name, self.user_id)
            yield gen.maybe_future(elf.add_system_user(user))

        if user.state is None:
           user.state = {}
        user.state['user_id'] = self.user_id
        self.db.commit()

        yield gen.maybe_future(super().add_user(user))

    def pre_spawn_start(self, user, spawner):
        """Make sure the user_id is available"""
        spawner.load_state(user.state)

    def user_homedir_exists(self, user):
        """Check if the user home directory already exists"""
        self.log("Homedir check for %s (%s)" % (user.name, self.homedir_string.replace('USERNAME', user.name)))
        return os.path.isdir(self.homdir_string.replace('USERNAME', user.name))

    def create_user_homedir(self, user):
        """Create storage for user"""
        name = user.name
        cmd = [ arg.replace('USERNAME', name) for arg in self.create_homedir_cmd ]
        self.log.info("Adding homedir: %s", ' '.join(map(pipes.quote, cmd)))
        p = Popen(cmd, stdout=PIPE, stderr=STDOUT)
        p.wait()
        if p.returncode:
            err = p.stdout.read().decode('utf-8', 'replace')
            raise RuntimeError("Failed to add homedir for user: %s at %s" % (name, err))

    def add_system_user(self, user):
        """Map storage for a system user with ZFS"""
        self.log.infor("Adding user: %s with ZFS storage" % (user.name))
        self.create_user_homedir(user)

        if user.state is None:
            user.state = {}
        user.state['user_id'] = self.user_id
        self.db.commit()

        if hasattr(user, 'spawner'):
            user.spawner.load_state(user.state)
