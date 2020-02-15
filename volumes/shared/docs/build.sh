#!/bin/bash

rm -rf build/doctrees
rm -rf build/html
rm -rf source/generated

sphinx-apidoc -f -o source/generated --no-toc ../src/collecting_society
sphinx-apidoc -f -o source/generated --no-toc ../src/collecting_society_web
sphinx-apidoc -f -o source/generated --no-toc ../src/collecting_society_worker
sphinx-apidoc -f -o source/generated --no-toc ../src/portal_web

# echo ".. title:: Collecting Society Docker Setup" > source/generated/collecting_society_docker_README.rst
cp ../ref/README.rst source/generated/collecting_society_docker_README.rst

# echo ".. title:: Collecting Society Web GUI" > source/generated/collecting_society_web_README.rst
cp ../src/collecting_society_web/README.rst source/generated/collecting_society_web_README.rst
echo "Files in this folder will be overwritten by the build.sh script" >> source/generated/WARNING_DO_NOT_CHANGE_FILES_HERE

# echo ".. title:: Collecting Society Web GUI" > source/generated/collecting_society_web_README.rst
mkdir source/collecting_society
echo "Files in this folder will be overwritten by the build.sh script" >> source/collecting_society/WARNING_DO_NOT_CHANGE_FILES_HERE
cp ../src/collecting_society/*.rst source/collecting_society

# echo ".. title:: Portal Web GUI" > source/generated/portal_web_README.rst
cp ../src/portal_web/README.rst source/generated/portal_web_README.rst

make html

