
class Upgrade(object):
    """
    Base upgrade class
    """

    def __init__(self, deployment):
        self.deployment = deployment

    def upgrade(self, upgrade_branch):
        raise NotImplementedError
