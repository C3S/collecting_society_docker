ARG ENVIRONMENT
ARG WORKDIR
ARG DEBUGGER_WINPDB
ARG DEBUGGER_PTVSD


#==============================================================================
# Base Images (Debian)
#==============================================================================

#--- BASE ---------------------------------------------------------------------

### production
FROM debian:bullseye-slim AS base_production
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
# upgrade pip
RUN python3 -m pip install --upgrade pip
# create virtual environment
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
ENV VIRTUAL_ENV=/opt/venv
# set default entrypoint and cmd for CLI script
ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["cli --help"]

### staging
FROM python_production AS python_staging

### testing
FROM python_staging AS python_testing

### development
FROM python_testing AS python_development

### result
FROM python_${ENVIRONMENT} AS python


#--- base -> python -> TRYTOND ------------------------------------------------

### production
FROM python AS trytond_production
# install database packages
RUN for i in $(seq 1 8); do mkdir -p "/usr/share/man/man${i}"; done \
    && apt-get update && apt-get install -y --no-install-recommends \
        postgresql-client-13  \
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
        postgresql-client-13  \
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
            libxslt-dev \
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
    click==8.0.1

### staging
FROM python_production_compiled AS python_staging_compiled

### testing
FROM python_staging_compiled AS python_testing_compiled
RUN pip install \
    autoapi==2.0.1 \
    coverage==5.5 \
    flake8==3.9.2 \
    nose==1.3.7 \
    nose2==0.10.0 \
    pytest==6.2.5 \
    sphinx==4.2.0 \
    sphinx_rtd_theme==1.0.0 \
    tox==3.24.4

### development
FROM python_testing_compiled AS python_development_compiled
RUN pip install \
    pdbpp==0.10.3

ARG DEBUGGER_PTVSD
RUN if [ ${DEBUGGER_PTVSD} -ne 0 ]; then pip install \
        ptvsd==4.3.2; \
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
    Genshi==0.7.5 \
    lxml==4.6.3 \
    passlib[bcrypt]==1.7.4 \
    polib==1.1.1 \
    python-dateutil==2.8.2 \
    python-sql==1.3.0 \
    relatorio[fodt]==0.10.0 \
    werkzeug==1.0.1 \
    wrapt==1.12.1
# trytond optional
RUN pip install \
    gevent==21.8.0 \
    html2text==2020.1.16 \
    pillow==8.3.2 \
    psycopg2==2.9.1 \
    pydot==1.4.2 \
    python-Levenshtein==0.12.2 \
    weasyprint==53.3
# additional
RUN pip install \
    hurry.filesize==0.9 \
    interlude==1.3.1 \
    mock==4.0.3 \
    pyOpenSSL==21.0.0 \
    pytz==2021.3 \
    requests==2.26.0 \
    vatnumber==1.2
# trytond currency
RUN pip install \
    forex-python==1.6 \
    pycountry==20.7.3
# trytond account
RUN pip install \
    simpleeval==0.9.10

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
    colander==1.8.3 \
    cornice==6.0.0 \
    cornice-swagger==1.0.1 \
    cryptacular==1.6.2 \
    Pillow==8.3.2 \
    deform==2.0.15 \
    pyramid==2.0 \
    pyramid-beaker==0.8 \
    pyramid-chameleon==0.3 \
    pyramid-mailer==0.15.1 \
    python-magic==0.4.24 \
    waitress==2.0.0

### staging
FROM pyramid_production_compiled AS pyramid_staging_compiled

### testing
FROM pyramid_staging_compiled AS pyramid_testing_compiled
RUN pip install \
    raven==6.10.0 \
    selenium==3.141.0 \
    WebTest==3.0.0

### development
FROM pyramid_testing_compiled AS pyramid_development_compiled
RUN pip install \
    pyramid-debugtoolbar==4.9

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
    pyechonest==9.0.0 \
    pydub==0.25.1  \
    pytaglib==1.4.6  \
    python-dateutil==2.8.2 \
    requests==2.26.0

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

FROM postgres:13 AS database


#--- WEBSERVER ----------------------------------------------------------------

FROM jwilder/nginx-proxy:0.9.3 AS webserver


#--- BROWSER ------------------------------------------------------------------

FROM selenium/standalone-firefox:3.141 AS browser


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
