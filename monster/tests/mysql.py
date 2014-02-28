from random import randint

from monster import util
from monster.tests.test import Test

class MySQLReplication(Test):
    """
    Assures functionality of MySqlReplication
    """

    def __init__(self, deployment):
        super(HATest, self).__init__(deployment)
        controllers = list(self.deployment.search_role("controller"))
        self.controller1 = controllers[0]
        self.controller2 = controllers[1]
        self.controller1_status = None
        self.controller2_status = None
        self.data_replication = False

    def check_status(self):
        """
        Check mysql replication status
        """
        check_cmd = "mysql -e 'SHOW SLAVE STATUS\G'"
        ret = controller1.run_cmd(check_cmd)
        self.controller1_status = ret['return']

        ret = controller2.run_cmd(check_cmd)
        self.controller2_status = ret['return']

    def create_data(self):
        """
        Create a db, table and row
        """
        self.value = randint(0, 1000)
        create_db = "mysql -e 'CREATE DATABASE qe;'"
        create_table = "mysql qe -e 'CREATE TABLE qe(value int);'"
        create_row = "mysql qe -e 'INSERT INTO qe(value) VALUES ({0})'".format(
            self.value)

    def check_data(self):
        """
        Check data migrated
        """
        get_data = "mysql qe -e 'SELECT value FROM qe\G'"
        drop_db = "mysql -e 'DROP DATABASE qe\G'"
        ret = controller.run_cmd(get_data)
        data = ret['return']
        if self.value in data:
            self.data_replication = True
        controller.run_cmd(drop_db)

    def run_tests(self):
        """
        Check mysql replication
        """
        check_status()
        create_data()
        check_data()


    def collect_results(self):
        """
        Collect results
        """
        if 'fail' in self.controller1_status if 'fail' in self.controller2_status:
            util.logger.error("Status Failed")
        else:
            util.logger.info("Status Passed")
