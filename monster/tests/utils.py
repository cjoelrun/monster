import subprocess

from monster.tests.tempest_helper import TempestHelper
from monster.tests.ha import HATest
from monster import util


class TestUtil:
    def __init__(self, deployment, args):
        self.deployment = deployment
        self.iterations = args.iterations

    def run_ha(self):
        if not self.deployment.feature_in("highavailability"):
            util.logger.warning('High Availability was not detected as a '
                                'feature; HA tests will not be run!')
            return
        ha = HATest(self.deployment)
        self.__run(ha)

    def run_tempest(self):
        branch = self.deployment.branch
        test_suite = TempestHelper.get_test_suite_for(branch)
        self.__run(test_suite)

    def run_cloudcafe(self):
        pass

    def __run(self, test_suite):
        self.__prepare_xml_directory()
        util.logger.info('Running {0}!'.format(test_suite.name))
        for i in range(self.iterations):
            util.logger.debug('Running iteration %s!' % (i + 1))
            test_suite.test()
        util.logger.info('{0} have been completed with {1} iterations!'
                         .format(test_suite.name, self.iterations))

    def __prepare_xml_directory(self):
        env = self.deployment.environment.name
        local = "./results/{0}/".format(env)
        controllers = self.deployment.search_role('controller')
        for controller in controllers:
            ip, user, password = controller.get_creds()
            remote = "{0}@{1}:~/*.xml".format(user, ip)
            self.__get_file(ip, user, password, remote, local)

            #Prepares directory for xml files to be SCPed over
            self.subprocess.call(['mkdir', '-p', '{0}'.format(local)])

    def __get_file(ip, user, password, remote, local, remote_delete=False):
        cmd1 = 'sshpass -p {0} scp -q {1} {2}'.format(password, remote, local)
        subprocess.call(cmd1, shell=True)
        if remote_delete:
            cmd2 = ("sshpass -p {0} ssh -o UserKnownHostsFile=/dev/null "
                    "-o StrictHostKeyChecking=no -o LogLevel=quiet -l {1} {2}"
                    " 'rm *.xml;exit'".format(password, user, ip))
            subprocess.call(cmd2, shell=True)
