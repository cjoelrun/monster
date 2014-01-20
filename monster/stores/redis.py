"""
Store module for Redis
"""

from limpyd import fields
from limpyd.model import RedisDatabase, RedisModel

from monster import util
from monster.stores.store import Store


class Redis(Store, RedisModel):
    if not util.redis:
        creds = util.config['secrets']['redis']
        util.redis = RedisDataBase(host=creds['host'], port=creds['port'],
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
        pass

    def restore(self, name):
        """
        Restores Deployment from Redis
        :param name: Deployment name to restore
        :type name: string
        """
        raise NotImplementedError
