#!/bin/bash

# sleep 3s

#-h localhost
psql -v ON_ERROR_STOP=1 -U "postgres"  <<-EOSQL
    CREATE USER flask_orm with password 'flask_orm';    
    CREATE DATABASE flask_orm;
    GRANT ALL PRIVILEGES ON DATABASE flask_orm TO flask_orm;
EOSQL