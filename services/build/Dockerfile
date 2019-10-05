ARG ENVIRONMENT
ARG WORKDIR
ARG APT_CACHERURL
ARG DEBIAN
ARG DEBUGGER_WINPDB
ARG DEBUGGER_PTVSD


#==============================================================================
# Base Images (Jessie)
#==============================================================================

#--- BASE ---------------------------------------------------------------------

### production
FROM debian:jessie-slim AS jessie_base_production
# set workdir
ARG WORKDIR
ENV WORKDIR $WORKDIR
ENV PATH $PATH:$WORKDIR
RUN mkdir -p $WORKDIR
WORKDIR $WORKDIR
# configure apt
ENV DEBIAN_FRONTEND noninteractive
ARG APT_CACHERURL
RUN if [ ${APT_CACHERURL} ]; then \
        echo "Acquire::HTTP::Proxy ${APT_CACHERURL};" >> /etc/apt/apt.conf.d/01proxy \
        && echo 'Acquire::HTTPS::Proxy "false";' >> /etc/apt/apt.conf.d/01proxy; \
    fi
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

### testing
FROM jessie_base_production AS jessie_base_testing

### development
FROM jessie_base_testing AS jessie_base_development
# install development packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    && apt-get install -y --no-install-recommends \
        git \
        htop \
        iputils-ping \
        net-tools \
        vim \
    && rm -rf /var/lib/apt/lists/*

### result
FROM jessie_base_${ENVIRONMENT} AS jessie_base


#--- base -> PYTHON -----------------------------------------------------------

### production
FROM jessie_base AS jessie_python_production
# install python
ENV PYTHONUNBUFFERED 1
RUN apt-get update && apt-get install -y --no-install-recommends \
    && apt-get install -y --no-install-recommends \
        curl \
        python \
    && rm -rf /var/lib/apt/lists/*
# install pip
RUN curl -s https://bootstrap.pypa.io/get-pip.py | python
# create virtual environment
RUN pip install virtualenv
RUN python -m virtualenv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
ENV VIRTUAL_ENV=/opt/venv

### testing
FROM jessie_python_production AS jessie_python_testing

### development
FROM jessie_python_testing AS jessie_python_development

### result
FROM jessie_python_${ENVIRONMENT} AS jessie_python


#--- base -> python -> TRYTOND ------------------------------------------------

### production
FROM jessie_python AS jessie_trytond_production
# install database packages
RUN for i in $(seq 1 8); do mkdir -p "/usr/share/man/man${i}"; done \
    && apt-get update && apt-get install -y --no-install-recommends \
        postgresql-client-9.4  \
        sqlite3 \
        libxslt1.1 \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /usr/share/man/*

### testing
FROM jessie_trytond_production AS jessie_trytond_testing

### development
FROM jessie_trytond_testing AS jessie_trytond_development

### result
FROM jessie_trytond_${ENVIRONMENT} AS jessie_trytond


#--- base -> python -> WORKER -------------------------------------------------

### production
FROM jessie_python AS jessie_worker_production
RUN apt-get update && apt-get install -y --no-install-recommends \
        cron \
        libav-tools \
        libtag1-vanilla \
    && rm -rf /var/lib/apt/lists/*
RUN ln -s /usr/bin/avconv /usr/local/bin/ffmpeg

### testing
FROM jessie_worker_production AS jessie_worker_testing

### development
FROM jessie_worker_testing AS jessie_worker_development

### result
FROM jessie_worker_${ENVIRONMENT} AS jessie_worker


#--- base -> python -> COMPILE ------------------------------------------------

FROM jessie_python AS jessie_compile
# install libs
RUN apt-get update && apt-get install -y --no-install-recommends \
    && apt-get install -y --no-install-recommends \
        build-essential \
        git \
        python-dev \
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
    && rm -rf /var/lib/apt/lists/*


#==============================================================================
# Compilation Images
#==============================================================================

#--- [COMPILE] PYTHON ---------------------------------------------------------

### production
FROM jessie_compile AS jessie_python_production_compiled
RUN pip install \
    click==4.0

### testing
FROM jessie_python_production_compiled AS jessie_python_testing_compiled
RUN pip install \
    coverage==4.5.1 \
    click==4.0 \
    nose==1.3.7 \
    nose2==0.9.1 \
    pytest==4.6.5 \
    tox==3.14.0

### development
FROM jessie_python_testing_compiled AS jessie_python_development_compiled
RUN pip install \
    pdbpp==0.9.2 \
    ptvsd==4.2.10 \
    sphinx==1.8.5
RUN if [ ${DEBUGGER_PTVSD} ]; then pip install \
        ptvsd==4.2.10; \
    fi
RUN if [ ${DEBUGGER_WINPDB} ]; then pip install \
        winpdb==1.4.8; \
    fi

### result
FROM jessie_python_${ENVIRONMENT}_compiled AS jessie_python_compiled


#--- [COMPILE] python -> TRYTOND ----------------------------------------------

### production
FROM jessie_python_compiled AS jessie_trytond_production_compiled
# trytond mandatory
RUN pip install \
    lxml==3.4.0 \
    polib==1.0.5 \
    python-dateutil==2.2 \
    python-sql==0.4 \
    relatorio==0.6.1
# trytond optional
RUN pip install \
    "proteus<3.5.0" \
    interlude==1.3.1 \
    mock==1.0.1 \
    py-bcrypt==0.4 \
    psycopg2==2.5.4 \
    pydot==1.4.1 \
    python-Levenshtein==0.11.2 \
    PyWebDAV==0.9.8 \
    simplejson==3.6.5
# additional
RUN pip install \
    hurry.filesize==0.9 \
    pyOpenSSL==17.5.0 \
    pytz==2015.7 \
    vatnumber==1.2

### testing
FROM jessie_trytond_production_compiled AS jessie_trytond_testing_compiled

### development
FROM jessie_trytond_testing_compiled AS jessie_trytond_development_compiled

### result
FROM jessie_trytond_${ENVIRONMENT}_compiled AS jessie_trytond_compiled


#--- [COMPILE] python -> trytond -> PYRAMID -----------------------------------

### production
FROM jessie_trytond_compiled AS jessie_pyramid_production_compiled
RUN pip install \
    colander==1.4 \
    cornice==3.4.0 \
    cornice-swagger==0.7.0 \
    cryptacular==1.4.1 \
    Pillow==6.0.0 \
    deform==2.0.5 \
        # 29.5.18: requirement of deform 2.0.5 not handled automaticly
        "iso8601<0.1.12" \
    pyramid==1.9.2 \
    pyramid-beaker==0.8 \
    pyramid-chameleon==0.3 \
    pyramid-mailer==0.15.1 \
    python-magic==0.4.15 \
    raven==6.10.0 \
    requests==2.18.4 \
    waitress==1.1.0

### testing
FROM jessie_pyramid_production_compiled AS jessie_pyramid_testing_compiled
RUN pip install \
    selenium==3.12.0 \
    WebTest==2.0.29

### development
FROM jessie_pyramid_testing_compiled AS jessie_pyramid_development_compiled
RUN pip install \
    pyramid-debugtoolbar==4.4

### result
FROM jessie_pyramid_${ENVIRONMENT}_compiled AS jessie_pyramid_compiled


#--- [COMPILE] python -> WORKER -----------------------------------------------

### production
FROM jessie_python_compiled AS jessie_worker_production_compiled
# compile echoprint-codegen
RUN git clone https://github.com/spotify/echoprint-codegen.git /opt/echoprint-codegen \
    && git -C /opt/echoprint-codegen checkout v4.12 \
    && make -C /opt/echoprint-codegen/src \
    && chmod 755 /opt/echoprint-codegen/echoprint-codegen
# install pip packages
RUN pip install  \
    "proteus<3.5.0" \
    pyechonest==9.0.0  \
    pydub==0.18.0  \
    pytaglib==1.4.1  \
    requests==2.9.1

### testing
FROM jessie_worker_production_compiled AS jessie_worker_testing_compiled

### development
FROM jessie_worker_testing_compiled AS jessie_worker_development_compiled

### result
FROM jessie_worker_${ENVIRONMENT}_compiled AS jessie_worker_compiled


#==============================================================================
# Service Images
#==============================================================================

#--- DATABASE -----------------------------------------------------------------

FROM postgres:9.4 AS database


#--- WEBSERVER ----------------------------------------------------------------

FROM jwilder/nginx-proxy AS webserver
RUN { \
      echo 'client_max_body_size 100m;'; \
      echo 'error_log off;'; \
    } > /etc/nginx/conf.d/my_proxy.conf


#--- BROWSER ------------------------------------------------------------------

FROM selenium/standalone-firefox AS browser


#--- base -> python -> WORKER -------------------------------------------------

FROM ${DEBIAN}_worker AS worker
COPY --from=jessie_worker_compiled /opt/echoprint-codegen/echoprint-codegen /usr/local/bin/echoprint-codegen
COPY --from=jessie_worker_compiled /opt/venv /opt/venv
COPY worker.cron /etc/cron.d/worker


#--- base -> python -> trytond -> ERPSERVER -----------------------------------

FROM ${DEBIAN}_trytond AS erpserver
COPY --from=jessie_trytond_compiled /opt/venv /opt/venv


#--- base -> python -> trytond -> WEBAPI --------------------------------------

FROM ${DEBIAN}_trytond AS webapi
COPY --from=jessie_pyramid_compiled /opt/venv /opt/venv


#--- base -> python -> trytond -> WEBGUI --------------------------------------

FROM webapi AS webgui

