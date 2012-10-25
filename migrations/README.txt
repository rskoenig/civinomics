SQL MIGRATION SCRIPTS
########################

These migration scripts do NOT need to be ran on new installs.

These are the sql scripts I used to 'upgrade' existing production Pylowiki deployments to support new schemas.


001.sql - Alter user and comment tables for disabled support
===================================================================

ALTER TABLE user ADD disabled BOOLEAN;
ALTER TABLE comment ADD disabled BOOLEAN;

sqlite
--------

sqlite3 [database].db < migrations/001.sql

mysql
--------

mysql [database] < migrations/001.sql


