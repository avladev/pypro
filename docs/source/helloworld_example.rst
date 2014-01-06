Hello world example
===================

.. toctree::

Before we can begin you need the https://github.com/avladev/pypro/examples/helloworld folder somewhere on you drive.

The structure of this example is the same for each project you gonna make::

    /helloworld

        /recipes
            hello_world.py
            hello_argument.py
            hello_settings.py

        /settings
            hello_settings.ini

        suite.ppr

There are ``/recipes`` and ``/setting`` folders which are required by default.

Recipes
=======

Recipes folder holds all of your recipes for your project. For example you can put all recipes for managing your
mysql installation in ``/recipes/mysql.py`` module.
This file can hold as many recipes as you want. For example you can have: ``CreateUser``, ``Restart``, ``Dump``,
``Restore``, ``ExecuteSQL`` recipes lives in this module.

Recipe itself is a class extending :class:`pypro.core.Recipe` and living in module inside a directory ./recipes in cwd.
Each recipe should override the run method.

The following code shows a simple HelloWorld example.

.. literalinclude:: ../../examples/helloworld/recipes/hello_world.py


Runner
======

Pypro comes with a simple script called ``ppr.py`` (name comes from "pypro runner")
which is your tool for executing your recipes.

To run the HelloWorld recipe you need to specify ``-r recipe_module.RecipeClassName`` option::

    ppr.py -r hello_world.HelloWorld

This will run the runner and you will be asked whether you want to execute this recipe. Hit <ENTER> and
the recipe will be executed giving you an output::

    Run hello_world.helloworld [yes]:
    Hello World!


Recipe arguments
================

Recipes can also accept arguments when called. The arguments are passed to recipe ``__init__`` method when
instantiated. For example see ``helloworld/recipes/hello_argument.py``

.. literalinclude:: ../../examples/helloworld/recipes/hello_argument.py

This recipe accepts ``what`` as argument which is stored in instance variable ``self.what`` then its used
when recipe is executed.

To run recipe which accepts argument you pass it as ``key=value`` pair after the name of the recipe.::

    ppr.py -r hello_argument.HelloArgument what=programmer

You should see this output::

    Run hello_argument.hello [yes]:
    Hello programmer!

This is useful when you want to reuse your recipe in different contexts. For example you can have just one recipe for
printing text to user screen and you can change its arguments to control the text it prints.

The space and equal sign characters are used by the parser to split your arguments.
To use complex string with these characters you should quote it in double quotes.
The string can contain quotes itself, but you have to escape them with backslash "\". For example::

    ppr.py -r hello_argument.HelloArgument what="\"smart\" programmer"

You should get::

    Run hello_argument.helloargument [yes]:
    Hello "smart" programmer!


Recipe settings
===============

In addition to call arguments there is another feature which is called settings. Settings are recipe specific
``key=value`` pairs stored in an .ini file under ``./settings`` folder. These settings are useful for configuration of
your recipes.

Example of this feature can be found in ``helloworld/recipes/hello_settings.py``

.. literalinclude:: ../../examples/helloworld/recipes/hello_settings.py

The first thing to know is that each setting is explicitly defined in an dict ``self.settings_keys``
where the ``key`` is the ``key`` in the .ini file and the ``value`` is a comment for what you use this setting.

Check ``helloworld/settings/hello_settings.ini``

.. literalinclude:: ../../examples/helloworld/settings/hello_settings.ini

This file is a standard ini file and settings keys for each recipe are defined in a section with the same
name as recipe class name. Run this recipe::

    ppr.py -r hello_settings.HelloSettings

You should get this output::

    Run hello_settings.hellosettings [yes]:
    Hello from .ini file HelloSettings section!


Recipe @{} notation
===================

You can access settings from your arguments or even between your settings files with the help of @{} notation.
Its syntax is simple ``@{recipe_module.RecipeClassName.SettingKey}``

For this example we will mix ``HelloArgument`` and ``HelloSettings`` recipes to make an example.
As we can see ``HelloArgument`` accepts its ``what`` argument from the command line so will change this and
will print what's inside ``HelloSettings`` settings file. It's very simple::

    ppr.py -r hello_argument.HelloArgument what=@{hello_settings.HelloSettings.what}

This will give us exactly the same message as ``HelloSettings`` recipe.::

    Run hello_argument.helloargument [yes]:
    Hello from .ini file HelloSettings section!

You can also use this notation as part of ``HelloArgument`` ``what`` argument message::

    ppr.py -r hello_argument.HelloArgument what="the HelloSettings.what contains: \"@{hello_settings.HelloSettings.what}\""

This feature is very useful when you have an global configuration for your project. For example you can create
an module called ``config`` and recipes ``DB``, ``WebProject`` and define their ``self.settings_keys`` dicts and
then you can reference this settings from all of your recipes. For example if you have recipe for executing sql
queries you can do::

    ppr.py -r mysql.ExecuteSQL file=./data/database.sql username=@{config.DB.username} password=@{config.DB.password}

Or::

    ppr.py -r myproject.RegenerateThumbnails thumb_dir=@{config.MyProject.thumb_dir}


Suite files
===========

It's pointless to run each recipe from command line one by one, that's why pypro have suites. Suite is a file
which contains your ordered recipes calls in the same format as we used in this tutorial.

There is just one rule:
**Only lines beginning with letter will be executed. (spaces will be trimmed from the start and the end of a line)** In this way you
can mix your recipes calls with comments and other formatting if you want.

Lets see an example suite in  ``../../examples/helloworld/suite.ppr`` (extension does not matter)

.. literalinclude:: ../../examples/helloworld/suite.ppr

To run this suite just specify ``-s suite.ppr`` option in ppr.py if you want can put and ``-y`` option
which auto accepts the default answers::

    ppr.py -s suite.ppr -y


Thanks
======

Thanks for your patience. For an real world examples visit other tutorials. This example is simple, but
exposes most of the core functionality in pypro. If you like the project and have ideas you can contribute in
the github repo at https://github.com/avladev/pypro/

Wish you happy pyproing!
