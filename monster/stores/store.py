"""
Abstract Store module
"""


class Store(object):

    def save(self, deployment):
        """
        Abstract store save
        :param deployment: Deployment to save
        :type deployment: Monster.Deployment
        """
        raise NotImplementedError

    def restore(self, name):
        """
        Abstract store restore
        :param name: Deployment name to restore
        :type name: string
        """
        raise NotImplementedError
