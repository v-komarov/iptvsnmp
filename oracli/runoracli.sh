#!/bin/sh

docker run -d --name oracli \
--link postgres12:pg \
-e PG_HOST=PG \
-e PG_USER=snmpuser \
-e PG_PASSWORD=snmpuser \
-e PG_DATABASE=snmpdb \
oracli:fifth
