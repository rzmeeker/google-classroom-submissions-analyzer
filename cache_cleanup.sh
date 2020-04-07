#!/usr/bin/env bash

systemctl stop app
rm -rf /var/www/gcs/app/cache
mkdir /var/www/gcs/app/cache
mkdir /var/www/gcs/app/cache/assignments
mkdir /var/www/gcs/app/cache/courses
chown -R nginx:nginx /var/www/gcs/app/cache
systemctl start app