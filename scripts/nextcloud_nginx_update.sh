#!/bin/bash
# This script will update the nginx
# configuration and reload nginx.
if [ "$EUID" -ne 0 ]
  then echo "Error : Please run as root"
  exit 1
fi

if [ $HOSTNAME != "cloud" ]
then
  echo This script must only be run in production!
  exit 1
fi

# Go to the project root
cd $(dirname $0)/..

./scripts/remove_default_site.sh
cat configs/nextcloud/nextcloud > /etc/nginx/sites-available/nextcloud
cat configs/common/ssl.conf > /etc/nginx/ssl.conf

# Create symlink only if it doesn't exist
if [ ! -L /etc/nginx/sites-enabled/nextcloud ]
then
  ln -s /etc/nginx/sites-available/nextcloud /etc/nginx/sites-enabled/nextcloud
fi