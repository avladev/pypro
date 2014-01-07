import pypro.core
import os


class UpdateAPT(pypro.core.Recipe):

    def run(self, runner, arguments=None):
        runner.call('apt-get update')

class CheckRoot(pypro.core.Recipe):

    def run(self, runner, arguments=None):

        if os.getuid() != 0:
            raise Exception("You have to be root to be able to execute all of the recipes!")