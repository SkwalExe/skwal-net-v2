#!/bin/bash
# This script will update the nginx
# configuration and reload nginx.
if [ $HOSTNAME != "reverse-proxy" ]
then
  echo This script must only be run in production!
  exit 1
fi

echo Dont forget to run as root

rm -f /etc/nginx/sites-enabled/default /etc/nginx/sites-available/default
cat configs/nginx/sites-available/reverse_proxy > /etc/nginx/sites-available/reverse_proxy
cat configs/nginx/ssl.conf > /etc/nginx/ssl.conf
ln -s /etc/nginx/sites-available/reverse_proxy /etc/nginx/sites-enabled/reverse_proxy