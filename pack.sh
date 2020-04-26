#!/usr/bin/env bash
echo "start pack vcode-spider..."
tag= git describe --tags ` git rev-list --tags --max-count=1`
echo "get the newest git tag: ${tag}"

echo "start build docker..."
docker build --tag vcode-spider:"${tag}" -f ./Dockerfile

echo "pack vcode-spider docker image success..."
