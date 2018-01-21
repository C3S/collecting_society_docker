#!/bin/bash

echo "====================================================================="
echo "====================================================================="
echo "= this script stops, destroys, rebuilds, restarts the c3s.ado setup ="
echo "====================================================================="
echo `date +%Y-%m-%d:%H:%M:%S`

# echo pwd

# if things were running already...
# stop docker containers
echo -e "\n== stop docker containers"
docker-compose stop

# delete database c3s
echo -e "\n== delete database"
docker-compose run portal ado-do db-delete c3s
echo $?
echo "0 means success, 1 and above mean failure!"

# delete database test
echo -e "\n== delete database"
docker-compose run portal ado-do db-delete test
echo $?
echo "0 means success, 1 and above mean failure!"

# delete database test
echo -e "\n== delete database"
docker-compose run portal ado-do db-delete test_template
echo $?
echo "0 means success, 1 and above mean failure!"



git pull # update the main repository
./update # update all other repos


# delete everything...

# re-create database
#echo -e "\n== re-create database"
#docker-compose run tryton ado-do db-demo-setup c3s &> /dev/null
#echo $?
#echo "0 means success, 1 and above mean failure!"

docker-compose build

# docker-compose build --no-cache  ## for full builds

# start docker containers
#echo -e "\n== start docker containers"
#docker-compose up -d

# run tests !
#Run all tests for portal + plugins::

docker-compose run portal ado-do run-tests

# stop docker containers
echo -e "\n== stop docker containers"
docker-compose stop


echo `date +%Y-%m-%d:%H:%M:%S`
echo "====================================================================="
echo "====================================================================="
