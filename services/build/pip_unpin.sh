#!/bin/bash

set -eu
scriptDir="$(dirname "$(readlink -vf "$0")")"
dockerFile="$scriptDir/Dockerfile"

# Backup Dockerfile
if [ ! -f "$dockerFile.original" ]; then
    cp "$dockerFile" "$dockerFile.original"
fi

# Unpin pip package versions
sed -i '/pip install\s*\\/,/^\s*$/ s/==/>=/' "$dockerFile"
