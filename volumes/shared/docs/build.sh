#!/bin/bash

rm -rf build/doctrees
rm -rf build/html
rm -rf source/generated

sphinx-apidoc -f -o source/generated --tocfile index ../src/collecting_society
sphinx-apidoc -f -o source/generated --tocfile index ../src/collecting_society_web
sphinx-apidoc -f -o source/generated --tocfile index ../src/collecting_society_worker
# sphinx-apidoc -f -o source/generated --tocfile portal_web ../src/portal_web

make html

