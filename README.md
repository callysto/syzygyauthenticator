# Jupyterhub ZFS Authenticator

A simple subclass of LocalAuthenticator to handle homedir creation on zfs.

------------
Installation
------------

This package can be installed with `pip`:

    cd zfs_home_authenticator 
    pip install .

You should edit your :file:`jupyterhub_config.py` to set the authenticator
class::

    c.JupyterHub.authenticator_class = 'zfs_home_authenticator.LocalZFSAuthenticator'

