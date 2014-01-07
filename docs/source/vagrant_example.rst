.. _tutorial:

Vagrant web project example
===========================

.. toctree::
    :hidden:
    vagrant_example

In this example we will use web.py framework to run their `Todo-list example <http://webpy.org/src/todo-list/0.3>`_ in a Vagrant box.
This includes installing all dependencies, importing database schema and setting up appropriate configuration.

For this tutorial you will need to install on your machine:

* VirtualBox - http://www.virtualbox.org
* Vagrant - http://www.vagrantup.com
* OpenSSH for Windows (optional) - http://sshwindows.sourceforge.net

.. warning:: I'm using PuTTy, but for this tutorial I've installed OpenSSH to check everything is running fine.
 This also wiped out my %PATH% and the only thing left was OpenSSH itself :),
 so make a backup I'm not sure if this was due my error or because of OpenSSH.

After you are ready with this get our vagrant example from https://github.com/avladev/pypro/examples/vagrant_todo somewhere on your drive.

Project structure is::

    /vagrant_todo

        /provision                  // Here lives pypro recipes and settings

            /data                   // Data folder is not required by pypro, we use it to store any data files
                db.sql              // Database schema for todo-list app

            /recipes
                config.py           // Recipe which acts as global config file for our recipes
                dependencies.py     // Recipes for dependencies needed by the project
                mysql.py            // Recipes for installing and running some useful mysql commands
                project.py          // Recipes for producing /todo/config.py file
                utils.py            // General useful tools

            /settings
                config.ini          // Settings for our global config
                mysql.ini           // Settings for mysql mainly for root password

            suite.ppr               // Suite file with each step

        /todo                       // This is web.py todo-list app with slight change of configuration to be outside of model.py

            /templates              // HTML views
                base.html
                index.html

            model.py                // Model for interacting with mysql db
            todo.py                 // The app itself

        Vagrantfile                 // Vagrant file for running our machine


For this tutorial we will use:

* Windows as host machine
* Ubuntu as guest machine
* Vagrant up


Vagrant
=======

Vagrant is a tool which integrates with VirtualBox to **"Create and configure lightweight, reproducible, and portable development environments."**
This tutorial will only touch a couple of concepts which you will need to run this example.

.. note:: If you are not familiar with Vagrant check its documentation at http://docs.vagrantup.com

So Vagrant is very useful when you want to work on your projects in isolated VM environment, its goal is to make our lives easier by
providing a couple of useful commands to do that.

Although we will only use `vagrant up` command because of pre existing Vagrantfile bellow are are most used Vagrant commands.

====================    =================================================================================================================
Basic Vagrant commands
=========================================================================================================================================
vagrant init            Creates `Vagrantfile` file in your current directory. This file is a Vagrant configuration file for your project.
vagrant add box url     Downloads VirtualBox template virtual disk with pre-installed OS.
vagrant up              Starts your virtual machine based on the box you specified.
vagrant halt            Shuts down your VM.
vagrant destroy         Destroys your virtual disk. Next time you ``up`` this project it will start with fresh box copy.
====================    =================================================================================================================

    ::


Lets get started
=================

Running the VM
--------------

I assume you already have installed VirtualBox, Vagrant and OpenSSH on your Windows machine. The next step is to open a command prompt and
navigate to the directory /vagrant_todo you downloaded.

To create a new VM instance execute::

    ``vagrant up``

This command will look for Vagrantfile and will download precise32 box and boot your machine based on it.

.. note:: Your machine is Ubuntu precise32 with predefined IP address 10.10.10.10. This is defined in Vagrantfile you can change it if you want.

Next step is to login trough SSH to your machine, Vagrant uses RSA key for authentication to the machine.::

    ``vagrant ssh``

OpenSSH will ask you for a passphrase which have to be empty so just press enter. For password use **vagrant**::

    Enter passphrase for key 'C:/Users/<User>/.vagrant.d/insecure_private_key':
    vagrant@127.0.0.1's password: vagrant

This will log you in your VM.

.. note::

    If you are using PuTTy note that Vagrant RSA key should be converted with PuTTyGen in order to work with PuTTy.
    The key is located in ``C:\Users\<User>\.vagrant.d\insecure_private_key`` see appendix for more information.


Installing pip and pypro
------------------------

Ubuntu should come with python installed by default, but without pip or easy_install. So we have to install it::

    ``sudo apt-get install python-pip``

Next step is to install pypro packages::

    ``sudo pip install pypro``

If everything is successful you should be able to run ppr.py command in the shell. Lets try::

  ``ppr.py``

Result should be a complain that there is no recipes directory::

    [Error] No recipes directory found!

That's fine.


Vagrant shared folder
---------------------

Vagrant shares the folder containing the Vagrantfile between host and guest machines.
So you should be able to find this in ``/vagrant`` on the guest machine::

  ``cd /vagrant``
  ``ls -la``

As you can see this is our example folder available in the guest machine::

    total 21
    drwxrwxrwx  1 vagrant vagrant 4096 Jan  6 20:54 .
    drwxr-xr-x 23 root    root    4096 Jan  6 21:07 ..
    drwxrwxrwx  1 vagrant vagrant 4096 Jan  6 19:25 provision
    drwxrwxrwx  1 vagrant vagrant 4096 Jan  6 01:19 todo
    drwxrwxrwx  1 vagrant vagrant    0 Jan  5 23:43 .vagrant
    -rwxrwxrwx  1 vagrant vagrant 4723 Jan  6 20:54 Vagrantfile


Running the recipes
-------------------

Now the culmination of our work running our recipes. We need to ``cd`` to ``provision`` folder which contains our recipes
and from this folder to run ppr.py as root because we will install from packages trough apt-get::

    ``cd /vagrant/provision``
    ``sudo ppr.py -s suite.ppr -y``

This commands have to be executed without and error (hopefully :)).

So let's check if your app is working::

    ``cd /vagrant/todo``
    ``python todo.py``

You should see output http://0.0.0.0:8080 .
Return back to your host machine and open an browser windows and enter http://10.10.10.10:8080 this have to load the
todo-list app showing input field and submit button. Play with it if you want.

Next task is to explain all the recipes and suite file so you can learn how to setup projects like this one by yourself.

Step by step explanation
========================

The suite.ppr file
------------------

This file contains our recipes calls with comments in it. Take a look:

.. literalinclude:: ../../examples/vagrant_todo/provision/suite.ppr

This should be clear enough, so I will not explain more about it.

Recipes
-------

CheckRoot
+++++++++

This recipe just checks that we are running ppr.py as root which is useful because you can forget to run it as root
and this will give you error when trying to install packages.

UpdateAPT
+++++++++

This recipe uses ``apt-get update`` command to retrieve fresh list of all packages.

The interesting thing here if you look at the source code is ``runner.call()`` method. This method allows you to
execute system command. This method returns the command output if you need it for something.

InstallWebPy
++++++++++++

This recipe install web.py framework python package so we can run out todo-list app.


Install
+++++++

This will install mysql-server. Вe define ``root_password`` in ``mysql.ini`` settings file, so we can use it in other
recipes, we also define an static method ``root_password()`` so we can access this from other recipes.

If you look at the source code of ``Install.root_password()`` method you will se that it creates new instance of Install()
recipe and retrieves its ``root_password`` setting. This is possible also in other modules and other recipes too if you want
to access some of the settings of other recipes. This should be used with care because it creates dependency between your
recipes.


InstallMySQLdb
++++++++++++++

This installs mysql support for python needed for todo-list app to store its todos.


ExecuteSQL
++++++++++

Let see the line in the ``suite.ppr``::

    mysql.ExecuteSQL file=./data/db.sql database=@{config.db.db_name} username=root password=@{mysql.install.root_password}

This recipe creates a database with name specified in the ``config.DB`` recipe which serves as global configuration.
And then imports the ``./data/db.sql`` file into the mysql.

You can also see that we again access ``mysql.Install`` ``root_password`` so we can login into mysql as root to execute
``CREATE DATABASE`` statement and the ``db.sql`` file.


Grant
+++++

Suite line::

    mysql.Grant database=@{config.db.db_name} username=@{config.db.username} password=@{config.db.password}

This recipe creates a mysql user for our database used by todo-list app.


CreateConfig
++++++++++++

Suite line::

    project.CreateConfig source=./data/config.py destination=../todo/config.py

This one creates config file ``../todo/config.py`` based on ``./data/config.py``.
Lets take a look at ``./data/config.py``:

.. literalinclude:: ../../examples/vagrant_todo/provision/data/config.py

This is a simple python module with a couple of string variables. The interesting about it is that these @{} notations
are replaced in ``project.CreateConfig`` ``run`` method by ``pypro.core.Variables.replace(string)`` method.

.. literalinclude:: ../../examples/vagrant_todo/provision/recipes/project.py

This class method is used in pypro itself to parse and find any setting that you want. Basically it searches for @{}
notation and finds the recipe, instantiate it and replace the notation with actual value stored in the .ini file.



Appendix
========

Using PuTTy with Vagrant
------------------------

**Install and run PuTTyGen:**

1. Click "Load" button, from dropdown box select "All files" and select C:/Users/<User>/.vagrant.d/insecure_private_key
2. Then enter passphrase if needed and click "Save private key"

**Install and run PuTTy:**

1. Then open PuTTy and enter guest machine ip in host field along with port 22 then in the box below give this connection a name and save it by "Save" button
2. In the settings tree on the left side locate ``Connection > SSH > Auth and use the "Browse..."`` button to select your .ppk key generated from PuTTyGen
3. Then go back to Session and Save the connection again.
4. Close PuTTy and open it again, locate your saved connection in the list and click "Load" button, now you are ready to connect.

