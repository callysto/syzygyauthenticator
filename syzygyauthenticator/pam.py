from .syzygy import SyzygyAuthenticator

from jupyterhub.auth import PAMAuthenticator

class SyzygyPAMAuthenticator(SyzygyLocalAuthenticator, PAMAuthenticator):
	"""A version using PAM for authentication"""
	pass
