#!/bin/bash
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker
apt-get install git python curl apt-transport-https ca-certificates gnupg2 software-properties-common
apt-get install lsb-release --no-install-recommends
# install docker for debian or ubuntu
source /etc/os-release
a=$(arch)
if [ $a == "x86_64" ]; then a="amd64"; fi
echo "deb [arch=$a] https://download.docker.com/linux/$ID `lsb_release -cs` stable" > /etc/apt/sources.list.d/docker.list
curl -fsSL https://download.docker.com/linux/$ID/gpg | apt-key add -
apt-get update
apt-get install docker-ce
# install docker-compose !!!don't install from default repo, version too old!!!
curl -L https://github.com/docker/compose/releases/download/1.18.0/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
source ~/.profile
# IMPORTANT: add your user here (instead of c3s)
# usermod -a -G docker c3s
# install is optional but can be helpful
# apt-get install net-tools openssh-server vim

# then do an ./update as user (not as root!) in the c3s repository and use docker-compose with options 'build' and 'up'
