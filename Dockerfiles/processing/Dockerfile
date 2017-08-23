# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/c3s.ado.repertoire

FROM c3sadorepertoire_tryton
MAINTAINER Udo Spallek <udono@virtual-things.biz>

RUN apt-get install -y --no-install-recommends  \
    cron \
    libtag1-dev

WORKDIR /ado

RUN pip install  \
    pyechonest==9.0.0  \
    pydub==0.18.0  \
    pytaglib==1.4.1  \
    proteus==3.4.8  \
    requests==2.9.1  \
    click==6.7

# ffmpeg installation
RUN wget https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-64bit-static.tar.xz
RUN tar --wildcards --extract --file=ffmpeg-release-64bit-static.tar.xz ffmpeg-*.*.*-64bit-static/ffmpeg
RUN mv ffmpeg-*.*.*-64bit-static/ffmpeg /usr/bin
RUN rmdir ffmpeg-*.*.*-64bit-static
RUN rm ffmpeg-release-64bit-static.tar.xz

# echoprint-codegen installation --> should be done outside the container...
#                                    for the time being, make echoprint-codegen manually!
#RUN apt-get install -y libboost-dev
#RUN apt-get install -y zlib1g-dev
#RUN apt-get install -y libtag1-dev <-- already installed in line 7
#RUN cd /ado; cd /ado/src; cd /ado/src/echoprint-codegen; cd /ado/src/echoprint-codegen/src; /usr/bin/make <-- Makefile not found here :-/
#

RUN mkdir /ado/tmp
RUN echo "" > /ado/tmp/repro.log

RUN echo "* * * * * cd /ado/src/c3sRepertoireProcessing; /usr/bin/python repro.py all 2>> /ado/tmp/repro.log >> /ado/tmp/repro.log" | crontab -
RUN crontab -u root -l