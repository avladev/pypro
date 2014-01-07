import pypro.core


class InstallWebPy(pypro.core.Recipe):

    def run(self, runner, arguments=None):
        runner.call('pip install web.py')


class InstallMySQLdb(pypro.core.Recipe):

    def run(self, runner, arguments=None):
        runner.call('apt-get install -y python-mysqldb')