import ConfigParser
import re
import os
import sys
import subprocess
import inspect
import pyprov.console
import argparse
import traceback


class Runner:
    """
    This class runs all added recipes
    """

    def __init__(self):
        self._recipes = []
        self._args_parser = None
        self._arguments = None

        # Add current folder to sys.path
        if not os.getcwd() in sys.path:
            sys.path.append(os.getcwd())

        # Check for recipes folder
        recipe_path = os.path.join(os.getcwd(), 'recipes')
        if not os.path.isdir(recipe_path):
            raise PyProvException("No recipes directory found!")

        # Check for recipes __init__.py file and create it if not present
        recipes_init_file = os.path.join(recipe_path, '__init__.py')
        if not os.path.isfile(recipes_init_file):
            f = open(recipes_init_file, 'w')
            f.close()


    @property
    def arguments_parser(self):
        """
        @rtype: argparse.ArgumentParser
        """
        if not self._args_parser:
            self._args_parser = argparse.ArgumentParser()
            self._args_parser.add_argument('arguments',
                                           help="Space separated list of parameters", type=str, nargs='*')
            self._args_parser.add_argument('-y', '--yes',
                                           help="Auto confirm on questions", action="store_true")
            self._args_parser.add_argument('-r', '--recipe',
                                           help="Run single recipe", type=str, metavar="recipe_name")
            self._args_parser.add_argument('-s', '--suite',
                                           help="Path to suite file", type=str, metavar='/path')
            self._args_parser.add_argument('-v', '--verbose',
                                           help="Verbose output", action="store_true")

        return self._args_parser

    def add_recipe(self, recipe):
        """
        @recipe: Recipe
        Add a recipe to the execution queue.
        """
        assert isinstance(recipe, Recipe), "%s is not subclass of Recipe" % recipe.__class__
        self._recipes += [recipe]

    @property
    def arguments(self):
        return self._arguments

    def _prepare(self):
        self._arguments = self.arguments_parser.parse_args()

        if self.arguments.suite:
            self._prepare_suite()
        elif self.arguments.recipe:
            self._prepare_single_recipe()
        else:
            self.arguments_parser.print_help()
            exit()

    def _prepare_suite(self):
        assert os.path.isfile(self.arguments.suite), 'Suite file not found.'

        parser = Parser(self.arguments.suite)

        for parts in parser.lines():
            recipe_parts = parts[0].split('.')
            package_name = recipe_parts[0]
            recipe_name = recipe_parts[1]

            recipe_arguments = parts[1:]
            recipe_arguments = dict(zip(recipe_arguments[0::2], recipe_arguments[1::2]))

            for key, param in recipe_arguments.items():
                recipe_arguments[key] = Variables.replace(param)

            recipe_class = None
            try:
                recipe_class = import_recipe(package_name, recipe_name, Parser.last_source, Parser.last_line)
                recipe = recipe_class(**recipe_arguments)
                self.add_recipe(recipe)
            except TypeError:
                needed = inspect.getargspec(recipe_class.__init__).args[1:]
                got = recipe_arguments
                missing = list(set(needed) - set(got))
                raise PyProvException("Wrong recipe arguments. Arguments needed: %s. Missing: %s" %
                                      (str(', ').join(needed), str(', ').join(missing)))

    def _prepare_single_recipe(self):
        package_name = self.arguments.recipe.split('.')[0]
        recipe_name = self.arguments.recipe.split('.')[-1]

        recipe_arguments = []

        for argument in self.arguments.arguments:
            recipe_arguments += Parser.parse_shell_argument(argument)

        recipe_arguments = dict(zip(recipe_arguments[0::2], recipe_arguments[1::2]))

        for key, value in recipe_arguments.items():
            recipe_arguments[key] = Variables.replace(value)

        recipe_class = None
        try:
            recipe_class = import_recipe(package_name, recipe_name)
            recipe = recipe_class(**recipe_arguments)

            self.add_recipe(recipe)

        except TypeError:
            needed = inspect.getargspec(recipe_class.__init__).args[1:]
            got = recipe_arguments
            missing = list(set(needed) - set(got))
            raise PyProvException("Wrong recipe arguments. Arguments needed: %s. Missing: %s" %
                                  (str(', ').join(needed), str(', ').join(missing)))

    def run(self):
        """ Starts recipes execution. """

        self._prepare()

        for recipe in self._recipes:
            run_recipe = True

            # Ask user whether to run current recipe if -y argument is not specified
            if not self.arguments.yes:
                run_recipe = pyprov.console.ask_bool('Run %s.%s' % (recipe.package, recipe.name), "yes")

            if run_recipe:
                recipe.run(self, self.arguments)

        if self.arguments.verbose:
            pyprov.console.out('Thanks for using pyprov. Support this project at https://github.com/avladev/pyprov')

    def call(self, command):
        """
        @command: str
        Executes shell command.
        """
        if self.arguments.verbose:
            pyprov.console.out('[Call] ', command)

        code = subprocess.call(command, shell=True, stdout=sys.stdout, stdin=sys.stdin, stderr=sys.stderr)

        if code:
            raise PyProvException("Unsuccessful system call '%s'" % command)

        return code


class Recipe:
    """ This class represents a given task called "recipe". """
    def __init__(self):
        self._settings = None
        pass

    @property
    def name(self):
        """ Returns the recipe name which is its class name without package. """
        return str(self.__class__).split('.')[-1].lower()

    @property
    def package(self):
        """
        Returns the package name of Recipe.
        This actually represents the file basename of a recipe.
        """
        return str(self.__class__).split('.')[-2].lower()

    @property
    def settings(self):
        """
        Loads the recipe settings file which is locate in:
        ./settings/{recipe_package}.ini
        """
        settings_file = os.path.join(os.getcwd(), 'settings', self.package + '.ini')

        # Loads the settings file once.
        if (not hasattr(self, '_settings') or self._settings is None) and os.path.isfile(settings_file):
            config = ConfigParser.ConfigParser()
            config.read(settings_file)

            settings = dict(config._sections)
            for key in settings:
                settings[key] = dict(config.defaults(), **settings[key])
                settings[key].pop('__name__', None)

            self._settings = SettingsDict(self, settings.get(str(self.__class__).split('.')[-1], {}))

        elif not hasattr(self, '_settings'):
            self._settings = SettingsDict(self, {})

        return self._settings

    @property
    def settings_keys(self):
        """
        Settings keys have to be defined in this dict in order to be accessed.
        The key is the setting name and the value is the setting comment.
        returns dict
        """
        raise PyProvException("Property 'settings_keys' should be defined in recipe '%s'." % self.name)

    def run(self, runner, arguments=None):
        """
        This method is executed when recipe is run.
        Each recipe should override this method.
        """
        raise PyProvException("Method 'run' not implemented in recipe.")


class SettingsDict(dict):

    def __init__(self, recipe, iterable=None):
        dict.__init__(self, iterable)
        self.recipe = recipe

    def get(self, k, d=None):
        if self.recipe.settings_keys.get(k) is None:
            raise PyProvException("No key '%s' defined in recipe '%s.%s' settings_keys dict!" %
                                  (k, self.recipe.package, self.recipe.name))

        if not k in self:
            raise PyProvException("No key '%s' defined in './settings/%s.ini'" %
                                  (k, self.recipe.package))

        return Variables.replace(dict.get(self, k, d))


class Parser:
    """
    This class parses suite files. Basic suite file structure is:
    package.RecipeClassName argument1=value1 argument2="Some complex value with spaces and = (equal) sign."
    """
    last_source = None
    last_line = None

    def __init__(self, path):
        self.path = path
        Parser.last_source = os.path.basename(self.path)
        Parser.last_line = 0

    def lines(self):
        Parser.last_line = 0
        with open(self.path) as f:

            # execute file line by line
            for line in f:
                Parser.last_line += 1
                line = line.strip()

                # skip empty line
                if not len(line):
                    continue

                # skip commented line (ones that don't begin with letter)
                if not re.match('\w', line[0]):
                    continue

                yield self.parse_string(line)

    @staticmethod
    def parse_shell_argument(string):
        return string.split('=', 1)

    @staticmethod
    def parse_string(string):
        string = string.strip()

        parts = []
        char_buffer = ""
        quote = None
        escape = False
        for char in string:
            if char == '"' or char == "'":
                # remove quote escape character
                if escape:
                    char_buffer = char_buffer[0:-1] + char
                    continue

                # opens quote
                if not quote:
                    quote = char
                    continue

                # closes quote
                if quote == char:
                    quote = None
                    parts.append(char_buffer)
                    char_buffer = ""
                    continue

            if char == "\\":
                escape = True
            else:
                escape = False

            # split by \s and = if not in quote
            if (char == " " or char == "=") and not quote:
                parts.append(char_buffer)
                char_buffer = ""
                continue

            char_buffer += char

        # write buffer leftovers
        if len(char_buffer):
            parts.append(char_buffer)

        filtered = []

        for index, part in enumerate(parts):
            part = part.strip()
            if not part or part == '=':
                continue

            if part[0] in ["'", "'"] and part[-1] in ["'", '"']:
                part = part[1:-1]

            filtered.append(part)

        return filtered


class Variables:

    _recipes = {}

    def __init__(self):
        raise PyProvException("This class should not be instantiated!")

    @staticmethod
    def replace(string):
        regex = r'\@\{([a-z\.\_\-0-9]+)\}'
        return re.sub(regex, Variables._replace_variable, str(string), flags=re.IGNORECASE)

    @staticmethod
    def _replace_variable(match):
        parts = match.group(1).split('.')

        if len(parts) < 3:
            raise PyProvException("Invalid variable '%s'!" % match.group(0))

        module, recipe_name, variable = parts
        cache_key = module + '.' + recipe_name

        if not cache_key in Variables._recipes:
            Variables._recipes[cache_key] = import_recipe(module, recipe_name, Parser.last_source, Parser.last_line)()

        return Variables._recipes[cache_key].settings.get(variable)


def import_recipe(package_name, recipe_name, source=None, line=None):

    source = 'unknown' if not source else source
    line = 'unknown' if not line else line

    package_name = 'recipes.%s' % package_name
    recipe_class = None

    try:
        # load recipe module and run instantiate the class
        __import__(package_name)

        for i, j in inspect.getmembers(sys.modules[package_name]):
            if i.lower() == recipe_name.lower():
                recipe_class = i

        if not recipe_class:
            raise AttributeError()

        recipe_class = getattr(sys.modules[package_name], recipe_class)

        if not recipe_class:
            raise AttributeError()

        return recipe_class

    except ImportError as e:
        raise PyProvException("Error loading package for recipe '%s.%s'. File '%s' line %s.\n"
                              "%s" % (package_name, recipe_name, source, line, traceback.format_exc()))
    except AttributeError:
        # missing recipe module or class
        raise PyProvException("Recipe '%s' not found. File '%s' line %s." %
                              (recipe_name, source, line))


class PyProvException(Exception):

    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)

def exception_handler(exctype, value, traceback):
    """
    This exception handler catches KeyboardInterrupt to cancel the Runner and
    also stops the Runner in case of an error.
    """
    if exctype == KeyboardInterrupt:
        pyprov.console.out('')  # Adds a new line after Ctrl+C character
        pyprov.console.err('Canceled')
    elif exctype == PyProvException:
        pyprov.console.err('[Error] ', value.message)
        exit()
    else:
        sys.__excepthook__(exctype, value, traceback)

sys.excepthook = exception_handler