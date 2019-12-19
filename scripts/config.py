#!/usr/bin/env python3
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker
"""
Configures folders to create, files to copy and repos to clone.

Meant to be included. Direct execution prints the configuratin.

Usage: ./config.py
"""

import os
import subprocess
import re


def get_root_dir():
    """Returns the root dir of the repository."""
    try:
        return subprocess.check_output(
            ['git', 'rev-parse', '--show-toplevel'], stderr=subprocess.STDOUT
        ).rstrip().decode('utf-8')
    except subprocess.CalledProcessError:
        directory = os.path.dirname(os.path.realpath(__file__))
        return os.path.realpath(os.path.join(directory, ".."))


# directories
dirs = {}
dirs['root'] = get_root_dir()
dirs['code'] = dirs['root'] + "/code"
dirs['scripts'] = dirs['root'] + "/scripts"
dirs['services'] = dirs['root'] + "/services"
dirs['volumes'] = dirs['root'] + "/volumes"
dirs['shared'] = dirs['volumes'] + "/shared"
dirs['ref'] = dirs['shared'] + "/ref"
dirs['src'] = dirs['shared'] + "/src"
dirs['tmp'] = dirs['shared'] + "/tmp"
dirs['logs'] = dirs['tmp'] + "/logs"


def get_shared_env(path=False):
    """Reads the shared environment file and parses it into a dictionary."""

    # get path
    if not path:
        path = os.path.join(dirs['root'], '.env')
    if not os.path.isfile(path):
        path = os.path.join(dirs['root'], '.env.example')
    assert os.path.isfile(path)

    # parse file
    result = {}
    envre = re.compile(r'''^([^\s=]+)=(?:[\s"']*)(.+?)(?:[\s"']*)$''')
    with open(path) as ins:
        for line in ins:
            match = envre.match(line)
            if match is not None:
                result[match.group(1)] = match.group(2)
    return result


# shared env
env = get_shared_env()

# branch
branch = "master"
if env['ENVIRONMENT'] in ["development", "testing"]:
    branch = "develop"

# folders to create
create_folders = [
    dirs['code'],
    dirs['tmp'],
    dirs['logs'],
]
if env['ENVIRONMENT'] in ["development", "testing"]:
    create_folders += [
        dirs['volumes'] + '/postgresql-data',
        dirs['volumes'] + '/trytond-files',
        dirs['volumes'] + '/nginx-certs',
        dirs['volumes'] + '/nginx-dhparam',
    ]

# files to copy
copy_files = [
    {
        'source': dirs['root'] + '/.env.example',
        'target': dirs['root'] + '/.env'
    },
    {
        'source': dirs['shared'] + '/config/trytond/passfile.example',
        'target': dirs['shared'] + '/config/trytond/passfile',
    },
    {
        'source': dirs['services'] + '/webgui.env.example',
        'target': dirs['services'] + '/webgui.env'
    },
    {
        'source': dirs['services'] + '/webapi.env.example',
        'target': dirs['services'] + '/webapi.env'
    },
    {
        'source': dirs['services'] + '/worker.env.example',
        'target': dirs['services'] + '/worker.env'
    },
    {
        'source':
            dirs['src'] + '/collecting_society_worker/config.ini.example',
        'target': dirs['src'] + '/collecting_society_worker/config.ini'
    },
]

# source repositories to clone
clone_sources = [
    # upstream: tryton
    {
        'url': 'https://github.com/tryton/trytond.git',
        'option': '--branch=' + env['TRYTON_VERSION'],
        'path': 'trytond'
    },
    {
        'url': 'https://github.com/tryton/country.git',
        'option': '--branch=' + env['TRYTON_VERSION'],
        'path': 'country'
    },
    {
        'url': 'https://github.com/tryton/currency.git',
        'option': '--branch=' + env['TRYTON_VERSION'],
        'path': 'currency'
    },
    {
        'url': 'https://github.com/tryton/party.git',
        'option': '--branch=' + env['TRYTON_VERSION'],
        'path': 'party'
    },
    {
        'url': 'https://github.com/tryton/company.git',
        'option': '--branch=' + env['TRYTON_VERSION'],
        'path': 'company'
    },
    {
        'url': 'https://github.com/tryton/product.git',
        'option': '--branch=' + env['TRYTON_VERSION'],
        'path': 'product'
    },
    {
        'url': 'https://github.com/tryton/account.git',
        'option': '--branch=' + env['TRYTON_VERSION'],
        'path': 'account'
    },
    {
        'url': 'https://github.com/tryton/account_product.git',
        'option': '--branch=' + env['TRYTON_VERSION'],
        'path': 'account_product'
    },
    {
        'url': 'https://github.com/tryton/account_invoice.git',
        'option': '--branch=' + env['TRYTON_VERSION'],
        'path': 'account_invoice'
    },
    {
        'url': 'https://github.com/tryton/account_invoice_line_standalone.git',
        'option': '--branch=' + env['TRYTON_VERSION'],
        'path': 'account_invoice_line_standalone'
    },
    {
        'url': 'https://github.com/tryton/bank.git',
        'option': '--branch=' + env['TRYTON_VERSION'],
        'path': 'bank'
    },
    {
        'url': 'https://github.com/virtualthings/web_user.git',
        'option': '--branch=' + env['TRYTON_VERSION'],
        'path': 'web_user'
    },
    # custom: tryton
    {
        'url': 'https://github.com/C3S/archiving.git',
        'ssh': 'git@github.com:C3S/archiving.git',
        'option': '--branch=' + branch,
        'path': 'archiving',
        'symlink': True
    },
    {
        'url': 'https://github.com/C3S/portal.git',
        'ssh': 'git@github.com:C3S/portal.git',
        'option': '--branch=' + branch,
        'path': 'portal',
        'symlink': True
    },
    {
        'url': 'https://github.com/C3S/collecting_society.git',
        'ssh': 'git@github.com:C3S/collecting_society.git',
        'option': '--branch=' + branch,
        'path': 'collecting_society',
        'symlink': True
    },
    # custom: pyramid
    {
        'url': 'https://github.com/C3S/portal_web.git',
        'ssh': 'git@github.com:C3S/portal_web.git',
        'option': '--branch=' + branch,
        'path': 'portal_web',
        'symlink': True
    },
    {
        'url': 'https://github.com/C3S/collecting_society_web.git',
        'ssh': 'git@github.com:C3S/collecting_society_web.git',
        'option': '--branch=' + branch,
        'path': 'collecting_society_web',
        'symlink': True
    },
    # upstream: worker
    {
        'url': 'https://github.com/spotify/echoprint-codegen.git',
        'option': '--branch=master',
        'path': 'echoprint-codegen'
    },
    # custom: worker
    {
        'url': 'https://github.com/C3S/echoprint-server.git',
        'ssh': 'git@github.com:C3S/echoprint-server.git',
        'option': '--branch=master',
        'path': 'echoprint-server',
        'symlink': True
    },
    {
        'url': 'https://github.com/C3S/collecting_society_worker.git',
        'ssh': 'git@github.com:C3S/collecting_society_worker.git',
        'option': '--branch=master',
        'path': 'collecting_society_worker',
        'symlink': True
    },
]

# reference repositories to clone development stage only
clone_references = [
    {
        'url': 'https://github.com/pallets/click.git',
        'option': '--tag=4.0',
        'path': 'click'
    },
    {
        'url': 'https://github.com/requests/requests.git',
        'option': '--tag=v2.18.4',
        'path': 'requests'
    },
    {
        'url': 'https://github.com/psycopg/psycopg2.git',
        'option': '--tag=2_5_4',
        'path': 'psycopg2'
    },
    {
        'url': 'https://github.com/tryton/proteus.git',
        'option': '--branch=' + env['TRYTON_VERSION'],
        'path': 'proteus'
    },
    {
        'url': 'https://github.com/Pylons/webob.git',
        'option': '--tag=v1.8.2',
        'path': 'webob'
    },
    {
        'url': 'https://github.com/Pylons/pyramid.git',
        'option': '--tag=1.9.2',
        'path': 'pyramid'
    },
    {
        'url': 'https://github.com/Pylons/pyramid_beaker.git',
        'option': '--tag=0.8',
        'path': 'pyramid_beaker'
    },
    {
        'url': 'https://github.com/Pylons/pyramid_chameleon.git',
        'option': '--tag=0.3',
        'path': 'pyramid_chameleon'
    },
    {
        'url': 'https://github.com/Pylons/pyramid_mailer.git',
        'option': '--tag=0.15.1',
        'path': 'pyramid_mailer'
    },
    {
        'url': 'https://github.com/Pylons/colander.git',
        'option': '--tag=1.4',
        'path': 'colander'
    },
    {
        'url': 'https://github.com/Cornices/cornice.git',
        'option': '--tag=3.4.0',
        'path': 'cornice'
    },
    {
        'url': 'https://github.com/Cornices/cornice.ext.swagger.git',
        'option': '--tag=0.7.0',
        'path': 'cornice_swagger'
    },
    {
        'url': 'https://github.com/Pylons/deform.git',
        'option': '--tag=2.0.5',
        'path': 'deform'
    },
    {
        'url': 'https://github.com/jiaaro/pydub.git',
        'option': '--tag=v0.22.0',
        'path': 'pydub'
    },
    {
        'url': 'https://github.com/supermihi/pytaglib.git',
        'option': '--tag=v1.4.3',
        'path': 'pytaglib'
    },
    {
        'url': 'https://github.com/echonest/pyechonest.git',
        'option': '--tag=9.0.0',
        'path': 'pyechonest'
    },
]

if __name__ == "__main__":
    import pprint
    print("CONFIG\n------\n")
    pprint.pprint({
        'env': env,
        'option': branch,
        'dirs': dirs,
        'create_folders': create_folders,
        'copy_files': copy_files,
        'clone_sources': clone_sources,
        'clone_references': clone_references,
    })
