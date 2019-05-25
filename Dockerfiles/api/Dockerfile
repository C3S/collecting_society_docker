# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/c3s.ado.repertoire

FROM c3s_repertoire_tryton
MAINTAINER Udo Spallek <udono@virtual-things.biz>

RUN apt-get install -y --no-install-recommends  \
    libtag1-dev

WORKDIR /ado

RUN pip install  \
    colander==1.4  \
    cornice==3.4.0  \
    coverage==4.5.1  \
    cryptacular==1.4.1  \
    deform==2.0.5  \
        # 29.5.18: requirement of deform 2.0.5 not handled automaticly
        "iso8601<0.1.12"  \
    nose==1.3.7  \
    pyechonest==9.0.0  \
    pydub==0.22.0  \
    pyramid==1.9.2 \
    pyramid-beaker==0.8  \
    pyramid-chameleon==0.3  \
    pyramid-debugtoolbar==4.4  \
    pyramid-mailer==0.15.1  \
    pyramid-oauth2-provider==0.2  \
    python-magic==0.4.15  \
    pytaglib==1.4.3  \
    requests==2.18.4  \
    selenium==3.12.0  \
    WebTest==2.0.29  \
    waitress==1.1.0 \
    Pillow==6.0.0 \
    ptvsd==4.2.10
    
# winpdb debugger requires either portal or api to have an open port 51000 
# (add "51000:51000" in docker-compose.yml -- make sure you open it only in
# a single container at a given time)
# to allow winpdb to attach to a pyton script, uncomment the RUN command below
# and insert this line in the script where you want to debug:
# import rpdb2; rpdb2.start_embedded_debugger("supersecret", fAllowRemote = True)
#RUN apt-get update && apt-get install -y winpdb 

