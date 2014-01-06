import pypro.core


class HelloSettings(pypro.core.Recipe):

    def __init__(self):
        self.settings_keys = {
            'what': 'What to hello'
        }

    def run(self, runner, arguments):
        print("Hello %s!" % self.settings.get('what'))