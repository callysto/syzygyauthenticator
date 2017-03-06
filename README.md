# Syzygy ZFS Integrated Authenticators

------------
Installation
------------

This package can be installed with `pip`:

    cd syzygyauthenticator
    pip install . --upgrade

You should edit your :file:`jupyterhub_config.py` to set the authenticator
class, e.g.

    c.JupyterHub.authenticator_class = 'syzygyauthenticator.pam.SyzygyPAMAuthenticator'

## SyzygyAuthenticator

This is the base class, it inherits directly from the Authenticator class. It is
not designed to be used directly as an authenticator but should be subclassed by
another authenticator. It adds the following traits

  * homedir_string: A path template for user directories, all occurences of the
    USERNAME token will be replaced.
  * create_homedir_cmd: A command for creating a home directory matching
    homedir_string. It is specified as a list of elements which will be joined
    together with any occurences of USERNAME replaced by the current username.
  * create_user_homedir: If set to true, attempt to create a homedir for the
    user matching the homedir_string. The default create command uses the
    zfs-homedir.sh script in this directory.

The authenticator also overrides the following methods

  * add_user: Check if a homedir already exists. If not and if
    create_user_homedir is set, then try to create it.

The following new methods are defined
  
  * user_homedir_exists: Check that homdir_string with USERNAME replaced is a
    valid system directory.
  * add_user_homedir: Create a user home directory

## pam.SyzygyPAMAuthenticator

This is the first pracitcal authenticator. It operates similiarly to the default
PAMAuthenticator, but mixes in the homedir creation from the
SyzygyAuthenticator.

