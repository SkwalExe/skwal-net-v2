#!/bin/bash
# This script will update the nginx
# configuration and reload nginx.

if [ "$EUID" -ne 0 ]
  then echo "Error : Please run as root"
  exit 1
fi

if [ $HOSTNAME != "status" ]
then
  echo This script must only be run in production!
  exit 1
fi

# Go to the project root
cd $(dirname $0)/..

./scripts/remove_default_site.sh
cat configs/status_page/status_page > /etc/nginx/sites-enabled/status_page
cat configs/common/ssl.conf > /etc/nginx/ssl.conf

# Create symlink only if it doesn't exist
if [ ! -L /etc/nginx/sites-enabled/status_page ]
then
  ln -s /etc/nginx/sites-available/status_page /etc/nginx/sites-enabled/status_page
fi