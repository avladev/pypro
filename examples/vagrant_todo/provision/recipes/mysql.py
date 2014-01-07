import pypro.core
import os


class Install(pypro.core.Recipe):

    def __init__(self):
        self.settings_keys = {
            'root_password': 'The password for root required by mysql installation'
        }

    def run(self, runner, arguments=None):
        root_password = self.settings.get('root_password')

        if not root_password:
            raise Exception("No password for root user specified!")

        # Sets the password (not quite sure what it does but it works,
        # because installer does not specify an option for this)
        runner.call('echo "mysql-server-5.5 mysql-server/root_password password %s" | debconf-set-selections' % root_password)
        runner.call('echo "mysql-server-5.5 mysql-server/root_password_again password %s" | debconf-set-selections' % root_password)

        # Install mysql server
        runner.call('apt-get install -y mysql-server-5.5')

    @staticmethod
    def root_password():
        return Install().settings.get('root_password')


class ExecuteSQL(pypro.core.Recipe):

    def __init__(self, file, database, username, password):
        self.file = file
        self.database = database
        self.username = 'root'
        self.password = Install.root_password()

    def run(self, runner, arguments=None):

        if not os.path.isfile(self.file):
            raise Exception("SQL file %s does not exists!" % self.file)

        create = 'mysql -u%s -p%s -e"CREATE DATABASE IF NOT EXISTS %s"' % (self.username, self.password, self.database)
        runner.call(create)

        command = 'mysql -u%s -p%s %s < %s' % (self.username, self.password, self.database, self.file)
        runner.call(command)


class Grant(pypro.core.Recipe):

    def __init__(self, database, username, password):
        self.database = database
        self.username = username
        self.password = password

    def run(self, runner, arguments=None):
        mysql_command = "GRANT ALL ON %s.* TO '%s'@'localhost' IDENTIFIED BY '%s'" %\
                        (self.database, self.username, self.password)

        command = 'mysql -uroot -p%s -e "%s"' % (Install.root_password(), mysql_command)
        runner.call(command)

