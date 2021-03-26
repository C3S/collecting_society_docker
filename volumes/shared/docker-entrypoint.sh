#!/bin/sh
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker
#
# Entrypoint for docker
# For the CLI commands look at ./volumes/shared/cli

SCRIPTNAME=$(basename -- "$0")

# check, if the script is executed in a service environment
if [ -z "$PROJECT" ] || [ -z "$ENVIRONMENT" ] || [ -z "$SERVICE" ] || [ -z "$WORKDIR" ]; then
    echo "This script is intended to run within a service container."
    echo "Please do not try to execute it on the host."
    exit 1
fi

# run cli help to test for valid commands
isCommand() {
    cli "$1" --help > /dev/null 2>&1
}

# docker-compose run commands
if [ "$SCRIPTNAME" = "docker-entrypoint.sh" ]; then
    # call of run explicitly
    if [ "$1" = "cli" ]; then
        exec "$@"
    # call of a run subcommand
    elif isCommand "$1"; then
        cli "$@"
    # other commands
    else
        exec "$@"
    fi

# docker-compose exec commands
elif isCommand "$SCRIPTNAME"; then
    cli $SCRIPTNAME "$@"

# other commands
else
    exec "$@"
fi
