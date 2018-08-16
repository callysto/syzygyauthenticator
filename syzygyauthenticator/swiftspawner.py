from dockerspawner import DockerSpawner
from traitlets import Dict

class SyzygySwiftSpawner(DockerSpawner):

    openstack_auth_info = Dict(
        config=True,
        help="""OpenStack authentication information""",
    )

    def get_env(self):
        env = super(DockerSpawner, self).get_env()
        env.update(self.openstack_auth_info)
        env["JPYNB_SWIFT_CONTAINER"] = env["NB_USER"]
        return env
