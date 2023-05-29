#!/bin/bash
# This script will update the nginx
# configuration and reload nginx.
if [ $HOSTNAME != "skwal-server" ]
then
  echo This script must only be run in production!
  exit 1
fi

echo Dont forget to run as root

rm -f /etc/nginx/sites-enabled/default /etc/nginx/sites-available/default
cat configs/nginx/sites-available/skwal_net > /etc/nginx/sites-available/skwal_net
cat configs/skwal.conf > /etc/nginx/skwal.conf
ln -s /etc/nginx/sites-available/skwal_net /etc/nginx/sites-enabled/skwal_net