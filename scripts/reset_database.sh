#!/bin/bash
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

echo "====================================================================="
echo "====================================================================="
echo "= this script stops, destroys, rebuilds, restarts the docker setup  ="
echo "====================================================================="
echo `date +%Y-%m-%d:%H:%M:%S`

# stop docker containers
echo -e "\n== stop docker containers"
docker-compose stop

# delete database
echo -e "\n== delete database"
docker-compose run portal execute db-delete c3s
echo $?
echo "0 means success, 1 and above mean failure!"

# re-create database
echo -e "\n== re-create database"
docker-compose run tryton execute db-demo-setup c3s &> /dev/null
echo $?
echo "0 means success, 1 and above mean failure!"

# start docker containers
echo -e "\n== start docker containers"
docker-compose up -d

echo `date +%Y-%m-%d:%H:%M:%S`
echo "====================================================================="
echo "====================================================================="