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
        """Syzygy Authenticator"""
        pass

class SyzygyLocalAuthenticator(SyzygyAuthenticator, LocalAuthenticator):
	"""A version mixing in local user creation"""
	pass
