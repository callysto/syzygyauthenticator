from syzygyauthenticator.systemuserspawner import SyzygySystemUserSpawner
from traitlets import Dict

class SyzygySwiftSystemUserSpawner(SyzygySystemUserSpawner):

    openstack_auth_info = Dict(
        config=True,
        help="""OpenStack authentication information""",
    )

    def get_env(self):
        env = super(SyzygySwiftSystemUserSpawner, self).get_env()
        env.update(self.openstack_auth_info)
        env["JPYNB_SWIFT_CONTAINER"] = env["NB_USER"]
        return env
