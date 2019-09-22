#!/bin/bash

echo "====================================================================="
echo "====================================================================="
echo "= this script stops, destroys, rebuilds, restarts the c3s.ado setup ="
echo "====================================================================="
echo `date +%Y-%m-%d:%H:%M:%S`

# stop docker containers
echo -e "\n== stop docker containers"
docker-compose stop

# delete database c3s
echo -e "\n== delete test databases"
docker-compose run portal ado-do db-delete test
docker-compose run portal ado-do db-delete test_template

# update repositories
echo -e "\n== update repositories"
git pull          # update the main repository
./update --reset  # update all other repos

# build docker container
echo -e "\n== build docker container"
docker-compose build

# run tests !
echo -e "\n== run tests"
docker-compose run --rm --use-aliases -e ENVIRONMENT=testing portal ado-do run-tests
EXITCODE=$?

echo `date +%Y-%m-%d:%H:%M:%S`
echo "====================================================================="
echo "====================================================================="

exit $EXITCODE

