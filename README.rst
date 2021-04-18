===============================
Collecting Society Docker Setup
===============================

Docker development and deployment setup for collecting society services.

The main resources can be found here:

- Documentation_
- Issues_
- Wiki_

.. _Documentation: https://files.c3s.cc/csdoku/index.html
.. _Issues: https://redmine.c3s.cc/projects/collecting_society/issues
.. _Wiki: https://redmine.c3s.cc/projects/collecting_society/wiki


Overview
========

The setup creates and maintains the docker_ services for development,
deployment, testing, and documentation. The tool docker-compose_ is used as
a creator and configurator for the docker services.

.. _docker: https://docs.docker.com
.. _docker-compose: https://docs.docker.com/compose

Schema
------
::

                                                           _
                                            ------------    |
           webbrowser           tryton      |  worker  |    | Clients
               .                  .         ------------   _|
               |                  |              |         _
    -----------------------   --------------------------    |
    |      webserver      |   |        erpserver       |    | Public
    -----------------------   --------------------------   _|
         |           |            |              |         _
    ----------   ----------       |              |          |
    | webgui |   | webapi |       |              |          |
    ----------   ----------       |              |          |
         |           |            |              |          | Internal
    ----------------------------------   ---------------    |
    |             database           |   | fingerprint |    |
    ----------------------------------   ---------------   _|

.. _Table of Services:

Services
--------

+-------------+---------------------+----------------------------+-----------------+-------------------+
| Service     | Description         | Repositories               | Ports           | Volumes           |
+=============+=====================+============================+=================+===================+
| database    | Postgres DB         |                            |                 | | shared          |
|             |                     |                            |                 | | postgresql-data |
+-------------+---------------------+----------------------------+-----------------+-------------------+
| erpserser   | Trytond Server      | collecting_society_        | | 8000: jsonrpc | | shared          |
|             |                     |                            | | 8069: xmlrpc  | | trytond-files   |
|             |                     |                            | | 51005: ptvsd  |                   |
|             |                     |                            | | 51006: ptvsd  |                   |
+-------------+---------------------+----------------------------+-----------------+-------------------+
| webserver   | Nginx Server        |                            | 80: http        | | shared          |
|             |                     |                            |                 | | nginx-certs     |
|             |                     |                            |                 | | nginx-dhparam   |
|             |                     |                            |                 | | nginx-htpasswd  |
+-------------+---------------------+----------------------------+-----------------+-------------------+
| webgui      | | Pyramid Gui App   | | portal_web_              | | 6543: pserve  | | shared          |
|             | | *+Trytond Server* | | collecting_society_web_  | | 51000: ptvsd  | | trytond-files   |
+-------------+---------------------+----------------------------+-----------------+-------------------+
| webapi      | | Pyramid Api App   | | portal_web_              | | 6544: pserve  | | shared          |
|             | | *+Trytond Server* | | collecting_society_web_  | | 51001: ptvsd  | | trytond-files   |
+-------------+---------------------+----------------------------+-----------------+-------------------+
| worker      | | File Processing   | collecting_society_worker_ | 51002: ptvsd    | shared            |
|             | | *+Proteus Client* |                            |                 |                   |
+-------------+---------------------+----------------------------+-----------------+-------------------+
| fingerprint | Echoprint Server    | echoprint-server_          | | 8080: http    | | shared          |
|             |                     |                            | | 51004: ptvsd  | | echoprint-data  |
+-------------+---------------------+----------------------------+-----------------+-------------------+

.. _collecting_society_docker: https://github.com/C3S/collecting_society_docker
.. _collecting_society: https://github.com/C3S/collecting_society
.. _archiving: https://github.com/C3S/archiving
.. _portal: https://github.com/C3S/portal
.. _portal_web: https://github.com/C3S/portal_web
.. _collecting_society_web: https://github.com/C3S/collecting_society_web
.. _collecting_society_worker: https://github.com/C3S/collecting_society_worker
.. _echoprint-server: https://github.com/C3S/echoprint-server

Files
-----

.. note:: Some files and folders are created on the first run of the
    `project script`_ update command, `docs-build script`_ or
    `service-test script`_ and many are symlinks into the shared volume, as the
    files need to be accessible from within the container.

::

    ├── code/                               # service application repositories
    │   ├── collecting_society/             # (erpserver) tryton module
    │   ├── portal_web/                     # (webgui/webapi) pyramid main app
    │   ├── collecting_society_web/         # (webgui/webapi) pyramid plugin app
    │   ├── collecting_society_worker/      # (worker) file processing
    │   └── echoprint-server/               # (fingerprint) echoprint server
    │
    ├── docs/                               # documentation build
    │   └── index.html                      # main index file of the built documentation
    │
    ├── services/                           # files for docker services
    │   ├── build/                          # build environment for docker images
    │   │   ├── Dockerfile                  # multistage Dockerfile for docker images
    │   │   └── worker.cron                 # (worker) cronjob file for processing
    │   │
    │   ├── config/                         # config files for services
    │   │   ├── collecting_society.*        # (erpserver) trytond config / passfile
    │   │   ├── portal_web.*                # (webapi/gui) pyramid config
    │   │   ├── collecing_society_web.*     # (webapi/gui) pyramid plugin config
    │   │   ├── collecting_society_worker.* # (worker) worker config
    │   │   └── nginx.proxy.conf            # (webserver) additional proxy wide nginx config
    │   │
    │   ├── deploy/                         # deployment scripts for services
    │   ├── healthcheck/                    # healthcheck scripts for services
    │   ├── pip/                            # pip runtime requirements for services
    │   │
    │   └── <SERVICE>.env                   # additional envvars file for SERVICE
    │
    ├── tests/                              # testing output
    │   ├── cover_web/                      # (webgui/webapi) coverage results
    │   │   └── index.html                  # main index file of coverage results
    │   ├── cover_worker/                   # (worker) coverage results
    │   │   └── index.html                  # main index file of coverage results
    │   └── screenshots/                    # (webgui) screenshots of integration tests
    │
    ├── volumes/                            # volumes mounted into the containers
    │   ├── shared/                         # (*) main volume mounted into all containers
    │   │   ├── src/                        # repos of packages to include on runtime
    │   │   ├── ref/                        # repos of packages in docker images for reference
    │   │   │
    │   │   ├── data/                       # demodata generation module
    │   │   │   ├── csv/                    # csv files to import
    │   │   │   │   ├── <MODEL>.csv         # csv file for tryton MODEL
    │   │   │   │   └── <MODEL>.py          # script to generate the csv file for tryton MODEL
    │   │   │   ├── datasets/               # datasets to generate
    │   │   │   │   └── <MODEL>.py          # dataset for tryton MODEL
    │   │   │   ├── fingerprints/           # fingerprints for echoprint
    │   │   │   ├── uploads/                # audiofile generation and compression script
    │   │   │   └── main.py                 # main demodata generation script
    │   │   │
    │   │   ├── docs/                       # documentation sphinx build environment
    │   │   │   ├── build/                  # build of the documentation
    │   │   │   ├── source/                 # source of the documentation
    │   │   │   ├── build.sh                # sphinx build script (run in container!)
    │   │   │   └── Makefile                # sphinx Makefile
    │   │   │
    │   │   ├── tmp/                        # tmp data of services (development/testing)
    │   │   │   ├── files/                  # trytond file storage
    │   │   │   ├── logs/                   # log files for debugging
    │   │   │   ├── sessions/               # cookie session files
    │   │   │   └── upload/                 # file upload processing
    │   │   │       └── <STAGE>/            # processing / archiving STAGE of files
    │   │   │
    │   │   ├── docker-entrypoint.sh        # docker entrypoint for python based containers
    │   │   └── cli                         # main CLI script for common tasks (run in container!)
    │   │
    │   ├── echoprint-data/                 # (fingerprint) echoprint database data
    │   ├── nginx-certs/                    # (webserver) certificates
    │   ├── nginx-dhparam/                  # (webserver) dh parameters
    │   ├── postgresql-data/                # (database) postgres database data
    │   └── tryton-files/                   # (erpserver/webgui/webapi) trytond file storage
    │
    ├── .env                                # main environment variable file
    ├── project.yml                         # main project setup file
    │
    ├── project                             # updates the files/folders/repos of the project
    ├── db-rebuild                          # rebuilds the database
    ├── docs-build                          # builds the documentation of the project
    ├── service-test                        # runs the tests of the project
    ├── cli                                 # main CLI script for common tasks (run in container!)
    │
    ├── docker-compose.yml                  # main docker compose file
    ├── docker-compose.override.yml         # symlink to environment docker override file
    ├── docker-compose.development.yml      # -> docker override file for development
    ├── docker-compose.staging.yml          # -> docker override file for staging
    ├── docker-compose.production.yml       # -> docker override file for production
    ├── docker-compose.testing.yml          # standalone docker compose file for testing
    ├── docker-compose.documentation.yml    # standalone docker compose file for documentation
    │
    ├── .vscode/                            # settings for vs code
    ├── .devcontainer.json*                 # settings for vs code remote containers
    ├── .flake8                             # symlink to settings for flake8 linter
    ├── .gitignore                          # ignore patterns for git
    ├── .rgignore                           # ignore patterns for ripgrep
    │
    ├── CHANGELOG.rst                       # changelog
    ├── COPYRIGHT.rst                       # copyright
    ├── LICENSE-AGPLv3.txt                  # license
    └── README.rst                          # this readme

Docker
''''''

======================================= ===============================================================
``.env``                                Main `.env`_ environment file for service configuration
``docker-compose.yml``                  Main docker `compose`_ file with the definition of the services
``docker-compose.override.yml``         `Environments`_ variables overriding those of the main file
``services/build/Dockerfile``           Multistage Dockerfile for the `docker images`_
``volumes/shared/docker-entrypoint.sh`` Entrypoint script for python based containers
======================================= ===============================================================

Development
'''''''''''

======================================= ===============================================================
``project.yml``                         project setup configuration file for file/folder/repo tasks
``project``                             `project script`_ for project maintainance tasks
``project update``                      updates the files/folders/repos of the project
``project status``                      status of all project repositories
``project diff``                        diff of all project repositories and example files
``project pull``                        pull all project repositories
``project checkout BRANCH``             checkout BRANCH in all project repositories
``project delete BRANCH``               deletes local and remote BRANCH in all project repositories
``project commit MESSAGE``              add changed/untracked files, commit them in project repos
``project push``                        push all commits in all project repos, creates remote branches
``project merge [BRANCH]``              merges current branch of project repos into BRANCH
``project promote ENVIRONMENT``         promotes an environment branch to the next environment branch
``cli``                                 `CLI`_ script for common tasks (run within the container!)
``services/config/``                    `Application Configuration`_ files for the services
``code/``                               Symlinks to src repositories for the `application development`_
``volumes/shared/src/``                 Repos of all Tryton and collecting_society modules
``volumes/shared/ref/``                 Repos of some pinned packages we use, just for reference
======================================= ===============================================================

Data
''''

============================================ ==========================================================
``db-rebuild``                               `db-rebuild script`_ for the database and demodata
``volumes/postgresql-data``                  Files of the postgres database
``volumes/echoprint-data``                   Files of the echoprint database
``volumes/shared/data/datasets/``            `Demodata`_ generation scripts for each tryton model
``volumes/shared/data/fingerprints/``        Ingestable demo fingerprints for echoprint
``volumes/shared/data/updloads/generate.sh`` Audiofile generation and compression script
============================================ ==========================================================

Documentation
'''''''''''''

======================================= ===============================================================
``docs-build``                          `docs-build script`_ to build the `project documentation`_
``docs/index.html``                     Main index file of the built documentation
======================================= ===============================================================

Tests
'''''

======================================= ===============================================================
``service-test``                        `service-test script`_ to run all service `application tests`_
``tests/cover_*/index.html``            Html summary of coverage for webapi/webgui and worker
``tests/screenshots/``                  Screenshots of the integration tests
======================================= ===============================================================


Installation
============

To install the docker development environment from scratch, carry out the
instructions of the following sections consecutively.

Requirements
------------

- Linux or OS X system
- `git`__
- `python`__ ``>=3.7``
- `pyyaml`__
- `docker`__ ``>= 17.12.0``
- `docker-compose`__ ``>= 1.28.6``

__ https://git-scm.com/downloads
__ https://www.python.org/downloads
__ https://pyyaml.org/wiki/PyYAMLDocumentation
__ https://docs.docker.com/engine/installation
__ https://docs.docker.com/compose/install

Summary for Debian/Ubuntu::

    $ sudo apt-get install docker docker-compose git python python-yaml
    $ sudo usermod -aG docker $USER
    $ newgrp docker

Repositories
------------

In the first step, the repositories of the services have to be cloned and some
filesystem preparation tasks have to be performed. Clone the
`collecting_society_docker`_ repository into your working space::

    $ cd MY/WORKING/SPACE
    $ git clone https://github.com/C3S/collecting_society_docker.git

Switch to the root directory of the repository::

    $ cd collecting_society_docker

.. note:: All setup and maintainance tasks are performed in the root path of
    this repository.

Checkout the `Environments`_ branch to build:
``development``, ``staging``, ``production``::

    $ git checkout <ENVIRONMENT>

If you just want to try out the software, the default ``development`` branch is recommended.

Copy the main environment variable example file ``.env.example`` to `.env`_::

    $ cp .env.example .env

Adjust the following variables:

======================= ====== ======= =================================================
Variable                Values Default Description
======================= ====== ======= =================================================
``DEBUGGER_PTVSD``      0|1    0       Install ptvsd during build process for debugging
``GIT_SSH``             0|1    0       Checkout git repositories via ssh
``GIT_USER_NAME``       string ""      Username for git commits *(optional)*
``GIT_USER_EMAIL``      string ""      Email for git commits *(optional)*
``GIT_USER_SIGNINGKEY`` string ""      16-hex-digit GPG key id for signed commits
======================= ====== ======= =================================================

Run the `project script`_ update command, which checkouts the service
repositories, creates the service folders and copies the configuration example
files *(~5-10 minutes)*::

    $ ./project update

Configuration
-------------

For ``staging`` and ``production`` environments:

1. Adjust the **variables** in `.env`_
   (hostnames, ports, usernames, paths, etc).
2. Adjust the **secrets**:

   ========================================================= ===================================
   File                                                      Variable
   ========================================================= ===================================
   ``sevices/webapi.env``                                    | ``PYRAMID_AUTHENTICATION_SECRET``
                                                             | ``PYRAMID_SESSION_SECRET``
   ``sevices/webgui.env``                                    | ``PYRAMID_AUTHENTICATION_SECRET``
                                                             | ``PYRAMID_SESSION_SECRET``
   ``sevices/worker.env``                                    | ``ECHOPRINT_TOKEN``
                                                             | ``WORKER_PROTEUS_PASSWORD``
   ``services/config/collecting_society.<ENVIRONMENT>.conf`` | ``privatekey``
                                                             | ``certificate``
                                                             | ``super_pwd``
   ``services/config/collecting_society.passfile``           plaintext
   ========================================================= ===================================
3. Add basic http authentication, if needed::

    $ sudo htpasswd -c volumes/nginx-htpasswd/collecting_society.test <USERNAME>
    $ sudo ln -s collecting_society.test volumes/nginx-htpasswd/api.collecting_society.test

Images
------

Each service runs on a separate docker container. A docker container is
a running instance of a prebuilt docker image. The `docker images`_ for all
services need to be built first.

The initial build of the containers will take some time *(around 30-60 minutes)*::

    $ docker-compose build

Database
--------

After building the images, the services can be started. On the first `run`_,
the database and `demodata`_ is created *(takes about 10 to 15 minutes)*::

    $ docker-compose up

The services should now be running and ready for clients to connect.

Webbrowser
----------

The webserver uses domain based routing of requests. In order to resolve the
testing domains to localhost, add the following lines to ``/etc/hosts``::

    127.0.0.1   collecting_society.test
    127.0.0.1   api.collecting_society.test

Test the connection by following the instructions in `Webbrowser Usage`_.

Tryton
------

To connect to Trytond, you can use one of the several Tryton client
applications or APIs. For back-office use of the application, the Gtk2 based
Tryton client is recommended.

.. note:: The Trytond server and the Tryton client are required to have the
    same version branch.

.. warning:: As the Tryton branch ``3.4`` is quite outdated, some manual
    installation steps are neccessary including the installation of outdated
    python packages.

Clone the repository and switch to the ``3.4`` branch::

    $ cd MY/WORKING/SPACE
    $ git clone https://github.com/tryton/tryton.git
    $ cd tryton
    $ git checkout 3.4

Depending on the OS, there might be different ways to install the dependencies
(see ``doc/installation.rst`` and `tryton-client`__ package of Ubuntu 16)::

    librsvg2-common
    python >= 2.7
    python-chardet
    python-dateutil
    python-gtk2 >= 2.22

__ https://packages.ubuntu.com/xenial/tryton-client

- **Ubuntu < 20.04**

  All dependencies can be installed from the apt repositories::

        $ sudo apt-get install librsvg2-common python python-chardet \
            python-dateutil python-simplejson python-gtk2

- **Ubuntu >= 20.04**

  .. warning:: This method of installation is untested, so please be careful!

  1. Install the dependencies available in the apt repositories::

          $ sudo apt-get install librsvg2-common python2

  2. As pygtk is not packaged and cannot be built by pip anymore, the only
     option left is to install the last available pygkt from the `archive`__
     (see working answer in `askubuntu`__). The other packages could be
     installed with pip2, but as pip2 is also not packaged anymore, it might
     be easier to install them via archive as well::

          $ ARCHIVE=http://archive.ubuntu.com/ubuntu/pool/universe
          $ wget $ARCHIVE/p/pygtk/python-gtk2_2.24.0-5.1ubuntu2_amd64.deb
          $ wget $ARCHIVE/s/six/python-six_1.15.0-2_all.deb
          $ wget $ARCHIVE/c/chardet/python-chardet_3.0.4-4build1_all.deb
          $ wget $ARCHIVE/p/python-dateutil/python-dateutil_2.7.3-3ubuntu1_all.deb
          $ sudo apt-get install ./python-gtk2_2.24.0-5.1ubuntu2_amd64.deb
          $ sudo apt-get install ./python-six_1.15.0-2_all.deb
          $ sudo apt-get install ./python-chardet_3.0.4-4build1_all.deb
          $ sudo apt-get install ./python-dateutil_2.7.3-3ubuntu1_all.deb

__ http://archive.ubuntu.com/ubuntu/pool/universe/
__ https://askubuntu.com/questions/1235271/pygtk-not-available-on-focal-fossa-20-04/1235347#1235347

Test, if Tryton is running::

    $ python2 bin/tryton

For easy startup create a startup script:

1. Create the file ``/usr/local/bin/tryton`` in your prefered editor, e.g.::

    $ sudo vim /usr/local/bin/tryton

2. Paste the following lines, set ``TRYTONPATH`` to the path of the
   tryton repository::

    #!/bin/bash
    TRYTONPATH=~/MY/WORKING/SPACE/tryton
    python2 $TRYTONPATH/bin/tryton -d

3. Set the execution flag of the script::

    $ sudo chmod u+x /usr/local/bin/tryton

Test the connection by following the instructions in `Tryton Usage`_.


.. _Application Configuration:

Configuration
=============

The services are configured via:

1. Project configuration:
   ``project.yml``
2. Application environment:
   ``development``, ``staging``, ``production``, ``testing``
3. Global and service specific envvar files for the containers:
   ``.env``, ``service/<SERVICE>.env``
4. Application specific configuration files:
   ``*.conf``, ``*.ini``

.. note:: Sane defaults for a development setup are given and should work as
    provided, so this section might be skipped to start with development.

.. note:: Some files are tracked in git as ``FILE.example`` and are initally
    copied to the untracked ``FILE`` but not overwritten by the
    `project script`_ update command. The script will print notifications and
    diffs, when those files need to be changed manually.


Project
-------

The project configuration file ``project.yml`` describes the tasks to perform
to setup and update the `environments`_. Tasks may include the the creation
or copying of files, folders and symlinks and the checkout specific branches
or tags of upstream and project repositories.


Environments
------------

The services are configured differently for certain application environments.
The differences on each level include:

- **docker**: mapped ports, volume handling
- **database**: demodata generation
- **application**: debug switches, template caching

=============== ====== ============== ======== ===== =====
Context         Ports  Volumes        Demodata Debug Cache
=============== ====== ============== ======== ===== =====
``development`` all    local mounts   yes      on    off
``staging``     public local mounts   yes      off   on
``production``  public docker managed no       off   on
``testing``     public docker managed no       off   on
=============== ====== ============== ======== ===== =====

For each of the environments except ``testing``, there is a corresponding
branch with the same name in this repository and most of the main
subrepositories pre-configured for this environment.

Envvars
-------

The `.env`_ file in the root path of the repository is the main envvar file
and prefered place to specify configuration variables for all services. It
is included in all main service containers. The variables might be overridden
in a service container by the corresponding ``services/<SERVICE>.env``.

The ``.env`` file is also processed by docker-compose by convention and
contains variables for the build process as well as for the
`project script`_.

.. seealso:: `Compose CLI environment variables`__

__ https://docs.docker.com/compose/reference/envvars/

.env
''''

================================== =============== =====================================
Variable                           Values          Description
================================== =============== =====================================
``PROJECT``                        string          project name
``ENVIRONMENT``                    | "development" environment, switch for config files
                                   | "staging"
                                   | "production"
``BRANCH``                         string          branch of project repositories
``BUILD``                          string          build number added by ci
``COMPOSE_DOCKER_CLI_BUILD``       0|1             use BuildKit for docker builds
``COMPOSE_PROJECT_NAME``           string          prefix for containers
``COMPOSE_IGNORE_ORPHANS``         0|1             suppress orphan container warnings
``DEBUGGER_WINPDB``                0|1             install packages for winpdb in images
``DEBUGGER_PTVSD``                 0|1             install packages for ptvsd in images
``WORKDIR``                        PATH            workdir for images
``GIT_SSH``                        0|1             use git via ssh
``GIT_USER_NAME``                  string          set git username in repositories
``GIT_USER_EMAIL``                 string          set git email in repositories
``GIT_USER_SIGNINGKEY``            string          GPG key for signing commits
``POSTGRES_HOSTNAME``              string          hostname of postgres server
``POSTGRES_PORT``                  integer         port of postgres server
``TRYTON_HOSTNAME``                string          hostname of tryton server
``TRYTON_DATABASE``                string          name of the tryton database
``TRYTON_PORT``                    integer         port of tryton server
``TRYTON_VERSION``                 string          version of tryton to use
``VIRTUAL_HOST_WEBGUI``            URI             nginx URI for the webgui service
``VIRTUAL_PORT_WEBGUI``            integer         nginx reverse port for webgui
``VIRTUAL_HOST_WEBAPI``            URI             nginx URI for the webapi service
``VIRTUAL_PORT_WEBAPI``            integer         nginx reverse port for webapi
``MAIL_HOST``                      string          hostname of the mail server
``MAIL_PORT``                      integer         port of the mail server
``MAIL_DEFAULT_SENDER``            EMAIL           default sender email address
``MAIL_TO_REAL_WORLD``             0|1             simulate sending mails or not
``PYRAMID_SCHEMA``                 SCHEMA          schema of pyramid server
``PYRAMID_TRUSTED_PROXY``          IP              trusted IP for pyramid server
``WEBAPI_URL``                     URL             URL of web api
``WEBAPI_CORS``                    URL             allowed origins for web api CORS
``WEBAPI_VERSION``                 string          version of web api
``WEBAPI_ENDPOINT_DATATABLES``     string          REST endpoint name for datatables
``WEBAPI_ENDPOINT_REPERTOIRE``     string          REST endpoint name for repertoire
``WEBAPI_CONTENT``                 PATH            path to content folder (upload)
``WEBAPI_STORAGE``                 PATH            path to storage folder (processing)
``ECHOPRINT_SCHEMA``               SCHEMA          schema of echoprint server
``ECHOPRINT_HOSTNAME``             string          hostname of echoprint server
``ECHOPRINT_PORT``                 integer         port of echoprint server
``WORKER_PROTEUS_USER``            string          tryton username for proteus client
``WORKER_DISEMBODY_DROPPED_FILES`` "yes"|"no"      delete upload content to save space
================================== =============== =====================================

webapi
''''''

================================= =============== =====================================
``PYRAMID_AUTHENTICATION_SECRET`` string          secret for authentication
``PYRAMID_SESSION_SECRET``        string          secret for sessions
================================= =============== =====================================

webgui
''''''

================================= =============== =====================================
``PYRAMID_AUTHENTICATION_SECRET`` string          secret for authentication
``PYRAMID_SESSION_SECRET``        string          secret for sessions
================================= =============== =====================================

worker
''''''

================================= =============== =====================================
``ECHOPRINT_TOKEN``               string          authtoken for echoprint server
``WORKER_PROTEUS_PASSWORD``       string          tryton password for proteus client
================================= =============== =====================================

Applications
------------

The applications (trytond, proteus, pyramid) provide distinct files for all
application `environments`_, which are included depending on the value of the
`.env`_ variable ``ENVIRONMENT``. The applications might use envvars as well
indicated by the syntax ``${VARIABLE}`` in the configuration file. The same
syntax can also be used in ``project.yml``. The following sections provide
a list of all envvar and configuration files for each application.

.. _Trytond Config:

Trytond
'''''''

*Services: erpserver, webapi, webgui*

========================================================= ==============================
``.env``                                                  main envvar file
``services/config/collecting_society.<ENVIRONMENT>.conf`` trytond config
``services/config/collecting_society.passfile``           initial trytond admin password
========================================================= ==============================

.. _Proteus Config:

Proteus
'''''''

*Services: worker*

======================================================== ==============================
``.env``                                                 main envvar file
``services/worker.env``                                  service envvar file
``services/config/collecting_society_worker.config.ini`` worker/proteus config
======================================================== ==============================

.. _Pyramid Config:

Pyramid
'''''''

*Services: webapi, webgui*

============================================================ ==========================
``.env``                                                     main envvar file
``services/web[api|gui].env``                                service envvar file
``services/config/portal_web.<ENVIRONMENT>.ini``             pyramid config
``services/config/collecting_society_web.<ENVIRONMENT>.ini`` pyramid plugin config
============================================================ ==========================

Usage
=====

There are several ways to interact with the services:

1. The ``docker-compose`` CLI is the prefered general high level docker tool
   for everyday use.
2. The ``docker`` CLI provides sometimes more useful low level commands.
3. The `Scripts`_ in the root folder are provided for comfort or
   automatisation.
4. The `CLI`_ script provides special maintainance commands for the services
   (for use within the containers).

If you tend to forget the commands or syntax, try getting used to the help
commands:

=============================== ==============================================================
List docker-compose commands    ``docker-compose --help``
Help for docker-compose command ``docker-compose COMMAND --help``
List docker commands            ``docker --help``
Help for docker command         ``docker COMMAND --help``
List scripts                    ``ls -F | grep '*$'``
Help for scripts                ``./SCRIPT --help``
List CLI command                ``docker-compose [exec|run --rm] erpserver --help``
Help for CLI command            ``docker-compose [exec|run --rm] erpserver COMMAND --help``
=============================== ==============================================================

.. seealso:: `Docker-compose command line reference`__ and
    `Docker command line reference`__.

__ https://docs.docker.com/compose/reference/overview/
__ https://docs.docker.com/engine/reference/commandline/cli/


Run
---

=========================================== ====================================================
Start services                              ``docker-compose up``
Start services in the background            ``docker-compose up -d``
Start a certain service (in the background) ``docker-compose up SERVICE [-d]``
Run a command on a running|new container    ``docker-compose [exec|run --rm] SERVICE CMD``
Run CLI command on a running|new container  ``docker-compose [exec|run --rm] SERVICE [cli] CMD``
Open a shell on a running|new container     ``docker-compose [exec|run --rm] SERVICE bash``
Run CLI command inside a container shell    ``[cli] CMD``
Build documentation                         ``./docs-build``
Run tests                                   ``./service-test``
Scale services on demand                    ``docker-compose scale SERVICE=#``
Stop services                               ``docker-compose stop``
Stop a certain service                      ``docker-compose stop SERVICE``
Stop and remove containers/volumes/networks ``docker-compose down``
=========================================== ====================================================

.. seealso:: ``[SERVICE]``: `Table of Services`_, ``[CMD]``: `CLI`_.

.. note:: Always prefer ``exec`` to ``run --rm``, if containers are already
    running.

.. _Project Update:

Update
------

========================= =======================================================
Update repositories       ``./project update``
Diff repos/example files  ``./project diff``
Build images              ``docker-compose build``
Update database           ``docker-compose [exec|run --rm] erpserver db-update``
========================= =======================================================

1. Update the repositories/files/folders::

    $ ./project update

   The script will print notifications and instruction, if further steps are
   neccessary.

   .. note:: The `project script`_ update command will also try to update the
       collecting_society_docker repository and thus itself first, before
       updating the subordinate repositories.

2. If there were changes to the ``*.example`` files, diff the files and
   apply changes manually::

    $ ./project diff

3. If there were changes in the ``Dockerfile``, rebuild all `docker images`_::

    $ docker-compose build

   If you run into problems, you can also rebuild all `docker images`_ without
   cache. Just `remove`_ all project images (also the dangling ones) before the
   execution of the ``build`` command.

   .. warning:: The ``build`` command has a ``--no-cache`` option, but for
       multistage builds the intermediate stages won't be reused then, which
       highly increases the build time.

4. If there were changes in the ``collection_society`` repository, update the
   database::

    $ docker-compose run --rm erpserver db-update

   If you run into problems and don't care about the data, you can also
   recreate the database::

    $ ./db-rebuild

Inspect
-------

============================================ ===================================================
Attach to the logs of a certain service      ``docker-compose logs [-f] SERVICE``
Open a shell on a service container          ``docker-compose run --rm SERVICE bash``
Open a shell on a running container          ``docker-compose exec bash``
List project docker containers               ``docker-compose ps``
List project docker images                   ``docker-compose images``
List project docker containers               ``docker-compose ps [-a]``
List processes of project container          ``docker-compose top``
Show used resources for containers           ``docker stats``
List docker images                           ``docker images ls [-a]``
List docker networks                         ``docker network ls``
List docker volumes                          ``docker volume ls``
Inspect a container/volume/network/...       ``docker inspect ID|NAME``
============================================ ===================================================

Remove
------

.. warning:: The ``docker`` commands apply to **all** docker containers on the host.

============================================== ================================
Remove project containers/networks/volumes     ``docker-compose down``
Remove all stopped docker containers           ``docker container prune``
Remove all dangling images to free diskspace   ``docker image prune``
Remove volumes                                 ``docker volume rm VOLUMENAME``
============================================== ================================

.. note:: For ``VOLUMENAME`` see the output of ``docker volume ls``.

Remove all containers, networks, volumes **and images**::

    $ docker-compose -f docker-compose.documentation.yml down -v --rmi all
    $ docker-compose -f docker-compose.testing.yml down -v --rmi all
    $ docker-compose down -v --rmi all
    $ docker image prune

.. note:: The multiple ``down`` commands are needed, as testing and
    documentation have separate containers, but are based on the same
    multistage Dockerfile.

Database
--------

======= =========================================================================================
Create  ``docker-compose [exec|run --rm] erpserver db-create [NAME]``
Copy    ``docker-compose [exec|run --rm] erpserver db-copy [--force] [SOURCENAME] [TARGETNAME]``
Backup  ``docker-compose [exec|run --rm] erpserver db-backup [NAME] > /shared/tmp/db.backup``
Delete  ``docker-compose [exec|run --rm] erpserver db-delete [NAME]``
Setup   ``docker-compose [exec|run --rm] erpserver db-setup [NAME]``
Rebuild | ``docker-compose [exec|run --rm] erpserver db-rebuild [NAME]``
        | ``./db-rebuild``
Examine ``docker-compose run --rm erpserver db-connect [NAME]``
======= =========================================================================================

.. note:: ``[NAME]`` is optional and defaults to ``collecting_society``.

.. note:: If the setup/rebuild hangs, look for and delete the
    ``./volumes/shared/running_db_creation.delete_me`` locking file.

The database files are stored in ``./volumes/postgresql-data``. If the postgres
setup itself seem to be broken, you can delete and recreate the folder::

    $ docker-compose down
    $ sudo rm -rf ./volumes/postgresql-data/
    $ docker-compose up

.. warning:: All data in this database will be deleted!

.. note:: The uid/gid of the folder and files matches those of the postgres
    user in the cointainer, so ``sudo`` is probably neccessary to be able to
    delete them.

Scripts
-------

The scripts are either intended to make some operations more comfortable or for
automatisation using a build server (CI). The following sections contain a brief
synopsis about each of the provided scripts as provided by the ``--help`` option.
The usual syntax is ``object``-``operation``.

.. _project script:

project
'''''''
::

    $ ./project --help
    usage: ./project

    Performs development and maintainance tasks for the project.

    optional arguments:
      -h, --help         show this help message and exit

    subcommands:
      (default: status)
        update           Updates files, folders, symlinks and repos
        status           Prints the git status of the project repositories
        diff             Prints the diff of the project repos and the example files
        pull             Pulls the current branch for all project repositories
        checkout         Checksout a branch in all project repositories
        delete           Deletes a local and remote branch in all project repos
        commit           Commits changes and untracked files to the project repositories
        push             Pushes commits in all project repos, creates missing remote branches
        merge            Merges the current branch into another branch in all project repos
        promote          Merges an environment branch into the next stage environment branch

::

    $ ./project update --help
    usage: ./project update [-h] [-v] [--branch NAME] [--environment NAME] [--reset] [--ci]

    Updates files, folders, symlinks and repos.

    optional arguments:
      -h, --help          show this help message and exit
      -v, --verbose       verbose output, -vv for debug output
      --branch NAME       Branch name (default: .env [feature-updatescript])
      --environment NAME  Environment name (default: .env [development])
      --reset             overwrites the configuration files with example files (default: False)
      --ci                continues integration mode: reset, debug, colorless (default: False)

::

    $ ./project status --help
    usage: ./project status [-h] [-v]

    Prints the git status of the project repositories.

    optional arguments:
      -h, --help     show this help message and exit
      -v, --verbose  verbose output, -vv for debug output

::

    $ ./project diff --help
    usage: ./project diff [-h] [-v]

    Prints the diff of the project repos and the example files.

    optional arguments:
      -h, --help     show this help message and exit
      -v, --verbose  verbose output, -vv for debug output

::

    $ ./project pull --help
    usage: ./project pull [-h] [-v]

    Pulls the current branch for all project repositories.

    optional arguments:
      -h, --help     show this help message and exit
      -v, --verbose  verbose output, -vv for debug output

::

    $ ./project checkout --help
    usage: ./project checkout [-h] [-v] [BRANCH]

    Checksout a branch in all project repositories.

    positional arguments:
      BRANCH         Branch name (default: checkedout [feature-updatescript])

    optional arguments:
      -h, --help     show this help message and exit
      -v, --verbose  verbose output, -vv for debug output

::

    $ ./project delete --help
    usage: ./project delete [-h] [-v] [-f] [--no-local-delete] [--no-remote-delete] BRANCH

    Deletes a local and remote branch in all project repos.

    positional arguments:
      BRANCH              Branch name

    optional arguments:
      -h, --help          show this help message and exit
      -v, --verbose       verbose output, -vv for debug output
      -f, --force         Force deletion of not fully merged branches (default: False)
      --no-local-delete   Don't delete local branch (default: False)
      --no-remote-delete  Don't delete remote branch (default: False)

::

    $ ./project commit --help
    usage: ./project commit [-h] [-v] MESSAGE

    Commits changes and untracked files to the project repositories.

    positional arguments:
      MESSAGE        Commit message

    optional arguments:
      -h, --help     show this help message and exit
      -v, --verbose  verbose output, -vv for debug output

::

    $ ./project push --help
    usage: ./project push [-h] [-v]

    Pushes commits in all project repos, creates missing remote branches.

    optional arguments:
      -h, --help     show this help message and exit
      -v, --verbose  verbose output, -vv for debug output

::

    $ ./project merge --help
    usage: ./project merge [-h] [-v] [-f] [--no-delete] [--no-local-delete] [--no-remote-delete]
                           [--no-push] [BRANCH]

    Merges the current branch into another branch in all project repos.

    positional arguments:
      BRANCH              Target branch name (default: development)

    optional arguments:
      -h, --help          show this help message and exit
      -v, --verbose       verbose output, -vv for debug output
      -f, --force         Force deletion of not fully merged branches (default: False)
      --no-delete         Don't delete branch after merge (default: False)
      --no-local-delete   Don't delete local branch after merge (default: False)
      --no-remote-delete  Don't delete remote branch after merge (default: False)
      --no-push           Don't push branch after merge (default: False)

::

    $ ./project promote --help
    usage: ./project promote [-h] [-v] ENVIRONMENT

    Merges an environment branch into the next stage environment branch.

    positional arguments:
      ENVIRONMENT    Environment to be promoted to the next stage

    optional arguments:
      -h, --help     show this help message and exit
      -v, --verbose  verbose output, -vv for debug output

.. _service-test script:

service-test
''''''''''''
::

    $ ./service-test --help
    Usage: ./service-test [service] [--down] [--build] [--keep] [--lint]
                      [--ci] [--ci-branch NAME] [--ci-environment NAME]
                      [--help] [PARAMS]

      This script runs the unit/function/integration tests and linter for the services:
        - erpserver (tryton)
        - web (pyramid)
        - worker (echoprint)

    Options:
      service: web|worker|erpserver|all (default: all)
      --down: immediately stop, remove the container and exit
      --build: build images and recreate the test database template
      --keep: keep container running
      --lint: only lint the code, don't run the tests
      --ci: continous integration mode
            - update repositories (overrides config files!)
            - build images
            - recreate the test database template
            - run tests and linter
            - stop and remove the container
      --ci-branch: branch to test
      --ci-environment: environment to test
      --help: display this help
      PARAMS: are passed to nosetest

.. _docs-build script:

docs-build
''''''''''
::

    $ ./docs-build --help
    Usage: ./docs-build [--down] [--build] [--keep] [--no-autoapi]
                        [--ci] [--ci-branch NAME] [--ci-environment NAME]
                        [--help]

      This script builds the documentation with sphinx.

    Options:
      --down: immediately stop and remove the container and exit
      --build: build images
      --keep: keep container running
      --no-autoapi: don't parse the modules
      --ci: continous integration mode
            - update repositories (overrides config files!)
            - build images
            - build docs
            - stop and remove the container
      --ci-branch: branch to test
      --ci-environment: environment to test
      --help: display this help

.. _db-rebuild script:

db-rebuild
''''''''''
::

    $ ./db-rebuild --help
    Usage: ./db-rebuild [--ci] [--help]

      This script deletes and recreates the database and generates the demodata.

    Options:
      --ci: stops the services before, starts the services detached afterwards
      --help: display this help

CLI
---

The ``./volumes/shared/cli`` script contains a CLI for special service
maintainance commands. Within the containers it is available in the working
directory ``/shared/cli``. For convenience and to ensure the same command
invokation syntax of ``exec`` and ``run --rm``, the commands of the script are
also available directy via ``/shared/COMMAND``.

.. warning:: All CLI commands should only be executed within a service container!

.. note:: Not all commands will work on any service.

**Usage**:

On the host::

    $ docker-compose run --rm SERVICE COMMAND
    $ docker-compose exec SERVICE COMMAND

For example::

    $ docker-compose run --rm erpserver db-rebuild
    $ docker-compose exec erpserver db-rebuild

.. note:: Use ``exec`` if the container is already running, e.g. in another terminal
     window after a ``docker-compose up``. Use ``run --rm`` if no container is running
     and your just want to start it for a single task upon which it is removed again (-rm).
     To start more than a single task, you would want to 'go inside a container' by
     running a ``bash`` command, e.g. ``docker-compose run --rm erpserver bash``.

Inside a service container::

    $ COMMAND

For example::

    $ db-rebuild

**Help**::

    $ cli --help
    $ COMMAND --help

**Commands**::

    $ cli --help
    Usage: cli [OPTIONS] COMMAND [ARGS]...

      Command line interface to setup and maintain services in docker
      containers.

    Options:
      --help  Show this message and exit.

    Commands:
      db-backup            Dumps the postgres database DBNAME to stdout.
      db-connect           Opens a SQL console for the database DBNAME.
      db-copy              Creates the postrges database DBNAME_DST from...
      db-create            Creates the postrges database DBNAME.
      db-delete            Deletes the postrges database DBNAME.
      db-rebuild           Deletes DBNAME and executes db setup
      db-setup             Creates and sets up the postgres database...
      db-update            Updates tryton modules for database DBNAME.
      docs-build           Builds the Sphinx documentation.
      pip-install          Installs required packages for a SERVICE with...
      service-deploy       Deploys the services (erpserver, webgui,...
      service-healthcheck  Healthcheck for the services.
      service-test         Runs all tests for a service (erpserver, web,...

.. _db-backup CLI:

db-backup
'''''''''
::

    $ db-backup --help
    Usage: cli db-backup [OPTIONS] [DBNAME]

      Dumps the postgres database DBNAME to stdout.

    Options:
      --help  Show this message and exit.

.. _db-connect CLI:

db-connect
''''''''''
::

    $ db-connect --help
    Usage: cli db-connect [OPTIONS] [DBNAME]

      Opens a SQL console for the database DBNAME.

    Options:
      --help  Show this message and exit.

.. _db-copy CLI:

db-copy
'''''''
::

    $ db-copy --help
    Usage: cli db-copy [OPTIONS] DBNAME_SRC DBNAME_DST

      Creates the postrges database DBNAME_DST from template DBNAME_SRC.

    Options:
      --force / --no-force  Force execution (default: no)
      --help                Show this message and exit.

.. _db-create CLI:

db-create
'''''''''
::

    $ db-create --help
    Usage: cli db-create [OPTIONS] [DBNAME]

      Creates the postrges database DBNAME.

      The execution is skipped if the database already exists.

    Options:
      --help  Show this message and exit.

.. _db-delete CLI:

db-delete
'''''''''
::

    $ db-delete --help
    Usage: cli db-delete [OPTIONS] [DBNAME]

      Deletes the postrges database DBNAME.

      On error the deletion is retried several times.

    Options:
      --help  Show this message and exit.

.. _db-rebuild CLI:

db-rebuild
''''''''''
::

    $ db-rebuild --help
    Usage: cli db-rebuild [OPTIONS] [DBNAME]

      Deletes DBNAME and executes db setup

    Options:
      -r, --reclimit INTEGER      Maximum numbers of objects (default: 0 = all)
      -d, --dataset TEXT          dataset in ./data/datasets/ to generate
                                  (default: all)
                                  can be used multiple times
      -e, --exclude TEXT          datasets in ./data/datasets/ to exclude
                                  (default: none)
                                  can be used multiple times
      --template / --no-template  Use template db for dataset deps (default: yes)
      --cache / --no-cache        Use/Recreate template db for dataset deps
                                  (default: no)
      --pdb / --no-pdb            Start pdb on error (default: no)
      --help                      Show this message and exit.

.. _db-setup CLI:

db-setup
''''''''
::

    $ db-setup --help
    Usage: cli db-setup [OPTIONS] [DBNAME]

      Creates and sets up the postgres database DBNAME.

      The execution is skipped if the database already exists. The execution
      might be forced (omits the db creation, if it exists).

      Generates production and demodata.

      During installation a lockfile is created on the host to prevent multiple
      execution from different docker containers.

    Options:
      -r, --reclimit INTEGER      Maximum numbers of objects (default: 0 = all)
      -d, --dataset TEXT          dataset in ./data/datasets/ to generate
                                  (default: all)
                                  can be used multiple times
      -e, --exclude TEXT          datasets in ./data/datasets/ to exclude
                                  (default: none)
                                  can be used multiple times
      --template / --no-template  Use template db for dataset deps (default: yes)
      --cache / --no-cache        Regenerate template db for dataset deps
                                  (default: no)
      --force / --no-force        Force execution (default: no)
      --pdb / --no-pdb            Start pdb on error (default: no)
      --help                      Show this message and exit.

.. _db-update CLI:

db-update
'''''''''
::

    $ db-update --help
    Usage: cli db-update [OPTIONS] [TRYTONDCONF] [DBNAME]

      Updates tryton modules for database DBNAME.

      Modules can be provided, default is 'collecting_society'. If modules are
      'all', all modules are updated.

    Options:
      -m, --modules TEXT  Single module or comma separated list of modules to
                          update. Whitspace not allowed!
      --help              Show this message and exit.

.. _docs-build CLI:

docs-build
''''''''''
::

    $ docs-build --help
    Usage: cli docs-build [OPTIONS]

      Builds the Sphinx documentation.

      Installs pip packages of all modules so they can be found by Sphinx.
      autoapi and Sphinx are started with docs/build.sh.

    Options:
      --autoapi / --no-autoapi  Activate autoapi (default: yes)
      --help                    Show this message and exit.

.. _pip-install CLI:

pip-install
'''''''''''
::

    $ pip-install --help
    Usage: cli pip-install [OPTIONS] [SERVICE]

      Installs required packages for a SERVICE with pip.

      Requirements have to be defined in `./shared/config/pip/SERVICE.pip`.

      After installation a flag file is created within the container to avoid
      multiple execution during its lifespan.

    Options:
      --help  Show this message and exit.

.. _service-deploy CLI:

service-deploy
''''''''''''''
::

    $ service-deploy --help
    Usage: cli service-deploy [OPTIONS] [SERVICE]

      Deploys the services (erpserver, webgui, webapi, worker, fingerprint).

      Installs pip packages, creates and sets up database and runs the
      application.

    Options:
      --help  Show this message and exit.

.. _service-healthcheck CLI:

service-healthcheck
'''''''''''''''''''
::

    $ service-healthcheck --help
    Usage: cli service-healthcheck [OPTIONS] [SERVICE]

      Healthcheck for the services.

    Options:
      --help  Show this message and exit.

.. _service-test CLI:

service-test
''''''''''''
::

    $ service-test --help
    Usage: cli service-test [OPTIONS] [SERVICE] [NARGS]...

      Runs all tests for a service (erpserver, web, worker).

      Starts nosetests and prints output to stdout.

      Creates the test database template DBNAME_template, if not existant. On
      RESET, the database DBNAME will be recreated from this template and the
      temporary tryton file folder will be deleted.

      The location of the temporary tryton upload folder is configured in
      `./shared/config/trytond/testing_DBTYPE.conf` (currently
      `./shared/tmp/files`).

      The location of the screenshots of integration tests is configured within
      `<portal_web>/tests/config.py` (currenty `./shared/tmp/screenshots).

      The PATH to tests may be defined to test certain testfiles, testclasses or
      test methods (see nosetests for the syntax). If no PATH is given, all tests
      of portal_web and plugins are included. The test files should be stored
      below the following subpaths by convention:

          <portal_web||plugin>/tests/unit (unittest)

          <portal_web||plugin>/tests/functional (webtest)

          <portal_web||plugin>/tests/integration (selenium)

      Additional NARGS will be passed to nosetests.

    Options:
      --dbname TEXT         Name of database (default: test)
      --reset / --no-reset  Reset the database (default: yes)
      --path TEXT           Searchpath for tests (see nosetest)
      --help                Show this message and exit.

.. _service-lint CLI:

service-lint
''''''''''''
::

    $ service-lint --help
    Usage: cli service-lint [OPTIONS] [SERVICE]

      Runs linter for a service (erpserver, web/webgui/webapi, worker).

      If PATH is provided, only the path is linted, not the service. If SERVICE
      is 'all', all services are linted.

    Options:
      --path TEXT  Custom path with files to lint
      --help       Show this message and exit.

.. _Webbrowser Usage:

Webbrowser
----------

Open the webbrowser and point it to the

- webgui: http://collecting_society.test
- webapi: http://api.collecting_society.test

Login as demo user:

===================================== ============ ===================
Username                              Password     Roles
===================================== ============ ===================
``allroles1@collecting-society.test`` ``password`` licenser, licensee
``licenser1@collecting-society.test`` ``password`` licenser
``licensee1@collecting-society.test`` ``password`` licensee
===================================== ============ ===================

.. _Tryton Usage:

Tryton
------

Start Tryton::

    $ tryton

.. note:: The Tryton client configuration files are stored in
    ``~/.config/tryton/3.4/``.

Open a connection to Trytond:

========== ================================
host       ``collecting_society.test:8000``
database   ``collecting_society``
user       ``admin``
password   ``admin``
========== ================================

.. seealso:: `Tryton Usage Documentation`__

__ https://das-do.readthedocs.io/en/3.4/usage.html

The database entries can be found in the navigation tree:

* **Collecting Society**: Societies, Tariffs, Allocations, Distributions
* **Licenser**: Artists, Releases, Creations, Licenses, Labels, Publishers
* **Licensee**: Events, Locations, Websites, Releases, Devices, Declarations,
  Utilisations
* **Portal**: Access
* **Archiving**: Storehouses, Harddisks, Filesystems, Contents

Other important entries are:

* **Party**: Parties, Addresses
* **Administration / Users**: Users, Web Users
* **Administration / Sequences**: Sequences


.. _Application Development:

Development
===========

Environment
-----------

Project
'''''''

The tasks to setup each environment can be configured in ``./project.yml``:

.. code-block:: yaml

    <ENVIRONMENT>:

      commands:
        <COMMAND>: {}

      tasks:
        <COMMAND>:

          - name: <NAME>
            actions: [<ACTION>, <ACTION>]
            <KEY>: <VALUE>

          - name: <NAME>
            actions: [<ACTION>, <ACTION>]
            <KEY>: <VALUE>
            batch:
              - name: <NAME>
                <KEY>: <VALUE>

      actions:
        <ACTION>: {}
        <ACTION>: []

=============== ===============================================================
Key             Description
=============== ===============================================================
``ENVIRONMENT`` | environment, for which the tasks are performed.
                | inheritance: production -> staging -> testing -> development
``commands``    configuration variables availbable for each command
``COMMAND``     | main commands
                | maps to ``@command`` functions in the `project script`_
``tasks``       list of tasks to perform consecutively for each command
``NAME``        name of the task, required for all tasks
``ACTION``      | actions to perform consecutivky for each task,
                | maps to ``@action`` functions in the `project script`_
``actions``     | *[dictionary]* configuration values available in actions
                | *[list]* action group with actions to perform consecutivley
=============== ===============================================================

Commands can be invoked via the `project script`_. For available commands, see
the ``@command`` decorated functions in the script.

Each command processes its task list and for each task the defined actions
consecutivley. Each action receives the task dictionary and expects the task
to have the proper key/value pairs (e.g. repos need a source, etc). The
command/action config dictionary is also available to the actions and might
configure how the action should be performed. For available actions, see the
``@action`` decorated functions in the script.

For a list of command/action configuration variables, see the comments in
``./project.yml``.

Batch tasks will use the key/value pairs of its parent updated with itself.
In inherited environments, tasks may be changed by using the same name of the
inherited task.

Branches
''''''''

Each project repository has a branch for all `environments`_. To switch a
branch for all project repositories::

    $ ./project checkout BRANCH

Using **feature branches** is encouraged. To create a new local feature branch
for all repositories::

    development$ ./project checkout feature-<FEATURENAME>

The basic workflow:

1. **Create** a feature branch. Remote branches are always prefered during
   checkout::

    development$ ./project checkout feature-branch

2. **Develop** the code::

    feature-branch$ [...]

3. **Test** the code::

    feature-branch$ ./service-test

4. **Check** the status of the workdirs::

    feature-branch$ ./project status
    feature-branch$ ./project diff [-v]

5. **Commit** the changes and new files::

    feature-branch$ ./project commit "commit message"

6. **Push** the branch, if the feature branch should be shared::

    feature-branch$ ./project push

7. **Delete** the branch, if the feature branch should be discarded. Both
   the local and remote branch will be deleted::

    feature-branch$ ./project chechkout development
    development$ ./project delete feature-branch

8. **Merge** the branch into ``development``, when the feature is finished.
   This will delete the local and remote branch after the merge::

    feature-branch$ ./project merge

Docker
------

Compose
'''''''

The project consists of 3 separate docker-compose setups:

**Development/Staging/Production**

- Purpose: Main development/production setup of the services
- Files

  - ``docker-compose.yml``: main file
  - ``docker-compose.override.yml``: override file, symlink to environment config (ports, volumes)

    - ``docker-compose.development.yml``: additions for development environment
    - ``docker-compose.staging.yml``: additions for staging environment
    - ``docker-compose.production.yml``: additions for productions environment

- Usage: ``docker compose COMMAND``
- Services: `Table of Services`_

.. note:: The ``docker-compose.override.yml`` is a docker-compose convention.

**Testing**

- Purpose: Manual/Automated testing, CI
- Files

  - ``docker-compose.testing.yml``

- Usage: ``docker-compose -f docker-compose.testing.yml COMMAND``
- Services

  - ``test_database``: same as database
  - ``test_erpserver``: same as erpserver
  - ``test_web``: webapi + webgui
  - ``test_worker``: same as worker
  - ``test_fingerprint``: same as fingerprint
  - ``test_browser``: selenium

**Documentation**

- Purpose: Manual/Automated builds of the documentation
- Files

  - ``docker-compose.documentation.yml``

- Usage: ``docker-compose -f docker-compose.documentation.yml COMMAND``
- Services:

  - ``documentation``: sphinx build container

For more information, look into the ``docker-compose*.yml`` files.

.. _Docker Images:

Images
''''''

All images for all 3 docker-compose setups are based on the same Dockerfile,
which is located in ``./services/build/Dockerfile``. The key concepts for this
image setup are:

- Some and only those images not intended for production use are imported from
  **Dockerhub** (nginx, postgres, selenium).
- All custom built images are based on **Debian**.
- It is a **multistage** build. This means, that all intermediate stages can be
  reused for multiple images, leading to a stage hierarchy tree.
- There are **2 branches** in the tree:

  - The **compile** branch contains the libraries needed for the compilation of
    the packages/applications.
  - The **service** branch contains only the runtime dependencies for the
    packages/applications.

- The packages/applications are compiled on images of the compile branch and in
  the end **copied** to the images on the service branch, which are used for
  the actual services.
- Each image stage has **4 substages** for the different `environments`_:

  - The **production** substage contains only the minimum of packages needed.
  - The **staging** substage adds packages for stating.
  - The **testing** substage adds packages for tests/CI/documentation.
  - The **development** substage adds packages to develop comfortably.

- The reason for both the division of compile/service branches as well as the
  substages matching the environment is to have **slimmer** images, **smaller**
  attack surfaces and a **faster** build time.
- All images based on ``jessie_python`` use
  ``volumes/shared/docker-entrypoint.sh`` as entrypoint to detect and execute
  `CLI`_ commands provided by the ``volumes/shared/cli`` script.

The tree of the stages of the service branch (without substages)::

                                   jessie_base
                                        |
                                  jessie_python
               _________________________|___________________________
              |                 |                |                  |
       jessie_trytond    jessie_worker    jessie_echoprint    jessie_compile
          |       |             |                |                  |
    erpserver   webapi        worker        fingerprint       documentation
                  |
                webgui

The tree of the stages of the compile branch (without substages)::

                                   jessie_base
                                        |
                                  jessie_python
                                        |
                                  jessie_compile
                                        |
                              jessie_python_compiled
               _________________________|__________________________
              |                         |                          |
    jessie_trytond_compiled   jessie_worker_compiled   jessie_echoprint_compiled
              |
    jessie_pyramid_compiled

The copy relations:

============= ====================================
Image         Copy Sources
============= ====================================
erpserver     jessie_trytond_compiled
webapi        jessie_pyramid_compiled
webgui        jessie_pyramid_compiled
worker        jessie_worker_compiled
fingerprint   jessie_echoprint_compiled
documentation | jessie_trytond_compiled
              | jessie_pyramid_compiled
              | jessie_worker_compiled
============= ====================================

Packages
--------

This setup maintains three levels of package inclusion:

    1. Debian packages
    2. Python packages installed with pip
    3. Source repositories for development purposes

Debian
''''''

The Debian packages installed for the applications can be found in the
Dockerfile and are pinned, where reasonable. For a list of packages, search
for ``apt-get install`` in ``./services/build/Dockerfile``.

Pip
'''

The pip packages installed for the applications also can be found in the
Dockerfile and are all pinned. For a list of packages, search for
``pip install`` in ``./services/build/Dockerfile``.

The source code of those packages can also be found in the folder
``./volumes/shared/ref/`` and are provided for reference and for quick lookups
during development. The source code is not used though. The repositories are
cloned on the first run of the `project script`_ update command and can be
configured in ``./project.yml``:

.. code-block:: yaml

    development:
      tasks:
        update:
          - name: checkout repos of pinned pip packages for reference
            batch:
              - name: <REPOFOLDER>
                source: <REPOSOURCE>
                version: tags/<TAG>

Repositories
''''''''''''

Those packages, which are either under development or need to be updated
regulary are git cloned into the folder ``./volumes/shared/src/``. Those packages
are pip installed during runtime each time a container is started. The list of
package requirements for each service container can be found in
``./services/pip/<SERVICE>.pip``.

The repositories are cloned and updated on each run of the `project script`_
update/pull command and can be configured in ``./project.yml``:

.. code-block:: yaml

    production:
      tasks:
        update:
          - name: update project repos
            batch:
              - name: <REPOFOLDER>
                source: <REPOSOURCE>
          - name: update upstream repos
            batch:
              - name: <REPOFOLDER>
                source: <REPOSOURCE>
                version: <BRANCH>

Services
--------

To start all services with stdin attached to the service logs, use::

    $ docker-compose up

To start all services detached::

    $ docker-compose up -d

If you want to start only a certain service with its dependencies, use::

    $ docker-compose run --rm --service-ports SERVICE    service-deploy
      '---------------------------------------------'    '-------------'
                      host command                      container command

    $ docker-compose run --rm --service-ports webgui     service-deploy
    $ docker-compose run --rm --service-ports webapi     service-deploy
    $ docker-compose run --rm --service-ports erpserver  service-deploy

The host command explained:

    - ``docker-compose run``: Run a one-off command in a new container
    - ``--rm``: The run command won't remove the stopped container by
      default, so that it can be inspected after the run. To prevent the
      aggregation of stopped container states, this switch is recommended.
    - ``--service-ports``: The run command is intended to be used, while
      the services are already running and does not map the service ports by
      default to prevent the port being allocated twice. This switch is used
      to enable the mapping of the service ports.
    - ``SERVICE``: The service on which the command is executed

The container command explained:

    - ``service-deploy``: The `service-deploy CLI`_ command to start the
      application

.. note:: The deploy scripts can be found in ``services/deploy/SERVICE``.

To open a shell on a new container::

    $ docker-compose run --rm [--service-ports] SERVICE bash

.. warning:: Manual changes are not persisted when the container is stopped.

To open a shell on a running container::

    $ docker-compose exec SERVICE bash

Trytond
'''''''

For the development of tryton modules it is recommended to open two shells
within the erpserver:

- One shell is to start the trytond server manually, as it often needs to be
  restarted.
- The other shell is for the database update command to apply the changes to
  the database.

1. Start the first terminal, open a bash in the erpserver and start trytond::

    $ docker-compose run --rm --service-ports erpserver bash
    > service-deploy

   To restart the trytond server::

    > <Ctrl+c>
    > service-deploy

2. Start the second terminal, open another bash in the running container::

    $ docker exec -it $(docker ps -a | grep ":8000" | cut -d' ' -f1) bash

   To update the collecting_society module for the database::

    > db-update

   To update all modules for the database::

    > db-update -m all

To connect to Trytond with the Tryton client, see `Tryton Usage`_.

.. note:: Start Tryton with the ``-d/--debug`` flag to disable caching.

You can now start coding:

======================================== =================================
``code/collecting_society/``             trytond main module
``services/config/collecting_society.*`` trytond server config files
``~/.config/tryton/3.4/``                tyton client config files
``volumes/shared/src/``                  all trytond module repositories
``volumes/trytond-files/``               trytond file storage
======================================== =================================

.. seealso:: `Trytond Config`_ and `C3S Redmine Wiki: Tryton HowTo`__

__ https://redmine.c3s.cc/projects/collecting_society/wiki/HowTo#Tryton

Lint the code::

    docker-compose exec erpserver flake8 src/collecting_society

Pyramid
'''''''

For the development of the pyramid application, it is sufficiant to just start
all services with stdin attached to the service logs::

    $ docker-compose up

The application will monitor changes to files and restart itself automatically.
You can now start coding:

============================================ =========================================
``code/portal_web/``                         pyramid main application code
``code/collecting_society_web/``             pyramid plugin code
``services/config/portal_web.*``             pyramid main application config files
``services/config/collecting_society_web.*`` pyramid plugin config files
``volumes/shared/ref/``                      pinned python package repos for reference
``volumes/shared/tmp/logs``                  log folder for some debugging flags
``volumes/shared/tmp/session``               cookie session data files
``volumes/shared/tmp/upload``                upload folder for audio/pdfs
============================================ =========================================

.. seealso:: `Pyramid Config`_

Lint the code::

    docker-compose exec webgui flake8 src/portal_web src/collecting_society_web

Debugging
---------

Pdb
'''

``Pdbpp`` ist installed in all images with python installed and should work out
of the box. Just add the line in the python file::

    import pdb; pdb.set_trace()

If you want to debug a **service**, you need to start the service via the
``run`` command to attach stdin/stdout and add the ``--service-port`` flag::

    $ docker-compose run --rm --service-ports SERVICE service-deploy

If you want to debug `application tests`_, you can add the ``--pdb`` flag to
the `service-test script`_ or the `service-test CLI`_ command to jump into
pdb on errors automatically.

If you want to debug the `demodata`_ generation, you can add the ``--pdb``
flag to the `db-rebuild CLI`_ command to jump into pdb on errors
automatically.

Ptvsd
'''''

If you use Visual Studio Code as your editor, you would want to install the
Remote Containers extension, so you can work directly in the docker containers,
including source level debugging from within VS Code. Just make sure that
the environment variables in `.env`_ have the right values::

    ENVIRONMENT=development
    DEBUGGER_PTVSD=1

Now rebuild the docker images for the packages to be installed, ``cd`` to
``collecting_society_docker`` and start VSCode with ``"code ."``. The necessary
``.devcontainer.json`` and ``launch.json`` files are already included in the
repositories.

To start debugging a container, click on the toast notification that will come
up in the bottom right corner or click on the green field in the lower left
corner of VS Code and select ``Remote-Containers: Reopen in Container``. Then
make sure the Python extension is installed in the container's VS Code instance
and reload, if necessary. *Git History* and *GitLens* are recommended but will
require you to ``"apt-get install git"`` in the container. To start debugging,
press ``Ctrl-Shift-D`` to open the debug sidebar and select the debug
configuration in the drop-down box on the top, e.g. *'Portal Attach'*
(Settings for attaching the container can be adjusted in the file
``./volumes/shared/.vscode/launch.settings``). Press the play button left to
the debug config drop-down box and a debug toolbar should appear.

.. note:: If you wish to debug other containers besides the default
    *webgui*, e.g. *webapi* or *worker*, change the ``service`` entry in
    ``.devcontainer.json`` accordingly, otherwise you will experience
    'connection refused' errors. The ``service`` entry in
    ``.devcontainer.json`` will determine which container is being selected by
    the *Remote-Containers* plugin.

Winpdb
''''''

To allow the winpdb debugger to attach to a portal script, make sure that
the environment variables in `.env`_ have the right values::

    ENVIRONMENT=development
    DEBUGGER_WINPDB=1

Now rebuild the docker images for the packages to be installed an in your
python file insert::

    import rpdb2; rpdb2.start_embedded_debugger("password", fAllowRemote = True)

Make sure to open a port for the remote debugger in
``docker-compose.development.yml``::

    ports:
      - "51000:51000"

Install winpdb also outside the container and run it::

    $ sudo apt-get install -y winpdb
    $ winpdb

The processing container can be setup for debugging the same way. Make sure to
only enable either of the both containers for debugging, not both the same
time.

.. _Application Tests:

Tests
-----

The tests are performed on separate containers. To build the images on the
first run, use the ``--build`` flag of the `service-test script`_::

    $ ./service-test --build

Run tests for all services (web, erpserver, worker)::

    $ ./service-test

If you develop the tests and need to start them more than once, you can
use the ``--keep`` flag, to keep the container running and use the command
multiple times::

    $ ./service-test --keep

To stop and remove the container, when you have finished, enter ::

    $ ./service-test --down

.. note:: All commits pushed to all C3S GitHub repositories are automatically CI tested with
    `jenkins`__ (needs authentication) using the same test script.

__ https://jenkins1b.c3s.cc/job/collecting_society/

Trytond
'''''''

Run all trytond tests (module tests, scenario doctests) once::

    $ ./service-test erpserver

Run all trytond tests and keep the container running for the next test run::

    $ ./service-test erpserver --keep

Stop the container afterwards::

    $ ./service-test --down

If you prefer, you can also execute the commands above from within the container::

    $ docker-compose -f docker-compose.testing.yml up -d
    $ docker-compose -f docker-compose.testing.yml exec test_erpserver bash

        # setup container
        > pip-install
        > export DB_NAME=:memory:

        # run tests
        > service-test

        # run tests directly
        > python /shared/src/trytond/trytond/tests/run-tests.py -vvvm collecting_society

        # exit container
        > exit

    $ docker-compose -f docker-compose.testing.yml down

Worker
''''''

Run all worker tests (module tests, scenario doctests) once::

    $ ./service-test worker

Run all trytond tests and keep the container running for the next test run::

    $ ./service-test worker --keep

Stop the container afterwards::

    $ ./service-test --down

.. note:: The following commands will use the ``--keep`` flag by default. It
    will highly speed up the execution time, if you run the tests more than
    once.

You can append the normal nosetest parameters::

    $ ./service-test worker --keep [--path PATH] [PARAMETER]

- Run all tests quietly, drop into pdb on errors::

    $ ./service-test worker --keep --quiet --pdb

- Run a specific set of tests::

    $ ./service-test worker --keep --path PATH[/FILE[:CLASS[.METHOD]]]

  For example::

    $ TESTPATH=src/collecting_society_worker/collecting_society_worker/tests

    $ ./service-test worker --keep \
        --path $TESTPATH/integration
    $ ./service-test worker --keep \
        --path $TESTPATH/integration/test_processing.py
    $ ./service-test worker --keep \
        -- path $TESTPATH/integration/test_processing.py:TestProcessing.test_200_checksum

Recreate the database template, if the database has changed::

    $ ./service-test worker --keep --build

If you prefer, you can also execute the commands above from within the container::

    $ docker-compose -f docker-compose.testing.yml up -d
    $ docker-compose -f docker-compose.testing.yml exec test_worker bash

        # run tests
        > service-test [--path PATH] [PARAMETER...]

        # rebuild database template
        > db-rebuild --no-template -d production collecting_society_test_template

        # exit container
        > exit

    $ docker-compose -f docker-compose.testing.yml down

The rendered HTML output of the coverage can be accessed via::

    firefox volumes/shared/cover_worker/index.html

Pyramid
'''''''

Run all pyramid tests once::

    $ ./service-test web

Run all pyramid tests and keep the container running for the next test run::

    $ ./service-test web --keep

Stop the container afterwards::

    $ ./service-test --down

.. note:: The following commands will use the ``--keep`` flag by default. It
    will highly speed up the execution time, if you run the tests more than
    once.

You can append the normal nosetest parameters::

    $ ./service-test web --keep [--path PATH] [PARAMETER]

- Run all tests quietly, drop into pdb on errors::

    $ ./service-test web --keep --quiet --pdb

- Run a specific set of tests::

    $ ./service-test web --keep --path PATH[/FILE[:CLASS[.METHOD]]]

  For example::

    $ ./service-test web --keep \
        --path src/portal_web/portal_web/tests/unit
    $ ./service-test web --keep \
        --path src/portal_web/portal_web/tests/unit/resources.py
    $ ./service-test web --keep \
        --path src/portal_web/portal_web/tests/unit/resources.py:TestResources
    $ ./service-test web --keep \
        --path src/portal_web/portal_web/tests/unit/resources.py:TestResources.test_add_child

Recreate the database template, if the database has changed::

    $ ./service-test web --keep --build

If you prefer, you can also execute the commands above from within the container::

    $ docker-compose -f docker-compose.testing.yml up -d
    $ docker-compose -f docker-compose.testing.yml exec test_web bash

        # run tests
        > service-test [--path PATH] [PARAMETER...]

        # rebuild database template
        > db-rebuild --no-template -d production collecting_society_test_template

        # exit container
        > exit

    $ docker-compose -f docker-compose.testing.yml down

.. note:: In the ``testing`` environment, the ``webgui`` and ``webapi``
    services run both on the ``web`` service as deployment needs to be
    coordinated and controlled by nosetest.

The rendered HTML output of the coverage can be accessed via::

    firefox volumes/shared/cover_web/index.html

The screenshots of the selenium integration tests can be found in the folder::

    volumes/shared/tmp/screenshots/

Linting
'''''''

Lint the code for the scripts in this repository::

    python2 -m flake8 scripts

Lint the code for application repositories via container::

    docker-compose exec SERVICE service-lint
    docker-compose exec SERVICE service-lint all
    docker-compose exec SERVICE service-lint --path /some/path/to/lint


.. note:: The code is also linted in the `service-test script`_.

Demodata
--------

The datasets are imported via a custom data import module using `proteus`__
with a trytond backend (not via XMLRPC). The most important files and folders
are:

__ https://docs.tryton.org/projects/client-library/en/latest/

============================================ ================================================
``volumes/shared/data/main.py``              Main function
``volumes/shared/data/datasets/__init__.py`` Definition of Dataset(s) classes
``volumes/shared/data/datasets/MODEL.py``    Dataset generation script for tryton model
``volumes/shared/data/csv/MODEL.csv``        CSV file for tryton model
``volumes/shared/data/csv/MODEL.py``         Script to generate the CSV file for tryton model
============================================ ================================================

A minimal working dataset consists of two attributes::

    #!/usr/bin/env python
    DEPENDS = []            # A list of other datasets to be build first
    generate(reclimit=0):   # The function to generate the datasets
        pass

.. note:: The dataset ``production`` is a special stage tag to separate the
    provision, which is neccessary for technical reasons from pure demodata.

Rebuild
'''''''

In the ``development`` and ``staging`` environment, the demodata is created
automatically during the setup of the database. If you need to rebuild the
database, just use your prefered method:

* via `db-rebuild script`_::

    $ ./db-rebuild

* via `db-rebuild CLI`_ command on a running container::

    $ docker-compose exec erpserver db-rebuild

* via `db-rebuild CLI`_ command on a new container::

    $ docker-compose run --rm erpserver db-rebuild

* via `db-rebuild CLI`_ command inside the *erpserver* container::

    > db-rebuild

The generation script will output some useful information during the run:

- *Configuration* of the run
- *Name* of the dataset
- *Description* of the dataset
- *Models* created/deleted/copied/updated and *Wizards* executed
- *Duration* of the generation

Update
''''''

If you want to change a certain dataset for a model without constantly generating
the demo data from scratch, this workflow is highly recommended:

1. Apply the changes to ``datasets/MODEL.py``.
2. Test your changes by generating the MODEL dataset using the
   `db-rebuild CLI`_ command::

    $ docker-compose run --rm erpserver bash
    > db-rebuild -d MODEL

3. While there are errors, fix them and retest using the ``--cache`` flag::

    > db-rebuild -d MODEL --cache

4. Retest the whole generation::

    > db-rebuild

5. Commit the changes.

If you want to change several datasets, you can prepare a template for the
most time consuming master dataset and start the data generation from it with
the ``-e/--exclude`` flag::

    > db-rebuild --no-template -d production collecting_society_template
    > db-rebuild -e production -d <DATASET>

You can also prepare a template for any dataset and copy it for later use::

    > db-rebuild --no-template -d production collecting_society_artist
    > db-copy --force collecting_society_artist collecting_society_template
    > db-rebuild -e artist -d <DATASET>

Create
''''''

If you want to create a new dataset, you can use this template and take a look
at the other datasets to see, how it works::

    #!/usr/bin/env python
    # -*- coding: UTF-8 -*-
    # For copyright and license terms, see COPYRIGHT.rst (top level of repository)
    # Repository: https://github.com/C3S/collecting_society_docker

    """
    Create the <MODEL>s
    """

    from proteus import Model

    DEPENDS = [
        '<DATASET>',
    ]


    def generate(reclimit=0):

        # constants

        # models

        # wizards

        # entries

        # content

        # create <MODEL>s

.. note:: All ``datasets/*.py`` files are registered automatically as new
    datasets on each run.

.. _Project Documentation:

Documentation
-------------

The documentation is built with Sphinx and integrates the documentation of all
collecting society applications. It contains both the ``*.rst`` files
(e.g. ``README.rst``) of the application repositories, as well as the python
code api generated via *autoapi*.

The build process runs on a special ``documentation`` service container, because for
*autoapi* the python modules need to be imported. To create the image for the
container on the first built, use the ``--build`` flag of the
`docs-build script`_::

    $ ./docs-build --build

To build the documentation afterwards, you can then just use::

    $ ./docs-build

If you edit the documentation and need to build it more than once, you can
use the ``--keep`` flag, to keep the container running and use the command
successively::

    $ ./docs-build --keep

To stop and remove the container, when you have finished, enter ::

    $ ./docs-build --down

If you did not change any ``*.py`` files, you can use the ``--no-autoapi`` flag
to omit the *autoapi* step and speed up the build::

    $ ./docs-build --keep --no-autoapi

If you prefer, you can also execute the commands above from within the container::

    $ docker-compose -f docker-compose.documentation.yml up -d
    $ docker-compose -f docker-compose.documentation.yml exec documentation bash

        # build documentation via script
        > docs-build

        # build with autoapi omitted
        > docs-build --no-autoapi

        # exit container
        > exit

    $ docker-compose -f docker-compose.documentation.yml down

The main source files can be found in the ``./volumes/shared/docs/source/``
folder.

.. warning:: Don't edit the ``*.rst`` files in the subfolders, because those
    are symlinked or generated by autoapi.

Once built, the docs can be viewed (from outside the container) like this::

    $ firefox docs/index.html

.. seealso:: `Sphinx rst Markup`__

__ https://www.sphinx-doc.org/en/1.5/markup/inline.html


Problems
--------

Docker
''''''

**Couldn't connect to Docker daemon**

**Docker-compose cannot start container <id> port has already been allocated**

If docker fails to start and you get messages like this:
"Couldn't connect to Docker daemon at http+unix://var/run/docker.sock
[...]" or "docker-compose cannot start container <docker id> port has already
been allocated"

1. Check if the docker service is started::

    $ sudo systemctl start docker

2. Check if any user of docker is member of group ``docker``::

    $ login
    $ groups | grep docker

Tryton
''''''

**Bad Fingerprint**

If the Tryton client already connected the *tryton*-container, the fingerprint
check could restrict the login with the message: Bad Fingerprint!

That means the fingerprint of the server certificate changed.
In production use, the ``Bad fingerprint`` alert is a sign that someone
could try to *fish* your login credentials with another server responding your
client.
Ask the server administrator if the certificate has changed.

Close the Tryton client.
Check the problematic host entry in ``~/.config/tryton/3.4/known_hosts``.
Add a new fingerprint provided by the server administrator or
simply remove the whole file, if the setup is not in production use::

    rm ~/.config/tryton/3.4/known_hosts

**Incompatible Server Version**

If the tryton client shows an "incompatible server version" error on login try::

    rm ~/.config/tryton/3.4/known_hosts

License
=======

For infos on copyright and licenses, see ``./COPYRIGHT.rst``.

