import pypro.core
import os


class CreateConfig(pypro.core.Recipe):

    def __init__(self, source, destination):
        self.source = source
        self.destination = destination

    def run(self, runner, arguments=None):
        # Read the template file
        content = ''
        with open(self.source, 'r') as f:
            content = f.read(os.path.getsize(self.source))

        # Replace notations with actual values
        content = pypro.core.Variables.replace(content)

        # Write the config file
        with open(self.destination, 'w') as f:
            f.write(content)