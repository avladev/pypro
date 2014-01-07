import pypro.core

class HelloWorld(pypro.core.Recipe):

    def run(self, runner, arguments):
        print("Hello World!")