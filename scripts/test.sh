#!/bin/bash
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

echo "====================================================================="
echo "====================================================================="
echo "= this script stops, updates, builds and tests the docker setup     ="
echo "====================================================================="
echo `date +%Y-%m-%d:%H:%M:%S`

# stop docker containers
echo -e "\n== stop docker containers"
docker-compose stop

# update repositories
echo -e "\n== update repositories"
git pull          # update the main repository
./update --reset  # update all other repos

# build docker containers
echo -e "\n== build docker containers"
docker-compose build

# recreate test database
echo -e "\n== recreate test database"
docker-compose run --rm tryton execute create-test-db

# run tests
echo -e "\n== run tests"
docker-compose run --rm --use-aliases -e ENVIRONMENT=testing portal execute run-tests
EXITCODE=$?

# remove docker containers
echo -e "\n== remove docker containers"
docker-compose rm -fs

echo `date +%Y-%m-%d:%H:%M:%S`
echo "====================================================================="
echo "====================================================================="

exit $EXITCODE

