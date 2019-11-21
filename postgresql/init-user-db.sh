#!/bin/sh

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE USER snmpuser;
    CREATE DATABASE snmpdb;
    GRANT ALL PRIVILEGES ON DATABASE snmpdb TO snmpuser;
EOSQL
