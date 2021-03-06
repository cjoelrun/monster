"""
Tool to retrofit a install
"""

from monster import util


class Retrofit(object):

    def __init__(self, deployment):
        self.deployment = deployment
        self.controllers = list(self.deployment.search_role('controller'))
        self.computes = list(self.deployment.search_role('compute'))

    def __repr__(self):
        """
        Print out current instance
        """

        outl = 'class: ' + self.__class__.__name__
        for attr in self.__dict__:
            outl += '\n\t{0} : {1}'.format(attr, getattr(self, attr))
        return outl

    def install(self, branch):
        """
        Installs the retrofit tool on the nodes
        """

        util.logger.info("Installing Retrofit")

        # Check for support
        self._check_os()
        self._check_neutron()
        self._check_brctl()

        for controller in self.controllers:
            self._install_repo(controller, branch)

        for compute in self.computes:
            self._install_repo(compute, branch)

    def bootstrap(self, iface, lx_bridge, ovs_bridge):
        """
        Bootstraps a node with retrofit
        """

        util.logger.info("Bootstraping to seperate plane")

        # bootstrap cmd
        bstrap_cmds = ['cd /opt/retrofit',
                       './retrofit.py bootstrap -i {0} -l {1} -o {2}'.format(
                           iface, lx_bridge, ovs_bridge)]
        bstrap_cmd = "; ".join(bstrap_cmds)

        for controller in self.controllers:
            controller.run_cmd(bstrap_cmd)

        for compute in self.computes:
            compute.run_cmd(bstrap_cmd)

    def convert(self, iface, lx_bridge, ovs_bridge):
        """
        Converts a deployment to a seperate plane
        """

        util.logger.info("Converting to seperate plane")

        conv_cmds = ["cd '/opt/retrofit",
                     "./retrofit.py convert -i {0} -l {1} -o {2}".format(
                         iface, lx_bridge, ovs_bridge)]
        conv_cmd = "; ".join(conv_cmds)

        for controller in self.controllers:
            controller.run_cmd(conv_cmd)

        for compute in self.computes:
            compute.run_cmd(conv_cmd)

    def revert(self, iface, lx_bridge, ovs_bridge):
        """
        Reverts a deployment to a single plane
        """

        util.logger.info("Reverting to a single plane")

        revt_cmds = ["cd '/opt/retrofit",
                     "./retrofit.py revert -i {0} -l {1} -o {2}".format(
                         iface, lx_bridge, ovs_bridge)]
        revt_cmd = "; ".join(revt_cmds)

        for controller in self.controllers:
            controller.run_cmd(revt_cmd)

        for compute in self.computes:
            compute.run_cmd(revt_cmd)

    def remove_port_from_bridge(self, ovs_bridge, del_port):
        """
        Removes a port from a bridge for the deployment
        """

        util.logger.info(
            ("Removing old OVS port:{0} from OVS bridge: "
             "{1} on deployment: {2}".format(
                 del_port, ovs_bridge, self.deployment.name)))

        remove_cmd = "ovs-vsctl del-port {0} {1}".format(ovs_bridge, del_port)

        for controller in self.controllers:
            controller.run_cmd(remove_cmd)

        for compute in self.computes:
            compute.run_cmd(remove_cmd)

    def _install_repo(self, node, branch='master'):
        """
        Installs the retrofit repository
        """

        retro_git = util.config['rcbops']['retrofit']['git']['url']
        branches = util.config['rcbops']['retrofit']['git']['branches']

        if branch not in branches:
            error = "{0} not a supported branch in retrofit".format(branch)
            util.logger.info(error)
            raise Exception(error)

        # clone repo
        clone_cmds = ['cd /opt',
                      'rm -rf retrofit',
                      'git clone -b {0} {1}'.format(branch, retro_git)]

        clone_cmd = "; ".join(clone_cmds)

        node.run_cmd(clone_cmd)

    def _check_neutron(self):
        """
        Check to make sure neutron is in the deployment
        """

        if not self.deployment.feature_in('neutron'):
            error = "This build doesnt have Neutron/Quantum, cannot Retrofit"
            util.logger.info(error)
            raise Exception(error)

    def _check_os(self):
        """
        Checks to see if os is supported
        """

        supported = util.config['rcbops']['retrofit']['supported']['os']

        if not self.deployment.os_name in supported:
            error = "{0} is not a retrofit supported OS".format(
                self.deployment.os_name)
            util.logger.info(error)
            raise NotImplementedError(error)

    def _check_brctl(self):
        """
        Checks to see if bridge-util is installed on nodes
        """

        for controller in self.controllers:
            installed = controller.check_package('bridge-utils')['success']
            if not installed:
                controller.install_package('bridge-utils')

        for compute in self.computes:
            installed = compute.check_package('bridge-utils')['success']
            if not installed:
                compute.install_package('bridge-utils')
