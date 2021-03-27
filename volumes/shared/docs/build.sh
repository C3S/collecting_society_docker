#!/bin/bash
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker
#
#% Usage: ./docs-build [--no-autoapi] [--help]
#%
#%   This script builds the documentation with sphinx.
#%
#% Options:
#%   --no-autoapi: don't parse the modules
#%   --help: display this help

# print usage
usage() {
  [ "$*" ] && echo "$0: $*"
  sed -n '/^#%/,/^$/s/^#% \{0,1\}//p' "$0"
  exit 2
} 2>/dev/null

# get options
NOAUTOAPI=false
for i in "$@"; do
    if [ $i = "--no-autoapi" ]; then NOAUTOAPI=true; continue; fi
    if [ $i = "--help" ]; then usage 2>&1; fi
done

# generate apidoc
if ! $NOAUTOAPI; then
    # delete files
    rm -rf build/doctrees
    rm -rf build/html
    rm -rf source/generated
    mkdir -p source/collecting_society
    # parse code
    sphinx-apidoc -f -o source/generated --no-toc ../src/collecting_society
    sphinx-apidoc -f -o source/generated --no-toc ../src/collecting_society_web
    sphinx-apidoc -f -o source/generated --no-toc ../src/collecting_society_worker
    sphinx-apidoc -f -o source/generated --no-toc ../src/portal_web
fi

# link readmes
ln -sf /collecting_society_docker/README.rst source/generated/collecting_society_docker_README.rst
ln -sf /shared/src/collecting_society_web/README.rst source/generated/collecting_society_web_README.rst
ln -sf /shared/src/collecting_society/README.rst source/collecting_society/README.rst
ln -sf /shared/src/collecting_society/INSTALL.rst source/collecting_society/INSTALL.rst
ln -sf /shared/src/collecting_society/CHANGELOG.rst source/collecting_society/CHANGELOG.rst
ln -sf /shared/src/collecting_society/COPYRIGHT.rst source/collecting_society/COPYRIGHT.rst
ln -sf /shared/src/portal_web/README.rst source/generated/portal_web_README.rst

# add warnings
WARNING_MESSAGE="Files in this folder will be overwritten by the build.sh script"
WARNING_FILENAME="WARNING_DO_NOT_CHANGE_FILES_HERE"
echo $WARNING_MESSAGE >> source/generated/$WARNING_FILENAME
echo $WARNING_MESSAGE >> source/collecting_society/$WARNING_FILENAME

# make html
make html

