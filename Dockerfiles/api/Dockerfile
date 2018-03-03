# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/c3s.ado.repertoire

FROM c3s_repertoire_tryton
MAINTAINER Udo Spallek <udono@virtual-things.biz>

RUN apt-get install -y --no-install-recommends  \
    libtag1-dev

WORKDIR /opt
RUN wget -O phantomjs.tar.bz2 https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2
RUN mkdir phantomjs
RUN tar -xf phantomjs.tar.bz2 -C phantomjs --strip-components=1
RUN ln -s /opt/phantomjs/bin/phantomjs /usr/local/bin/phantomjs
WORKDIR /ado

RUN pip install  \
    colander==1.0  \
    cornice==1.0.0  \
    coverage==3.7.1  \
    cryptacular==1.4.1  \
    deform==2.0a2  \
    nose==1.3.6  \
    pyechonest==9.0.0  \
    pydub==0.18.0  \
    pyramid==1.5.7  \
    pyramid_beaker==0.8  \
    pyramid-chameleon==0.3  \
    pyramid_debugtoolbar==2.3  \
    pyramid_mailer==0.14  \
    pyramid_oauth2_provider==0.2  \
    python-magic==0.4.12  \
    pytaglib==1.4.1  \
    webtest==2.0.18  \
    waitress==0.8.9  \
    requests==2.9.1  \
    selenium==2.53.1  \
    proteus==3.4.8  \
    click==6.7

# winpdb debugger requires either portal or api to have an open port 51000 
# (add "51000:51000" in docker-compose.yml -- make sure you open it only in
# a single container at a given time)
# to allow winpdb to attach to a pyton script, uncomment the RUN command below
# and insert this line in the script where you want to debug:
# import rpdb2; rpdb2.start_embedded_debugger("supersecret", fAllowRemote = True)
RUN apt-get update && apt-get install -y winpdb 
