import pypro.core


class DB(pypro.core.Recipe):

    def __init__(self):
        self.settings_keys = {
            'db_name': 'Database name',
            'username': 'Username for db_name database',
            'password': 'Password for the user',
            'tables_prefix': 'Prefix for database tables',
            'todo_table': 'The name of todo table',
        }

    def run(self, runner, arguments=None):
        raise Exception("This recipe is for configuration only!")