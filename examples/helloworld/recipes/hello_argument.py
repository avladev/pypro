import pypro.core


class HelloArgument(pypro.core.Recipe):

    def __init__(self, what):
        self.what = what

    def run(self, runner, arguments):
        print("Hello %s!" % self.what)