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
    click

### staging
FROM python_production_compiled AS python_staging_compiled

### testing
FROM python_staging_compiled AS python_testing_compiled
RUN pip install \
    autoapi \
    coverage \
    flake8 \
    nose \
    nose2 \
    pytest \
    sphinx \
    sphinx_rtd_theme \
    tox

### development
FROM python_testing_compiled AS python_development_compiled
RUN pip install \
    pdbpp

ARG DEBUGGER_PTVSD
RUN if [ ${DEBUGGER_PTVSD} -ne 0 ]; then pip install \
        ptvsd; \
    fi
ARG DEBUGGER_WINPDB
RUN if [ ${DEBUGGER_WINPDB} -ne 0 ]; then pip install \
        winpdb; \
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
    web.py \
    pyechonest

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
    Genshi \
    lxml \
    passlib[bcrypt] \
    polib \
    python-dateutil \
    python-sql \
    relatorio[fodt] \
    "werkzeug<2" \
    wrapt
# trytond optional
RUN pip install \
    gevent \
    html2text \
    pillow \
    psycopg2 \
    pydot \
    python-Levenshtein \
    weasyprint
# additional
RUN pip install \
    hurry.filesize \
    interlude \
    mock \
    pyOpenSSL \
    pytz \
    requests \
    vatnumber
# trytond currency
RUN pip install \
    forex-python \
    pycountry
# trytond account
RUN pip install \
    simpleeval

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
    colander \
    cornice \
    cornice-swagger \
    cryptacular \
    Pillow \
    deform \
    pyramid \
    pyramid-beaker \
    pyramid-chameleon \
    pyramid-mailer \
    python-magic \
    waitress

### staging
FROM pyramid_production_compiled AS pyramid_staging_compiled

### testing
FROM pyramid_staging_compiled AS pyramid_testing_compiled
RUN pip install \
    raven \
    selenium \
    WebTest

### development
FROM pyramid_testing_compiled AS pyramid_development_compiled
RUN pip install \
    pyramid-debugtoolbar

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
    pyechonest \
    pydub  \
    pytaglib  \
    python-dateutil \
    requests

### staging
FROM proteus_production_compiled AS proteus_staging_compiled

### testing
FROM proteus_staging_compiled AS proteus_testing_compiled

### development
FROM proteus_testing_compiled AS proteus_development_compiled

### result
FROM proteus_${ENVIRONMENT}_compiled AS proteus_compiled


#==============================================================================
# Service Images
#==============================================================================

#--- DATABASE -----------------------------------------------------------------

FROM postgres:13 AS database


#--- WEBSERVER ----------------------------------------------------------------

FROM jwilder/nginx-proxy AS webserver


#--- BROWSER ------------------------------------------------------------------

FROM selenium/standalone-firefox AS browser


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
