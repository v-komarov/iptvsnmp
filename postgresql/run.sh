#!/bin/sh

docker run -d -p 5432:5432 --name postgres12 \
postgres12:second
