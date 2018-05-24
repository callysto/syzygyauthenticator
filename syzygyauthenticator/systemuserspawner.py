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
