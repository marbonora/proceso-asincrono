#!/bin/sh

echo 'Installing...'
cd /app/server
python -u -m install

echo 'Configuring nginx...'
cat /app/docker/nginx.conf \
 > /etc/nginx/sites-enabled/default

echo 'Starting nginx...'
nginx -g 'daemon on;'

echo 'Configuring supervisor...'
echo "- SERVER_WORKERS: ${SERVER_WORKERS}"
echo "- SERVER_THREADS: ${SERVER_THREADS}"
cat /app/docker/supervisord.conf \
 | sed "s|SERVER_WORKERS|${SERVER_WORKERS}|g" \
 | sed "s|SERVER_THREADS|${SERVER_THREADS}|g" \
 | sed "s|EMAIL_ACCOUNT|${EMAIL_ACCOUNT}|g" \
 > /etc/supervisord.conf

echo 'Starting supervisor...'
supervisord -c /etc/supervisord.conf