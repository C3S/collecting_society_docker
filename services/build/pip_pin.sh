#!/bin/bash

set -eu
buildDir="$(dirname "$(readlink -vf "$0")")"
dockerDir="$(readlink -vf "$buildDir/../..")"
dockerFile="$buildDir/Dockerfile"
pipFile="$buildDir/Dockerfile.requirements"

# Backup Dockerfile
if [ ! -f "$dockerFile.unpinned" ]; then
    cp "$dockerFile" "$dockerFile.unpinned"
fi

# Fetch new versions
cd $dockerDir
docker compose -f docker-compose.documentation.yml build documentation
docker compose -f docker-compose.documentation.yml run --rm documentation \
    bash -c 'pip freeze' > "$pipFile"
cd $buildDir

# Pin pip package versions
replacements=()
while read package; do
    name=${package%%=*}
    version=${package##*=}
    if [ "$name" = "selenium" ]; then
        continue
    fi
    replacements+=(
        "-e s/\(^\s*\)$name\(\[.*\]\)\{0,1\}>=[[:alnum:].]*/\1$name\2==$version/i"
    )
done < "$pipFile"
sed -i \
    "${replacements[@]}" \
    -e '/pip install\s*\\/,/^\s*$/ s/>=/==/' \
    "$dockerFile"

# Show diff
git diff "$dockerFile"

# Tidy up
rm "$dockerFile."{requirements,unpinned,original}
