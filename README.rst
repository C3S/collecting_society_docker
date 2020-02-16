===============================
Collecting Society Docker Setup
===============================

Docker development and deployment setup for collecting society services.


Overview
========

The setup creates and maintains `Docker <http://docs.docker.com>`
containers for development and production use.
`Docker-compose <https://docs.docker.com/compose/>`, is used as a creator
and configurator for the Docker containers:

* db: Postgres database
* tryton: Tryton server
* nginx: Web server
* portal: Pyramid web portal
* api: Pyramid web api
* processing: File processing
* selenium: Headless browser for integration tests


Requirements
============

A Linux or OS X system, `docker <https://docs.docker.com/engine/installation/>`,
`docker-compose  <https://docs.docker.com/compose/install/>`
and `git <http://git-scm.com/downloads>`. Summary::

    $ sudo apt-get install git docker docker-compose
    $ sudo usermod -aG docker $USER
    $ newgrp docker


Setup
=====

Clone this repository into your working space::

    $ cd MY/WORKING/SPACE
    $ git clone https://github.com/C3S/collecting_society_docker.git
    
All setup and maintenance tasks are done in the root path of the
``collecting_society_docker/`` repository::

    $ cd collecting_society_docker

Choose the environment to build:

1. For production environment switch to the ``master`` branch::

    $ git checkout master

2. For development environment switch to the ``develop`` branch::

    $ git checkout develop

Update the environment, clone/pull development repositories::

    $ ./update

Build docker containers::

    $ docker-compose build

The initial build of the containers will take some time.
Later builds will take less time.

Adjust environment files for containers, if neccessary. Sane defaults for
a development setup are given:

    * ``./api.env``
    * ``./portal.env``
    * ``./processing.env``
    * ``./selenium.env``
    * ``./erpserver.env``

Change the password for the *admin* user in
``./volumes/shared/config/trytond/passfile``

Start containers::

    $ docker-compose up

This starts all service containers.


Clients
=======

Web
---

The number of *portal* services is implemented scalable.
Because of this it is not possible to hard code the external port number of
a service.
So all services use *random external ports on the host system*.
The tool `nginx-proxy<https://github.com/jwilder/nginx-proxy>` is used as a
reverse proxy and load-balancer to the *portal* services host on *port 81*.

.. note: To connect a client to a particular service, it is
    needed to find out the hosta nd the port of the service.
    Use the script ``./show_external_urls`` or ``docker-compose ps``
    to find the port of a particular service.

Prior to the connection via browser, your /etc/hosts should contain
repertoire.test and api.repertoire.test pointing to 0.0.0.0

Connecting the portal, point your browser to::
    http://repertoire.test:81

Connecting the api, point your browser to::
    http://api.repertoire.test:81

Connecting a specific instance of the portal service, point your browser to::
    http://localhost:<random external port on host system>/login

Tryton
------

To connect to trytond you can use one of the several Tryton client
applications or APIs.
For back-office use of the application the Gtk2 based Tryton client is
recommended.

Install the client application with the name *tryton* or *tryton-client* in
Version 3.4.x from your Linux distribution.
You can also use the source, OS X, or Windows packages or binaries found here:
`<http://www.tryton.org/download.html>`

On the host system connect to::

    server: localhost
    port: 8000
    database: c3s
    user: admin
    password: admin

.. note:: Tryton server and the client are required to have the same version
    branch (actual 3.4.x).


Using containers
================

Services
--------

For development purposes it is convenient to have the possibility to debug the
running code.
To start only the necessary services for developing a service
use e.g::

    $ docker-compose run --rm --service-ports portal execute deploy-portal
    $ docker-compose run --rm --service-ports api execute deploy-api
    $ docker-compose run --rm --service-ports erpserver execute deploy-erpserver


The portal service is started with ``execute`` inside a portal container.
The --rm parameter for run avoids docker from collecting an increasing amount of volumes.
The tryton service can be started with::

    $ docker-compose run --rm --service-ports erpserver execute deploy-erpserver

The flag ``service-ports`` runs the container and all its dependecies
with the service's ports enabled and mapped to the host.
For development is the benefit of starting a service with
``docker-compose run --rm --service-ports <service>`` vs ``docker-compose up``
the possibility to communicate with a debugger like pdb.

A similar topic is to start a shell in a container.
To manually examine the operating system of a container, just run a shell in
the container::

    $ docker-compose run --rm portal /bin/bash

.. warning:: Manual changes are not persisted when closing a container.
    All changes are reset.

.. note:: The console is always opend in a freshly build of the service and
    does not connect to a running container. To enter a running container use
    ``docker exec``. See below for further instructions.

*execute* is a command line tool to setup and maintain services in a container.
To start the ``execute`` command from inside a container the
``docker-compose run`` must be removed from the following examples.

Get acquainted with ``execute`` a command driven tool which performs tasks on
container start::

    $ docker-compose run --rm portal execute --help
    $ docker-compose run --rm portal execute <COMMAND> --help

Database
--------

Update all modules in an existing database::

    $ docker-compose run --rm erpserver execute update

Update specific modules in an existing database::

    $ docker-compose run --rm erpserver execute update  \
        -m MODULE_NAME1[,MODULE_NAME2,…]

E.g.::

    $ docker-compose run --rm erpserver execute update  \
        -m party,account,collecting_society

Note: When developing and changing the db model, you probably want to try 
the above first, because this is the quickest way to adapt db changes. 
If you run into errors, it is a good idea to stop your containers and do a 
    $ docker-compose run erpserver execute db-delete.
If a db build seems to hang, look for a 'running_db_creation.delete_me' 
locking file in the base folder.

Examine and edit a database, use::

    $ docker-compose run --rm erpserver execute db-psql

Backup a database::

    $ docker-compose run --rm erpserver execute db-backup  \
        > `date +%F.%T`_DATABASE_NAME.backup

Delete a database::

    $ docker-compose run --rm erpserver execute db-delete

Create a new database::

    $ docker-compose run --rm erpserver execute db-create

Setup test data::

    $ docker-compose run --rm erpserver execute db-test-setup

Setup demo data::

    $ docker-compose run --rm erpserver execute db-demo-setup

Rebuild a database::

    $ docker-compose run --rm erpserver execute db-rebuild

Service Scaling
---------------

To scale increasing load it is possible to start more service containers on
demand::

    $ docker-compose scale portal=2 erpserver=3 db=1

To scale decreasing load it is possible to stop service containers on demand::

    $ docker-compose scale erpserver=2

Lookup all host ports in use::

    $ /path/to/collecting_society_docker/show_external_urls

… or use ``docker-compose ps`` as an alternative.

Lookup a specific host port in use::

    $ docker-compose --index=1 port tryton 8000

Maintenance After Update
------------------------

Some changes in the container setup require a rebuild of the whole system.

Update the environment as usual::

    $ cd collecting_society_docker
    $ ./update

Build containers, this time without a cache::

    $ docker-compose build --no-cache

Start containers::

    $ docker-compose up


Deployment
==========

Monitoring
----------

To monitor all running containers use::

    $ watch ./monitor

.. note:: The monitoring abilities are limted to system and user cpu and
    rss+cache size. The most informative metrics to use for monitoring
    are a moving target.


Development
===========

The general Python requirements are provided by default Debian packages from
Jessie (actual testing) if available, otherwise from PyPI.
Packages under development are located in ``./shared/src`` and can be edited on 
the host system, outside the containers.
For developer convenience all Tryton modules use a git mirror of the upstream
Tryton repositories.
For this setup the Tryton release branch 3.4 is used.

Architecture
------------

This repository is build by the following files and directories::

    ├── shared  # This directory is mapped into portal and tryton container
    │   ├── execute  # Maintenance Utility for containers
    │   ├── etc
    │   │   ├── requirements-portal.txt  # Pip requirements for portal service
    │   │   ├── requirements-tryton.txt  # Pip requirements for Tryton service
    │   │   ├── scenario_master_data.txt # Demo data script
    │   │   ├── trytond.conf  # Configuration file for Tryton service
    │   │   └── trytonpassfile  # Password file for Tryton admin user
    │   ├── src  # Source repositories, edit here
    │   │   ├── account
    │   │   ├── account_invoice
    │   │   ├── ...
    │   └── var  # upload directory for tryton webdav service
    │       └── lib ...
    ├── CHANGELOG
    ├── config.py  # Configuration for paths and reporitories
    ├── Dockerfiles  # Definition of service container images
    │   ├── portal ...
    │   └── tryton ...
    ├── docker-compose.yml  # docker-compose configuration
    ├── postgresql-data ...  # postgresql database data files
    ├── README.rst  #*this file*
    ├── show_external_urls  # helper script to show used external urls
    └── update  # Update script for repositories and file structure

Packages and Debs
-----------------

This setup maintains three levels of package inclusion:

    1. Debian packages
    2. Python packages installed with pip
    3. Source repositories for development purposes

Source packages for the development are available as git repositories are
stored in ``config.py`` in variable ``repositories``::

    (
        git repository url or None.
        git clone option, required if repository is given.
        relative path to create or clone.
    ),

These packages are cloned or updated with the ``./update`` command and must
be pip installable.
To install a source repository package in a container, it is be declared in
*one* of the ``shared/etc/requirements*.txt`` files.

.. note:: The ``requirements-portal.txt`` inherits the
    ``requirements-tryton.txt``.
.. note:: The ``config.py`` can be used to create empty directories, too.

Debian and Python packages are included in one of the ``Dockerfiles``:

    * tryton
    * portal

.. note:: Add source repository packages only when they are realy needed for
    development.

Remove Database
---------------

The database files are stored in ``postgresql-data``.
To rebuild a new database use the following pattern::

    $ docker-compose stop db
    $ docker-compose rm db
    $ sudo rm -rf postgresql-data/
    $ mkdir postgresql-data

.. warning:: All data in this database will be deleted!


Testing
=======

Tryton
------

To run tests (for e.g. module collecting_society) in the tryton container use::

    $ docker-compose run --rm erpserver sh -c \
          'execute pip-install erpserver \
          && export DB_NAME=:memory: \
          && python /shared/src/trytond/trytond/tests/run-tests.py -vvvm collecting_society'

(If the container already runs, use "exec" instead of "run --rm") 
To run the master setup again, use::

    $ docker-compose run --rm erpserver sh -c \
          'execute pip-install erpserver \
          && python -m doctest -v data/master.txt'

To run the demo setup again, use::

    $ docker-compose run --rm erpserver sh -c \
          'execute pip-install erpserver \
          && python -m doctest -v etc/scenario_test_data.txt'


Portal
------

Create a database template, which will be copied and used for tests::

    $ docker-compose run --rm --use-aliases -e ENVIRONMENT=testing portal \
        execute create-test-db

Run all tests in PATH (optional) with nosetests PARAMETER (optional)::

    $ docker-compose run --rm --use-aliases -e ENVIRONMENT=testing portal \
        execute run-tests [--path=PATH] [PARAMETER]

Run all tests for portal_web + plugins::

    $ docker-compose run --rm --use-aliases -e ENVIRONMENT=testing portal \
        execute run-tests

Run all tests for portal_web + plugins quiet, drop into pdb on errors::

    $ docker-compose run --rm --use-aliases -e ENVIRONMENT=testing portal \
        execute run-tests --quiet --pdb

Run only tests for portal_web::

    $ docker-compose run --rm --use-aliases -e ENVIRONMENT=testing portal \
        execute run-tests --path src/portal_web

Run only unittests of portal::

    $ docker-compose run --rm --use-aliases -e ENVIRONMENT=testing portal \
        execute run-tests --path src/portal_web/portal_web/tests/unit

Run a specific unittest for a model of portal::

    $ docker-compose run --rm --use-aliases -e ENVIRONMENT=testing portal \
        execute run-tests --path \
        src/portal_web/portal_web/tests/unit/models.py:TESTCLASS.TESTMETHOD

For repeated testing without recreating the container every time, start the
container once and run the tests from within::

    $ docker-compose run --rm --use-aliases -e ENVIRONMENT=testing portal bash
    $ execute run-tests [--path=PATH] [PARAMETER...]

Debugging with ptvsd
---------------------

If you use Visual Studio Code as your editor, you would want to install the 
Remote Containers extension, so you can work directly in the docker containers, 
including source level debugging from within VS Code. Just make sure that 
'ENVIRONMENT' is set to 'development' in the resp. containers .env file found 
in the shared folder, then cd to collecting_society_docker and start VSCode 
with *"code ."*. The necessary .devcontainer.json and launch.json files are 
already included in the repositories.

To start debugging a container, click on the toast notification that will come 
up in the bottom right corner or click on the green field in the lower left 
corner of VS Code and select 'Remote-Containers: Reopen in Container'. Then 
make sure the Python extension is installed in the container's VS Code instance 
and reload, if necessary. *Git History* and *GitLens* are recommended but will 
require you to *"apt-get install git"* in the container. To start Debugging, 
press Ctrl-Shift-D to open the debug sidebar and select the debug configuration 
in the drop-down box on the top, e.g. *'Portal Attach'*. (Settings for 
attaching the container can be adjusted in the file 
*/shared/.vscode/launch.settings*.) Press the play button left to the debug 
config drop-down box and a debug toolbar should appear.

**Important note**: If you wish to debug other containers besides the default 
*portal*, e.g. *api* or *processing*, change the *service* entry in 
.devcontainer.json accordingly, otherwise you will experience 'connection 
refused' errors. The *service* entry in .devcontainer.json will determine which 
container is being selected by the *Remote-Containers* plugin.

Debugging with winpdb
---------------------

To allow the winpdb debugger to attach to a portal script, uncomment:: 

    #RUN apt-get update && apt-get install -y winpdb

in Dockerfiles/portal/Dockerfile and in your python file insert::

    import rpdb2; rpdb2.start_embedded_debugger("password", fAllowRemote = True)

Make sure to open a port for the remote debugger in docker-compose.yml::

    ports:
      - "51000:51000"

Install winpdb also outside the container and run it::

    $ sudo apt-get install -y winpdb
    $ winpdb

The processing container can be setup for debugging the same way.
Make sure to only enable either of the both containers for debugging, not both 
the same time.

Sphinx Documentaion
===================

Sphinx doesn't just parse the code but rather wants to start the modules.
This is why there exists a special documentation container you can build with

    $ scrips/docs --build

Once built, you may ommit the --build option to rebuild the docs from
the modules .rst files (e.g. README.rst) and the common .rst files in
shared/docs/source. Don't edit the .rst files in subfolders of source
because those are copied or generated by autoapi. If you have not 
changed any .py files, you can ommit the autoapi step and speed up the
Sphinx build by entering

    $ scrips/docs --no-autoapi

If you have work to do inside the container, start it like this:

    $ docker-compose -f docker-compose.documentation.yml run --rm documentation /bin/bash

or enter it using

    $ docker-compose -f docker-compose.documentation.yml exec documentation /bin/bash

if you have left the container running before by ommiting --rm or by
starting it with:

    $ scrips/docs --keep

In the container, as alternative to scripts/docs from the outside, enter:

    $ cd docs
    $ ./build.sh

or just

    $ cd docs
    $ make html

to skip the autoapi step, if you haven't done changes to the python source
code.

To shut down the container enter:

    $ scrips/docs --down

Once built, the docs can be viewed (from outside the container) like this:
 
    $ firefox volumes/shared/docs/build/html/index.html

Problems
========

Couldn't connect to Docker daemon
---------------------------------
Docker-compose cannot start container <id> port has already been allocated
--------------------------------------------------------------------------

If docker fails to start and you get messages like this:
"Couldn't connect to Docker daemon at http+unix://var/run/docker.sock
[...]" or "docker-compose cannot start container <docker id> port has already
been allocated"

1. Check if the docker service is started::

    $ /etc/init.d/docker[.io] stop
    $ /etc/init.d/docker[.io] start

2. Check if any user of docker is member of group ``docker``::

    $ login
    $ groups | grep docker

Bad Fingerprint
---------------

If the Tryton client already connected the *tryton*-container, the fingerprint
check could restrict the login with the message: Bad Fingerprint!

That means the fingerprint of the server certificate changed.
In production use, the ``Bad fingerprint`` alert is a sign that someone
could try to *fish* your login credentials with another server responding your
client.
Ask the server administrator if the certificate is changed.

Close the Tryton client.
Check the problematic host entry in ``~/.config/tryton/3.4/known_hosts``.
Add a new fingerprint provided by the server administrator or
simply remove the whole file, if the setup is not in production use::

    rm ~/.config/tryton/3.4/known_hosts

Engine Room
-----------

This is a collection of docker internals.
Good to have but seldom useful.

Show running container (docker-compose level), e.g. ::

    $ docker-compose ps
    Name          Command                          State  Ports
    --------------------------------------------------------------------
    c3s_db_1      /docker-entrypoint.sh postgres   Up     5432/tcp
    c3s_portal_1  execute deploy-portal            Up     6543->6543/tcp
    c3s_tryton_1  execute deploy-erpserver c3s     Up     8000->8000/tcp

Use docker help::

    $ docker help

Show running container (docker level)::

    $ docker ps

Enter a running container by id (Docker>=1.3;Kernel>3.8)::

    $ docker exec -it <container-id> bash

.. note:: The docker containers are usually stored under ``/var/lib/docker``
    and can occupy some gigabyte diskspace.

Docker is memory intensive. To Stop and remove all containers use::

    $ docker stop $(docker ps -a -q)
    $ docker rm $(docker ps -a -q)

Remove images ::

    $ docker rmi $(docker images -f "dangling=true" -q)

In case you need disk space, remove all local cached images::

    $ docker rmi $(docker images -q)

Should images not been removed, try the -f (force) switch.


Copyright / License
===================

For infos on copyright and licenses, see ``./COPYRIGHT.rst``


References
==========

* http://crosbymichael.com/dockerfile-best-practices.html
* http://crosbymichael.com/dockerfile-best-practices-take-2.html
* https://crosbymichael.com/advanced-docker-volumes.html
* http://blog.jacius.info/git-submodule-cheat-sheet/
