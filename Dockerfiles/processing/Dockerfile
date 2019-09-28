# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/c3s.ado.repertoire

FROM c3s_repertoire_tryton
MAINTAINER Udo Spallek <udono@virtual-things.biz>

RUN apt-get update && apt-get install -y --no-install-recommends  \
    cron \
    libtag1-dev \
    libav-tools \
    git \
    libboost-dev \
    zlib1g-dev

WORKDIR /shared

RUN pip install  \
    pyechonest==9.0.0  \
    pydub==0.18.0  \
    pytaglib==1.4.1  \
    requests==2.9.1 \
    ptvsd

# ffmpeg symlink to avconv
RUN ln -s /usr/bin/avconv /usr/local/bin/ffmpeg

# echoprint
WORKDIR /opt
RUN git clone https://github.com/spotify/echoprint-codegen.git
WORKDIR /opt/echoprint-codegen
RUN git checkout v4.12
WORKDIR /opt/echoprint-codegen/src
RUN make
WORKDIR /opt/echoprint-codegen
RUN chmod 755 echoprint-codegen
RUN ln -s /opt/echoprint-codegen/echoprint-codegen /usr/local/bin/echoprint-codegen
WORKDIR /shared

RUN mkdir /shared/tmp
RUN echo "" > /shared/tmp/repro.log
RUN echo "* * * * * cd /shared/src/c3sRepertoireProcessing; /usr/bin/python repro.py all 2>> /shared/tmp/repro.log >> /shared/tmp/repro.log" | crontab -
RUN crontab -u root -l

# winpdb debugger requires processing port "51000:51000" in docker-compose.yml
# to allow winpdb to attach to a pyton script, uncomment the RUN and insert this line in the script where you want to debug:
# import rpdb2; rpdb2.start_embedded_debugger("supersecret", fAllowRemote = True)
#RUN apt-get update && apt-get install -y winpdb 