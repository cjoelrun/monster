from chef import autoconfigure
from chef import Environment as ChefEnvironment

from monster import util
from chef import Node as ChefNode

from monster.stores.store import Store
from monster.provisioners.util import get_provisioner
from monster.nodes.chef_node import Chef as MonsterChefNode
from monster.deployments.chef_deployment import Chef as ChefDeployment
from monster.environments.chef_environment import Chef as \
    MonsterChefEnvironment


class Chef(Store):
    """
    Stores restoration data into chef environment
    """

    def __init__(self, api):
        raise NotImplementedError

    def save(self, deployment):
        """
        Save deployment restore attributes to chef environment
        :param deployment: Deployment to save
        :type deployment: Monster.Deployment
        """

        features = {key: value for (key, value) in
                    ((str(x).lower(), x.rpcs_feature) for x in
                     deployment.features)}
        nodes = [n.name for n in deployment.nodes]
        deployment = {'nodes': nodes,
                      'features': features,
                      'name': deployment.name,
                      'os_name': deployment.os_name,
                      'branch': deployment.branch,
                      'status': deployment.status,
                      'product': deployment.product,
                      'provisioner': deployment.provisioner}

        deployment.environment.add_override_attr('deployment', deployment)

    def restore(self, name):
        """
        Rebuilds a Deployment given a chef environment
        :param name: name of environment
        :type name: string
        :rtype: Monster.Deployments.Chef
        """

        local_api = autoconfigure()
        env = ChefEnvironment(name, api=local_api)
        override = env.override_attributes
        default = env.default_attributes
        chef_auth = override.get('remote_chef', None)
        remote_api = None
        if chef_auth and chef_auth["key"]:
            remote_api = ChefServer._remote_chef_api(chef_auth)
            renv = ChefEnvironment(name, api=remote_api)
            override = renv.override_attributes
            default = renv.default_attributes
        environment = MonsterChefEnvironment(
            env.name, local_api, description=env.name,
            default=default, override=override, remote_api=remote_api)

        name = env.name
        deployment_args = override.get('deployment', {})
        features = deployment_args.get('features', {})
        os_name = deployment_args.get('os_name', None)
        branch = deployment_args.get('branch', None)
        status = deployment_args.get('status', "provisioning")
        product = deployment_args.get('product', None)
        provisioner_name = deployment_args.get('provisioner', "razor")
        provisioner = get_provisioner(provisioner_name)

        deployment = ChefDeployment.deployment_config(features, name, os_name, branch,
                                           environment, provisioner, status,
                                           product=product)

        nodes = deployment_args.get('nodes', [])
        for node in (ChefNode(n, local_api) for n in nodes):
            if not node.exists:
                util.logger.error("Non existant chef node:{0}".
                                  format(node.name))
                continue
            cnode = MonsterChefNode.from_chef_node(node,
                                                   deployment_args['os_name'],
                                                   product, environment,
                                                   deployment, provisioner,
                                                   deployment_args['branch'])
            deployment.nodes.append(cnode)
        return deployment

    def exists(self, name):
        api =
        return ChefEnvironment(name, api=local_api).exists:
