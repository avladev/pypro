.. pyprov documentation master file, created by
   sphinx-quickstart on Sun Jan 05 17:45:21 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

pyprov documentation
==================================

Table of contents

    .. toctree::
        :maxdepth: 2
        :numbered:


Introduction
============

Pyprov is a simple tool for running a python code organized in packages called recipes.
It can be used to automate tedious tasks, provisioning a systems and everything you wanted to automate.

It was designed as a simple tool to help easily provision new vagrant machines for a web projects where
after machine is ready you logon run your recipes and you development environment is ready in a matter of minutes
you can start working on your tasks.


Installation
============

Pyprov comes as standard pypi package

Recipes
=======

Each recipe is a class living in a package. Each recipe should extend :class:`pyprov.core.Recipe` class.

A minimal recipe should override at least the run method. The following code shows a typical HelloWorld example.::

    import pyprov.core
    import pyprov.console

    class HelloWorld(pyprov.core.Recipe):

        def run(self, runner, arguments):
            print("Hello World!")
            name = pyprov.console.ask("What's your name?")
            pyprov.console.out("Nice to meet you %s." % name)





Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

