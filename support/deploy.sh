#!/bin/sh

REPO_ROOT="`dirname $0`/.."

cd $REPO_ROOT

if [ ! -f bin/activate ]; then
	virtualenv .
fi

. bin/activate

pip install -r requirements.txt
mkdir LakeGIS/static
python LakeGIS/manage.py collectstatic --clear --noinput
touch LakeGIS/wsgi.py

