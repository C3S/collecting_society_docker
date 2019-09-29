# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

environment = "development"
tryton_version = "3.4"
ref = "shared/ref/"
src = "shared/src/"

repositories = (
    # (
    #     git repository url or None.
    #     git clone option, required if repository is given.
    #     relative path to create or clone.
    # ),
    (
        None,
        None,
        'postgresql-data'
    ),
    (
        None,
        None,
        'shared/var/lib/trytond'
    ),

    # sourcecode of libraries for reference
    (
        'https://github.com/pallets/click.git',
        '--tag=4.0',
        ref + 'click'
    ),
    (
        'https://github.com/requests/requests.git',
        '--tag=v2.18.4',
        ref + 'requests'
    ),
    (
        'https://github.com/psycopg/psycopg2.git',
        '--tag=2_5_4',
        ref + 'psycopg2'
    ),
    (
        'https://github.com/tryton/proteus.git',
        '--branch=' + tryton_version,
        ref + 'proteus'
    ),
    (
        'https://github.com/Pylons/webob.git',
        '--tag=v1.8.2',
        ref + 'webob'
    ),
    (
        'https://github.com/Pylons/pyramid.git',
        '--tag=1.9.2',
        ref + 'pyramid'
    ),
    (
        'https://github.com/Pylons/pyramid_beaker.git',
        '--tag=0.8',
        ref + 'pyramid_beaker'
    ),
    (
        'https://github.com/Pylons/pyramid_chameleon.git',
        '--tag=0.3',
        ref + 'pyramid_chameleon'
    ),
    (
        'https://github.com/Pylons/pyramid_mailer.git',
        '--tag=0.15.1',
        ref + 'pyramid_mailer'
    ),
    (
        'https://github.com/Pylons/colander.git',
        '--tag=1.4',
        ref + 'colander'
    ),
    (
        'https://github.com/Cornices/cornice.git',
        '--tag=3.4.0',
        ref + 'cornice'
    ),
    (
        'https://github.com/Pylons/deform.git',
        '--tag=2.0.5',
        ref + 'deform'
    ),
    (
        'https://github.com/jiaaro/pydub.git',
        '--tag=v0.22.0',
        ref + 'pydub'
    ),
    (
        'https://github.com/supermihi/pytaglib.git',
        '--tag=v1.4.3',
        ref + 'pytaglib'
    ),
    (
        'https://github.com/echonest/pyechonest.git',
        '--tag=9.0.0',
        ref + 'pyechonest'
    ),

    # included repositories: tryton upstream
    (
        'https://github.com/tryton/trytond.git',
        '--branch=' + tryton_version,
        src + 'trytond'
    ),
    (
        'https://github.com/tryton/country.git',
        '--branch=' + tryton_version,
        src + 'country'
    ),
    (
        'https://github.com/tryton/currency.git',
        '--branch=' + tryton_version,
        src + 'currency'
    ),
    (
        'https://github.com/tryton/party.git',
        '--branch=' + tryton_version,
        src + 'party'
    ),
    (
        'https://github.com/tryton/company.git',
        '--branch=' + tryton_version,
        src + 'company'
    ),
    (
        'https://github.com/tryton/product.git',
        '--branch=' + tryton_version,
        src + 'product'
    ),
    (
        'https://github.com/tryton/account.git',
        '--branch=' + tryton_version,
        src + 'account'
    ),
    (
        'https://github.com/tryton/account_product.git',
        '--branch=' + tryton_version,
        src + 'account_product'
    ),
    (
        'https://github.com/tryton/account_invoice.git',
        '--branch=' + tryton_version,
        src + 'account_invoice'
    ),
    (
        'https://github.com/tryton/account_invoice_line_standalone.git',
        '--branch=' + tryton_version,
        src + 'account_invoice_line_standalone'
    ),
    (
        'https://github.com/tryton/bank.git',
        '--branch=' + tryton_version,
        src + 'bank'
    ),
    (
        'https://github.com/virtualthings/web_user.git',
        '--branch=' + tryton_version,
        src + 'web_user'
    ),

    # included repositories: tryton custom
    (
        'https://github.com/C3S/archiving.git',
        '--branch=' + environment,
        src + 'archiving'
    ),
    (
        'https://github.com/C3S/portal.git',
        '--branch=' + environment,
        src + 'portal'
    ),
    (
        'https://github.com/C3S/collecting_society.git',
        '--branch=' + environment,
        src + 'collecting_society'
    ),

    # included repositories: pyramid
    (
        'https://github.com/C3S/portal_web.git',
        '--branch=' + environment,
        src + 'portal_web'
    ),
    (
        'https://github.com/C3S/collecting_society_web.git',
        '--branch=' + environment,
        src + 'collecting_society_web'
    ),

    # included repositories: worker
    (
        'https://github.com/C3S/collecting_society_worker.git',
        '--branch=master',
        src + 'collecting_society_woker'
    ),
    (
        'https://github.com/spotify/echoprint-codegen.git',
        '--branch=master',
        src + 'echoprint-codegen'
    ),
)

configfiles = (
    (
        'shared/etc/trytonpassfile.example',
        'shared/etc/trytonpassfile',
    ),
    (
        'tryton.env.example',
        'tryton.env'
    ),
    (
        'portal.env.example',
        'portal.env'
    ),
    (
        'api.env.example',
        'api.env'
    ),
    (
        'processing.env.example',
        'processing.env'
    ),
    (
        'selenium.env.example',
        'selenium.env'
    ),
    (
        'shared/src/collecting_society_worker/config.ini.EXAMPLE',
        'shared/src/collecting_society_worker/config.ini'
    ),
)
