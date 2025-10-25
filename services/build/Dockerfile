ARG ENVIRONMENT=production
ARG WORKDIR
ARG DEBUGGER_WINPDB
ARG DEBUGGER_DEBUGPY


#==============================================================================
# Base Images (Debian)
#==============================================================================

#--- BASE ---------------------------------------------------------------------

### production
FROM debian:trixie-slim AS base_production
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
        curl \
        python3 \
        python3-pip \
        python3-venv \
    && rm -rf /var/lib/apt/lists/*
# create virtual environment
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
ENV VIRTUAL_ENV=/opt/venv
# upgrade essential pip packages
RUN python3 -m pip install --upgrade pip wheel setuptools
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
        postgresql-client-17 \
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
        libtag2 \
    && rm -rf /var/lib/apt/lists/*

### staging
FROM proteus_production AS proteus_staging

### testing
FROM proteus_staging AS proteus_testing
# install database packages
RUN for i in $(seq 1 8); do mkdir -p "/usr/share/man/man${i}"; done \
    && apt-get update && apt-get install -y --no-install-recommends \
        postgresql-client-17 \
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
            libtag-dev \
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
    click==8.3.0

### staging
FROM python_production_compiled AS python_staging_compiled

### testing
FROM python_staging_compiled AS python_testing_compiled
RUN pip install \
    autoapi==2.0.1 \
    coverage==7.10.7 \
    flake8==7.3.0 \
    mypy==1.18.2 \
    pytest==8.4.2 \
    pytest-cov==7.0.0 \
    pytest-mock==3.15.1 \
    types-python-dateutil==2.9.0.20251008 \
    types-requests==2.32.4.20250913 \
    Sphinx==8.2.3 \
    sphinx-rtd-theme==3.0.2 \
    sphinxcontrib-plantuml \
    tox==4.31.0

### development
FROM python_testing_compiled AS python_development_compiled
RUN pip install \
    pdbpp==0.11.7

ARG DEBUGGER_DEBUGPY
RUN if [ ${DEBUGGER_DEBUGPY} -ne 0 ]; then pip install \
        debugpy==1.8.17; \
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
RUN wget https://files.c3s.cc/tokyocabinet-1.4.48.tar.gz
RUN tar xvf tokyocabinet-1.4.48.tar.gz
RUN mkdir /opt/tokyocabinet/
RUN cd tokyocabinet-1.4.48 && ./configure --prefix=/opt/tokyocabinet/ && make && make install

# install tokyo tyrant
RUN wget https://files.c3s.cc/tokyotyrant-1.1.41.tar.gz
RUN tar xvf tokyotyrant-1.1.41.tar.gz
RUN mkdir /opt/tokyotyrant
RUN cd tokyotyrant-1.1.41 && ./configure --prefix=/opt/tokyotyrant/ --with-tc=/opt/tokyocabinet && make && make install

# install python packages
# https://github.com/webpy/webpy/issues/813 \
RUN pip install legacy-cgi==2.6.3
RUN pip install --no-build-isolation \
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
    defusedxml==0.7.1 \
    Genshi==0.7.9 \
    lxml==6.0.2 \
    passlib[bcrypt]==1.7.4 \
    polib==1.2.0 \
    python-dateutil==2.9.0.post0 \
    python-sql==1.6.0 \
    relatorio[fodt]==0.11.1 \
    Werkzeug==3.1.3
# trytond optional
RUN pip install \
    gevent==25.9.1 \
    html2text==2025.4.15 \
    pillow==11.3.0 \
    psycopg2==2.9.11 \
    pydot==4.0.1 \
    python-Levenshtein==0.27.1 \
    weasyprint==66.0
# trytond account
RUN pip install \
    simpleeval==1.0.3
# trytond bank, party, product
RUN pip install \
    python-stdnum==2.1
# trytond currency
RUN pip install \
    forex-python==1.9.2 \
    pycountry==24.6.1
# additional
RUN pip install \
    hurry.filesize==0.9 \
    interlude==1.3.1 \
    mock==5.2.0 \
    pyOpenSSL==25.3.0 \
    pytz==2025.2 \
    requests==2.32.5

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
    cornice==6.1.0 \
    cornice-swagger==1.0.1 \
    cryptacular==1.6.2 \
    pillow==11.3.0 \
    deform==2.0.15 \
    pyramid==2.0.2 \
    pyramid-beaker==0.8 \
    pyramid-chameleon==0.3 \
    pyramid-mailer==0.15.1 \
    python-magic==0.4.27 \
    waitress==3.0.2

### staging
FROM pyramid_production_compiled AS pyramid_staging_compiled

### testing
FROM pyramid_staging_compiled AS pyramid_testing_compiled
RUN pip install \
    raven==6.10.0 \
    selenium==4.36.0 \
    WebTest==3.0.7

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
    # https://github.com/jiaaro/pydub/issues/815 \
        audioop-lts==0.2.2 \
    pytaglib==3.0.1 \
    python-dateutil==2.9.0.post0 \
    requests==2.32.5

### staging
FROM proteus_production_compiled AS proteus_staging_compiled

### testing
FROM proteus_staging_compiled AS proteus_testing_compiled

### development
FROM proteus_testing_compiled AS proteus_development_compiled

### result
FROM proteus_${ENVIRONMENT}_compiled AS proteus_compiled


#--- [COMPILE] SAO ------------------------------------------------------------

### production
FROM node:trixie-slim AS sao_production_compiled
RUN apt-get update && apt-get install -y --no-install-recommends \
        ca-certificates \
        git \
        wget \
    && rm -rf /var/lib/apt/lists/*
ARG TRYTON_VERSION
# RUN git clone -b ${TRYTON_VERSION} --single-branch https://github.com/tryton/sao.git /opt/sao \
#     && chown -R node:node /opt/sao
RUN wget https://downloads.tryton.org/${TRYTON_VERSION}/tryton-sao-last.tgz \
    && tar -zxf tryton-sao-last.tgz \
    && mv package /opt/sao \
    && chown -R node:node /opt/sao
USER node
RUN cd /opt/sao \
    && npm install --legacy-peer-deps \
    && node_modules/.bin/grunt dev
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


#--- [COMPILE] python -> DOCUMENTATION ----------------------------------------

### production
FROM python_compiled AS documentation_compiled

# install libs
RUN apt-get update && apt-get install -y --no-install-recommends \
        default-jdk-headless \
        graphviz \
    && rm -rf /var/lib/apt/lists/*
RUN curl -L 'http://downloads.sourceforge.net/project/plantuml/plantuml.jar' \
      -o /opt/plantuml.jar


#==============================================================================
# Service Images
#==============================================================================

#--- DATABASE -----------------------------------------------------------------

FROM postgres:17 AS database


#--- WEBSERVER ----------------------------------------------------------------

FROM jwilder/nginx-proxy:1.8.0 AS webserver


#--- BROWSER ------------------------------------------------------------------

FROM selenium/standalone-firefox:4.36.0 AS browser


#--- base -> python -> echoprint -> FINGERPRINT -------------------------------

FROM echoprint AS fingerprint
COPY --from=echoprint_compiled /opt/tokyocabinet/bin/* /bin/
COPY --from=echoprint_compiled /opt/tokyocabinet/lib/libtokyocabinet.* /lib/
COPY --from=echoprint_compiled /opt/tokyotyrant/bin/* /bin/
COPY --from=echoprint_compiled /opt/tokyotyrant/lib/libtokyotyrant.* /lib/
COPY --from=echoprint_compiled /opt/tokyotyrant/lib/ttskel* /lib/
COPY --from=echoprint_compiled /opt/venv /opt/venv

#--- base -> python -> audioneex -> FINGERPRINT-AUDIONEEX ---------------------

FROM python_compiled AS fingerprint-audioneex

### runtime
RUN for i in $(seq 1 8); do mkdir -p "/usr/share/man/man${i}"; done \
    && apt-get update && apt-get install -y --no-install-recommends \
        ffmpeg \
        libtag2 \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /usr/share/man/*

### compile
RUN for i in $(seq 1 8); do mkdir -p "/usr/share/man/man${i}"; done \
    && apt-get update && apt-get install -y --no-install-recommends \
        cmake \
        file \
        libboost-dev \
        libboost-filesystem-dev \
        libboost-system-dev \
        libboost-thread-dev \
        libboost-regex-dev \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /usr/share/man/*
# fftss
RUN version="3.0-20071031" \
    && wget https://www.ssisc.org/fftss/dl/fftss-${version}.tar.gz \
    && tar xvf fftss-*.tar.gz \
    && cd fftss-* \
    # error: implicit declaration of function \
        && > libfftss/fftss_fortran.c \
    && ./configure CFLAGS=-fPIC \
                   --prefix=/opt/fftss \
                   --includedir=/opt/fftss/include/fftss \
    && make \
    && make install
# tokyocabinet
RUN version="1.4.48" \
    && wget https://files.c3s.cc/tokyocabinet-${version}.tar.gz \
    && tar xvf tokyocabinet-*.tar.gz \
    && cd tokyocabinet-* \
    && ./configure --disable-zlib \
                   --disable-bzip \
                   --prefix=/opt/tokyocabinet \
                   --includedir=/opt/tokyocabinet/include/tcabinet \
    && make \
    && make install
# audioneex
RUN version="v1.3.2" \
    && wget https://github.com/a-gram/audioneex/archive/refs/tags/${version}.tar.gz \
    && tar xvf ${version}.tar.gz \
    && cd audioneex-* \
    && sed -i "s|set(MY_INCLUDE_DIRS|set(MY_INCLUDE_DIRS\n\
                 /opt/fftss/include\n\
                 /opt/fftss/include/fftss\n\
                 /opt/tokyocabinet/include\n\
                 /opt/tokyocabinet/include/tcabinet\n|"\
           CMakeLists.txt \
    && sed -i "s|set(MY_LIBRARY_x64_RELEASE_DIRS|set(MY_LIBRARY_x64_RELEASE_DIRS\n\
                 /opt/fftss/lib\n\
                 /opt/tokyocabinet/lib\n|" \
           CMakeLists.txt \
    && ./build WITH_EXAMPLES=ON WITH_ID3=ON  # WITH_TESTS=ON

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

FROM documentation_compiled AS documentation
COPY --from=trytond_compiled /opt/venv /opt/venv
COPY --from=pyramid_compiled /opt/venv /opt/venv
COPY --from=proteus_compiled /opt/venv /opt/venv
COPY --from=echoprint_compiled /opt/venv /opt/venv
