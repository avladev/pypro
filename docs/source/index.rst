.. pypro documentation master file, created by
   sphinx-quickstart on Sun Jan 05 17:45:21 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Pypro Documentation
===================

Pypro is a simple tool for running python code organized in classes called recipes.
It can be used to automate tedious tasks, provisioning systems and everything you want to automate.

It was designed as a simple tool to help easily provision new Vagrant machines for a web projects.
After machine is ready you logon and run your recipes. The recipes installs all dependencies on your machine.
Each project is checked out and configured in matter of minutes and you can start working on your tasks.


.. toctree::
    :hidden:

    helloworld_example
    vagrant_example

.. warning:: This project is not mature enough to be used in production environments. Please test it before using
 your important data with it.

.. important:: If you want to rewrite this documentation in better English please clone the dev branch
 https://github.com/avladev/pypro/tree/dev and post a pull request. For bug reports, feature requests and so on
 https://github.com/avladev/pypro/issues


Installation
============

Pypro comes as standard pypi package, so you can install it as any other package trough easy_install or pip.
You also can download the latest version from the git repo at https://github.com/avladev/pypro and install it
from the setup.py file provided.

Basic concepts
==============

* Runner - ppr.py script which runs pypro engine
* Recipe - Class which defines code to be executed
* Settings - An optional .ini file with settings for each recipe module
* Suite - A list of recipes to be executed
* @{} notation - A way to reference the settings on call time or in the settings file itself

Quick start
===========

Pypro is a simple tool but it relies on a couple of conventions that are better explained trough examples.
There is an examples folder in the package which contains all required files and folders for the tutorials.

* `HelloWorld example <helloworld_example.html>`_
* `Setting up a simple web app with Vagrant <vagrant_example.html>`_
