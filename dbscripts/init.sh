#!/bin/sh
# Скрипт для создания БД для LakeGIS

DEFAULT_DB_NAME=lakegis
DEFAULT_DB_LOGIN=lakegis
DEFAULT_DB_LOGIN_PASSWORD=NULL

DEFAULT_TEMPLATE_DB_NAME=template_postgis

DEFAULT_DB_SUPERUSER=postgres

DB_NAME=${DB_NAME:=$DEFAULT_DB_NAME}
DB_LOGIN=${DB_LOGIN:=$DEFAULT_DB_LOGIN}
DB_LOGIN_PASSWORD=${DB_LOGIN_PASSWORD:=$DEFAULT_DB_LOGIN_PASSWORD}
TEMPLATE_DB_NAME=${TEMPLATE_DB_NAME:=$DEFAULT_TEMPLATE_DB_NAME}
DB_SUPERUSER=${DB_SUPERUSER:=$DEFAULT_DB_SUPERUSER}

cd `dirname $0`

echo "Script will create database \"$DB_NAME\" from template \"$TEMPLATE_DB_NAME\"."
echo "Script will also create database user \"$DB_LOGIN\" with password $DB_LOGIN_PASSWORD. This user will be given full access to created database."
echo "Will use \"$DB_SUPERUSER\" as database superuser. Depending on your PostgreSQL configuration, you may be asked to enter password."
echo

psql -U $DB_SUPERUSER -d postgres -v "DB_NAME=$DB_NAME" -v"DB_LOGIN=$DB_LOGIN" -v "DB_LOGIN_PASSWORD=$DB_LOGIN_PASSWORD" -v "TEMPLATE_DB_NAME=$TEMPLATE_DB_NAME" -f init.sql 2>/dev/null

if [ "$DB_NAME" != "$DEFAULT_DB_NAME" -o "$DB_LOGIN" != "$DEFAULT_DB_LOGIN" -o "$DB_LOGIN_PASSWORD" != "$DEFAULT_DB_LOGIN_PASSWORD" ]; then
	echo
	echo "+------------------------WARNING-------------------------+"
	echo "|  Some settings changes you have made, require custom   |"
       	echo "| django database configuration. Place following lines   |"
	echo "| to your local_settings.py (LakeGIS knows how to handle |"
	echo "| this file):                                            |"
	echo "+--------------------------------------------------------+"
	echo "DATABASES = {"
	echo "    'default': {"
	echo "        'ENGINE' : 'django.contrib.gis.db.backends.postgis',"
	echo "        'NAME' : '$DB_NAME',"
	echo "        'USER' : '$DB_LOGIN',"
	if [ "$DB_LOGIN_PASSWORD" != "$DEFAULT_DB_LOGIN_PASSWORD" ]; then
		echo "        'PASSWORD' : $DB_LOGIN_PASSWORD"
	fi
	echo "    }"
	echo "}"
fi
