#!/bin/bash

# Set the date format, filename and the directories where your backup files will be placed and which directory will be archived.
NOW=$(date +"%Y-%m-%d")

# Set the MySQL username and password
DB_USER="root"
DB_PASS="password"

# Set the MySQL host
DB_HOST="localhost"

# Set the MySQL databases
DB_NAMES="database1 database2"

# Set the backup directory
BACKUP_DIR="./backup"

# Set the MySQL backup filename
MYSQL_BACKUP_FILENAME="mysql-$NOW.sql"

# tables 
# TABLES="table1 table2"

# use mysqldump to backup the databases to a file
# mysqldump -u $DB_USER -h $DB_HOST -p$DB_PASS --databases $DB_NAMES --tables $TABLES > $BACKUP_DIR/$MYSQL_BACKUP_FILENAME

# sqlite dump 
sqlite3 backend/db.sqlite3 .dump > $BACKUP_DIR/sqlite-$NOW.sql