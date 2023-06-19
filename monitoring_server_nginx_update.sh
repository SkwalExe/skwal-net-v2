#!/bin/bash
# This script will update the nginx
# configuration and reload nginx.
echo Dont forget to run as root

rm -f /etc/nginx/sites-enabled/default /etc/nginx/sites-available/default
cat configs/nginx/sites-available/status_page > /etc/nginx/sites-available/status_page
cat configs/nginx/ssl.conf > /etc/nginx/ssl.conf
ln -s /etc/nginx/sites-available/status_page /etc/nginx/sites-enabled/status_page