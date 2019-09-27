#!/bin/bash

echo "====================================================================="
echo "====================================================================="
echo "= this script stops, destroys, rebuilds, restarts the c3s.ado setup ="
echo "====================================================================="
echo `date +%Y-%m-%d:%H:%M:%S`

# stop docker containers
echo -e "\n== stop docker containers"
docker-compose stop

# update repositories
echo -e "\n== update repositories"
git pull          # update the main repository
./update --reset  # update all other repos

# build docker container
echo -e "\n== build docker container"
docker-compose build

# recreate test database
echo -e "\n== recreate test databases"
docker-compose run -rm tryton ado-do create-test-db

# run tests
echo -e "\n== run tests"
docker-compose run --rm --use-aliases -e ENVIRONMENT=testing portal ado-do run-tests
EXITCODE=$?

echo `date +%Y-%m-%d:%H:%M:%S`
echo "====================================================================="
echo "====================================================================="

exit $EXITCODE

