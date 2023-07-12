#!/bin/bash

if [ "$1" = "" ]; then
    echo "Usage: release.sh major/minor/patch... (see hatch version --help for details)"
    exit 1
fi

# Bump version with hatchling
case $1 in 

    "fix")
        hatch version fix
        ;;

    "minor")
        hatch version minor
        ;;

    "major")
        hatch version major
        ;;

    *)
        hatch version $1
esac

# Get version number
HATCH_VERSION=`hatch version`
RELEASE_VERSION="v${HATCH_VERSION}"

# Confirm it actually builds
rm -r dist
python3 -m build

# Commit version bump
git add src/idealforms/__about__.py
git commit -m "bump version to $RELEASE_VERSION"

# Tag in Git
git tag $RELEASE_VERSION -m "release $RELEASE_VERSION"

# Push tag and version bump
git push --atomic origin main $RELEASE_VERSION