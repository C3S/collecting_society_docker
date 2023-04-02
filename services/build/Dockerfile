ARG ENVIRONMENT
ARG WORKDIR
ARG DEBUGGER_WINPDB
ARG DEBUGGER_DEBUGPY


#==============================================================================
# Base Images (Debian)
#==============================================================================

#--- BASE ---------------------------------------------------------------------

### production
FROM debian:bookworm-slim AS base_production
# set workdir
ARG WORKDIR
ENV WORKDIR $WORKDIR
ENV PATH $PATH:$WORKDIR
RUN mkdir -p $WORKDIR
WORKDIR $WORKDIR
# configure apt
ENV DEBIAN_FRONTEND noninteractive
# install base packages
RUN apt-get update && apt-get install -y --no-install-recommends \
        locales \
        ssl-cert \
        ca-certificates \
        libmagic1 \
    && rm -rf /var/lib/apt/lists/*
# configure language
RUN localedef -i en_US -f UTF-8 en_US.UTF-8
ENV LANGUAGE en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8

### staging
FROM base_production AS base_staging

### testing
FROM base_staging AS base_testing

### development
FROM base_testing AS base_development
# install development packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    && apt-get install -y --no-install-recommends \
        git \
        htop \
        iputils-ping \
        net-tools \
        vim \
        nano \
    && rm -rf /var/lib/apt/lists/*

### result
FROM base_${ENVIRONMENT} AS base


#--- base -> PYTHON -----------------------------------------------------------

### production
FROM base AS python_production
# install python
ENV PYTHONUNBUFFERED 1
RUN apt-get update && apt-get install -y --no-install-recommends \
    && apt-get install -y --no-install-recommends \
        curl \
        python3 \
        python3-distutils \
        python3-pip \
        python3-venv \
    && rm -rf /var/lib/apt/lists/*
# create virtual environment
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
ENV VIRTUAL_ENV=/opt/venv
# upgrade essential pip packages
RUN python3 -m pip install --upgrade pip wheel
# set default entrypoint and cmd for CLI script
ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["cli --help"]

### staging
FROM python_production AS python_staging

### testing
FROM python_staging AS python_testing

### development
FROM python_testing AS python_development
ARG DEBUGGER_DEBUGPY
RUN if [ ${DEBUGGER_DEBUGPY} -ne 0 ]; then \
        apt-get update && apt-get install -y --no-install-recommends \
            && apt-get install -y --no-install-recommends \
                gnome-keyring \
                build-essential \
                wget \
            && rm -rf /var/lib/apt/lists/*; \
    fi
COPY download-vs-code-server.sh /tmp
ENV PATH="$PATH:/root/.vscode-server/bin/default_version/bin"
RUN if [ ${DEBUGGER_DEBUGPY} -ne 0 ]; then \
        /tmp/download-vs-code-server.sh; \
        code-server --start-server --install-extension ms-python.python; \
        code-server --install-extension njpwerner.autodocstring; \
        code-server --install-extension mhutchie.git-graph; \
        code-server --install-extension maattdd.gitless; \
        code-server --install-extension njqdev.vscode-python-typehint; \
        code-server --install-extension littlefoxteam.vscode-python-test-adapter; \
        code-server --install-extension matangover.mypy; \
        code-server --install-extension kevinrose.vsc-python-indent; \
        code-server --install-extension alefragnani.bookmarks; \
        code-server --install-extension ms-python.flake8; \
    fi

### result
FROM python_${ENVIRONMENT} AS python


#--- base -> python -> TRYTOND ------------------------------------------------

### production
FROM python AS trytond_production
# install database packages
RUN for i in $(seq 1 8); do mkdir -p "/usr/share/man/man${i}"; done \
    && apt-get update && apt-get install -y --no-install-recommends \
        postgresql-client-15 \
        sqlite3 \
        libxslt1.1 \
        graphviz \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /usr/share/man/*

### staging
FROM trytond_production AS trytond_staging

### testing
FROM trytond_staging AS trytond_testing

### development
FROM trytond_testing AS trytond_development

### result
FROM trytond_${ENVIRONMENT} AS trytond


#--- base -> python -> ECHOPRINT ----------------------------------------------

### production
FROM python AS echoprint_production
RUN for i in $(seq 1 8); do mkdir -p "/usr/share/man/man${i}"; done \
    && apt-get update && apt-get install -y --no-install-recommends \
        default-jre-headless \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /usr/share/man/*
RUN mkdir /opt/echoprint-data

### staging
FROM echoprint_production AS echoprint_staging

### testing
FROM echoprint_staging AS echoprint_testing

### development
FROM echoprint_testing AS echoprint_development

### result
FROM echoprint_${ENVIRONMENT} AS echoprint


#--- base -> python -> PROTEUS ------------------------------------------------

### production
FROM python AS proteus_production
RUN apt-get update && apt-get install -y --no-install-recommends \
        cron \
        ffmpeg \
        libtag1v5-vanilla \
    && rm -rf /var/lib/apt/lists/*

### staging
FROM proteus_production AS proteus_staging

### testing
FROM proteus_staging AS proteus_testing
# install database packages
RUN for i in $(seq 1 8); do mkdir -p "/usr/share/man/man${i}"; done \
    && apt-get update && apt-get install -y --no-install-recommends \
        postgresql-client-15 \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /usr/share/man/*

### development
FROM proteus_testing AS proteus_development

### result
FROM proteus_${ENVIRONMENT} AS proteus


#--- base -> python -> COMPILE ------------------------------------------------

FROM python AS compile
# install libs
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        git \
        python3-dev \
        # pip: lxml \
            libxml2-dev \
            libxslt1-dev \
        # pip: psycopg2 \
            libpq-dev \
        # pip: pyOpenSSL \
            libssl-dev \
            libffi-dev \
        # pip: pytaglib \
            libtag1-dev \
        # echoprint-codegen \
            libboost-dev \
            zlib1g-dev \
        # echoprint-server
            libbz2-dev \
            wget \
    && rm -rf /var/lib/apt/lists/*


#==============================================================================
# Compilation Images
#==============================================================================

#--- [COMPILE] PYTHON ---------------------------------------------------------

### production
FROM compile AS python_production_compiled
RUN pip install \
    click==8.1.3

### staging
FROM python_production_compiled AS python_staging_compiled

### testing
FROM python_staging_compiled AS python_testing_compiled
RUN pip install \
    autoapi==2.0.1 \
    coverage==7.2.2 \
    flake8==6.0.0 \
    mypy==1.1.1 \
    pytest==7.2.2 \
    pytest-cov==4.0.0 \
    pytest-flake8==1.1.1 \
    pytest-mock==3.10.0 \
    pytest-mypy==0.10.3 \
    types-python-dateutil==2.8.19.11 \
    types-requests==2.28.11.17 \
    Sphinx==6.1.3 \
    sphinx-rtd-theme==1.2.0 \
    tox==4.4.8

### development
FROM python_testing_compiled AS python_development_compiled
RUN pip install \
    pdbpp==0.10.3

ARG DEBUGGER_DEBUGPY
RUN if [ ${DEBUGGER_DEBUGPY} -ne 0 ]; then pip install \
        debugpy==1.6.6; \
    fi
ARG DEBUGGER_WINPDB
RUN if [ ${DEBUGGER_WINPDB} -ne 0 ]; then pip install \
        winpdb==1.4.9.2; \
    fi

### result
FROM python_${ENVIRONMENT}_compiled AS python_compiled

#--- [COMPILE] python -> ECHOPRINT --------------------------------------------

### production
FROM python_compiled AS echoprint_production_compiled

# install tokyo cabinet (from https://github.com/jon-eckstein/docker-echoprint-server)
# TODO: SSL verification temporarily disabled, reenable after upgrade. Workaround for:
# https://letsencrypt.org/docs/dst-root-ca-x3-expiration-september-2021/
RUN wget --no-check-certificate https://fallabs.com/tokyocabinet/tokyocabinet-1.4.48.tar.gz
RUN tar xvf tokyocabinet-1.4.48.tar.gz
RUN mkdir /opt/tokyocabinet/
RUN cd tokyocabinet-1.4.48 && ./configure --prefix=/opt/tokyocabinet/ && make && make install

# install tokyo tyrant
# TODO: SSL verification temporarily disabled, reenable after upgrade. Workaround for:
# https://letsencrypt.org/docs/dst-root-ca-x3-expiration-september-2021/
RUN wget --no-check-certificate https://fallabs.com/tokyotyrant/tokyotyrant-1.1.41.tar.gz
RUN tar xvf tokyotyrant-1.1.41.tar.gz
RUN mkdir /opt/tokyotyrant
RUN cd tokyotyrant-1.1.41 && ./configure --prefix=/opt/tokyotyrant/ --with-tc=/opt/tokyocabinet && make && make install

# install python packages
RUN pip install \
    web.py==0.62 \
    pyechonest==9.0.0

### staging
FROM echoprint_production_compiled AS echoprint_staging_compiled

### testing
FROM echoprint_staging_compiled AS echoprint_testing_compiled

### development
FROM echoprint_testing_compiled AS echoprint_development_compiled

### result
FROM echoprint_${ENVIRONMENT}_compiled AS echoprint_compiled

#--- [COMPILE] python -> TRYTOND ----------------------------------------------

### production
FROM python_compiled AS trytond_production_compiled
# trytond mandatory
RUN pip install \
    Genshi==0.7.7 \
    lxml==4.9.2 \
    passlib[bcrypt]==1.7.4 \
    polib==1.2.0 \
    python-dateutil==2.8.2 \
    python-sql==1.4.0 \
    python-stdnum==1.18 \
    relatorio[fodt]==0.10.1 \
    Werkzeug==2.2.3 \
    wrapt==1.15.0
# trytond optional
RUN pip install \
    gevent==22.10.2 \
    html2text==2020.1.16 \
    Pillow==9.4.0 \
    psycopg2==2.9.5 \
    pydot==1.4.2 \
    python-Levenshtein==0.20.9 \
    weasyprint==58.1
# additional
RUN pip install \
    hurry.filesize==0.9 \
    interlude==1.3.1 \
    mock==5.0.1 \
    pyOpenSSL==23.1.1 \
    pytz==2023.2 \
    requests==2.28.2
# trytond account
RUN pip install \
    simpleeval==0.9.13
# trytond currency
RUN pip install \
    forex-python==1.8 \
    pycountry==22.3.5
# proteus
RUN pip install \
    defusedxml==0.7.1

### staging
FROM trytond_production_compiled AS trytond_staging_compiled

### testing
FROM trytond_staging_compiled AS trytond_testing_compiled

### development
FROM trytond_testing_compiled AS trytond_development_compiled

### result
FROM trytond_${ENVIRONMENT}_compiled AS trytond_compiled


#--- [COMPILE] python -> trytond -> PYRAMID -----------------------------------

### production
FROM trytond_compiled AS pyramid_production_compiled
RUN pip install \
    colander==2.0 \
    cornice==6.0.1 \
    cornice-swagger==1.0.1 \
    cryptacular==1.6.2 \
    Pillow==9.4.0 \
    deform==2.0.15 \
    pyramid==2.0.1 \
    pyramid-beaker==0.8 \
    pyramid-chameleon==0.3 \
    pyramid-mailer==0.15.1 \
    python-magic==0.4.27 \
    waitress==2.1.2

### staging
FROM pyramid_production_compiled AS pyramid_staging_compiled

### testing
FROM pyramid_staging_compiled AS pyramid_testing_compiled
RUN pip install \
    raven==6.10.0 \
    selenium==4.8.0 \
    WebTest==3.0.0

### development
FROM pyramid_testing_compiled AS pyramid_development_compiled
RUN pip install \
    pyramid-debugtoolbar==4.10

### result
FROM pyramid_${ENVIRONMENT}_compiled AS pyramid_compiled


#--- [COMPILE] python -> PROTEUS ----------------------------------------------

### production
FROM python_compiled AS proteus_production_compiled
# compile echoprint-codegen
RUN git clone https://github.com/spotify/echoprint-codegen.git /opt/echoprint-codegen \
    && git -C /opt/echoprint-codegen checkout v4.12 \
    && make -C /opt/echoprint-codegen/src \
    && chmod 755 /opt/echoprint-codegen/echoprint-codegen
# install pip packages
RUN pip install  \
    defusedxml==0.7.1 \
    pyechonest==9.0.0 \
    pydub==0.25.1 \
    pytaglib==2.0.0 \
    python-dateutil==2.8.2 \
    requests==2.28.2

### staging
FROM proteus_production_compiled AS proteus_staging_compiled

### testing
FROM proteus_staging_compiled AS proteus_testing_compiled

### development
FROM proteus_testing_compiled AS proteus_development_compiled

### result
FROM proteus_${ENVIRONMENT}_compiled AS proteus_compiled


#--- [COMPILE] NODEJS ---------------------------------------------------------

### production
# TODO: upgrade when node:bookworm-slim is available
FROM node:bullseye-slim AS sao_production_compiled
RUN apt-get update && apt-get install -y --no-install-recommends \
        ca-certificates \
        git \
    && rm -rf /var/lib/apt/lists/*
ARG TRYTON_VERSION
RUN git clone -b ${TRYTON_VERSION} --single-branch https://github.com/tryton/sao.git /opt/sao \
    && chown -R node:node /opt/sao
USER node
RUN cd /opt/sao \
    && npm install --legacy-peer-deps \
    && node_modules/.bin/grunt
RUN cd /opt/sao && rm -rf \
    .??* \
    *.json \
    *.js \
    *.md \
    node_modules \
    src \
    tests

### staging
FROM sao_production_compiled AS sao_staging_compiled

### testing
FROM sao_staging_compiled AS sao_testing_compiled

### development
FROM sao_testing_compiled AS sao_development_compiled

### result
FROM sao_development_compiled AS sao_compiled


#==============================================================================
# Service Images
#==============================================================================

#--- DATABASE -----------------------------------------------------------------

FROM postgres:15 AS database


#--- WEBSERVER ----------------------------------------------------------------

FROM jwilder/nginx-proxy:1.2.1 AS webserver


#--- BROWSER ------------------------------------------------------------------

FROM selenium/standalone-firefox:4.8.0 AS browser


#--- base -> python -> echoprint -> FINGERPRINT -------------------------------

FROM echoprint AS fingerprint
COPY --from=echoprint_compiled /opt/tokyocabinet/bin/* /bin/
COPY --from=echoprint_compiled /opt/tokyocabinet/lib/libtokyocabinet.* /lib/
COPY --from=echoprint_compiled /opt/tokyotyrant/bin/* /bin/
COPY --from=echoprint_compiled /opt/tokyotyrant/lib/libtokyotyrant.* /lib/
COPY --from=echoprint_compiled /opt/tokyotyrant/lib/ttskel* /lib/
COPY --from=echoprint_compiled /opt/venv /opt/venv


#--- base -> python -> proteus -> WORKER --------------------------------------

FROM proteus AS worker
COPY --from=proteus_compiled /opt/echoprint-codegen/echoprint-codegen /usr/local/bin/echoprint-codegen
COPY --from=proteus_compiled /opt/venv /opt/venv
COPY worker.cron /etc/cron.d/worker


#--- base -> python -> trytond -> ERPSERVER -----------------------------------

FROM trytond AS erpserver
COPY --from=trytond_compiled /opt/venv /opt/venv
COPY --from=sao_compiled /opt/sao /sao


#--- base -> python -> trytond -> WEBAPI --------------------------------------

FROM trytond AS webapi
COPY --from=pyramid_compiled /opt/venv /opt/venv


#--- base -> python -> trytond -> WEBGUI --------------------------------------

FROM webapi AS webgui


#--- base -> python -> DOCUMENTATION ------------------------------------------

FROM compile AS documentation
COPY --from=trytond_compiled /opt/venv /opt/venv
COPY --from=pyramid_compiled /opt/venv /opt/venv
COPY --from=proteus_compiled /opt/venv /opt/venv
COPY --from=echoprint_compiled /opt/venv /opt/venv
