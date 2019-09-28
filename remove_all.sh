#!/bin/bash
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker
read -p "Do you REALLY want to remove all docker containers, images, cached images and the database on this system? (Y/N) " input
if [[ $input='y' || $input = 'Y' ]]
then
    echo "Stopping docker containers, if running ..."
    current_containers="$(docker ps -a -q)"
    docker stop "${current_containers}"
    echo "removing database ... (if your user is not in sudoers, the delete postgresql-data manually via root user and execute this script again)"
    sudo rm -rf postgresql-data/
    echo "recreating empty postgresql-data directory ..."
    mkdir postgresql-data
    echo "removing docker containers ..."
    docker rm "${current_containers}"
    echo "removing docker images ..."
    docker rmi "$(docker images -f 'dangling=true' -q)"
    echo "removing all locally cached docker images ... (in case of error, try docker rmi with -f)"
    docker rmi "$(docker images -q)"
elif [[ $input='n' || $input='N' ]]
then
    exit
else
    echo "Invaild Option"
    exit
fi
