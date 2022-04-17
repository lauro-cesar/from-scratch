#!/bin/bash

timeout=0
isReady=0


mkdir -p  /home/django_project/datastore/main
mkdir -p /opt/datastore/main/
export DATABASE_ENGINE=django.contrib.gis.db.backends.postgis

if [ -z ${DATABASE_PORT} ] ; then
    until nc -z ${DATABASE_HOST} ${DATABASE_PORT}; do
    echo "$(date) - waiting for database"
    sleep 5
done
fi



echo "Starting Django"
python manage.py makemigrations accounts --noinput
python manage.py makemigrations --noinput

python manage.py migrate --noinput
python manage.py collectstatic --noinput





if test -f "initial_data/initial_data.json"; then
    python manage.py loaddata initial_data/initial_data.json --ignorenonexistent
fi



screen -wipe

screen -dmS websocket daphne -b 0.0.0.0 -p 8002 --proxy-headers  project.asgi:application
screen -dmS queue celery -b redis://$REDIS_HOST:$REDIS_PORT/$REDIS_DB -A project worker -B -E -Q $REDIS_QUEUE_NAME


screen -dmS django gunicorn project.wsgi:application --bind 0.0.0.0:8001 --proxy-protocol --strip-header-spaces --graceful-timeout=900 --timeout=900

echo "Django Started"
tail -f /var/log/lastlog
exec "$@"
