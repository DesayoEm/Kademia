export PGUSER='postgres'

psql -c 'CREATE DATABASE testtrakademik'
psql testtrakademik -c  'CREATE EXTENSION IF NOT EXISTS \'uuid-ossp'\';
