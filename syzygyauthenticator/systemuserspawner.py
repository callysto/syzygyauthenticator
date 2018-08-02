from dockerspawner.systemuserspawner import SystemUserSpawner

class SyzygySystemUserSpawner(SystemUserSpawner):
    def get_env(self):
        env = super(SystemUserSpawner, self).get_env()
        # relies on NB_USER and NB_UID handling in jupyter/docker-stacks
        # Truncate NB_USER to maximum linux username length
        env.update(dict(
            USER=self.user.name[:32], # deprecated
            NB_USER=self.user.name[:32],
            USER_ID=self.user_id, # deprecated
            NB_UID=self.user_id,
            HOME=self.homedir,
        ))
        return env

    def _user_id_default(self):
        """
        Get user_id from pwd lookup by name
        Since our users logging in don't have a real system account
        we need to use the jupyter user's UID
        """
        import pwd
        return pwd.getpwnam('jupyter').pw_uid
