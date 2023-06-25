#!/bin/bash
# This script will update the nginx
# configuration and reload nginx.
if [ $HOSTNAME != "link" ]
then
  echo This script must only be run in production!
  exit 1
fi

if [ "$EUID" -ne 0 ]
  then echo "Error : Please run as root"
  exit 1
fi

# Go to the project root
cd $(dirname $0)/..

./scripts/remove_default_site.sh
cat configs/shlink/shlink > /etc/nginx/sites-available/shlink
cat configs/common/ssl.conf > /etc/nginx/ssl.conf

# Create symlink only if it doesn't exist
if [ ! -L /etc/nginx/sites-enabled/shlink ]
then
  ln -s /etc/nginx/sites-available/shlink /etc/nginx/sites-enabled/shlink
fi