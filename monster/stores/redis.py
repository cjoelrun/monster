"""
Store module for Redis
"""

from limpyd import fields
from limpyd.model import RedisModel, RedisDatabase

from monster import util
from monster.stores.store import Store


class Redis(Store, RedisModel):
    if not util.redis:
        creds = util.config['secrets']['redis']
        util.redis = RedisDatabase(host=creds['host'], port=creds['port'],
                                   db=creds['db'])

    database = util.redis
    name = fields.PKField()
    os_name = fields.StringField()
    branch = fields.StringField()
    features = fields.HashField()
    nodes = fields.ListField()
    status = fields.StringField()
    provisioner = fields.StringField()
    product = fields.StringField()

    def save(self, deployment):
        """
        Saves deployment to Redis
        :param deployment: Deployment to save
        :type deployment: Monster.Deployment
        """
        self.name.set(deployment.name)
        self.os_name.set(deployment.os_name)
        self.branch.set(deployment.branch)
        self.features.set(deployment.feature_names)
        self.nodes.set(deployment.nodes)
        self.status.set(deployment.status)
        self.provisioner.set(deployment.provisioner)
        self.product.set(deployment.product)

    def restore(self, name):
        """
        Restores Deployment from Redis
        :param name: Deployment name to restore
        :type name: string
        :rtype: Monster.Deployment
        """
        raise NotImplementedError
