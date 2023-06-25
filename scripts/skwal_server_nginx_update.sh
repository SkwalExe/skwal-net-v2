#!/bin/bash
# This script will update the nginx
# configuration and reload nginx.

if [ "$EUID" -ne 0 ]
  then echo "Error : Please run as root"
  exit 1
fi

if [ $HOSTNAME != "skwal-server" ]
then
  echo This script must only be run in production!
  exit 1
fi

# Go to the project root
cd $(dirname $0)/..

./scripts/remove_default_site.sh

cat configs/skwal_net/skwal_net > /etc/nginx/sites-available/skwal_net
cat configs/skwal_net/skwal.conf > /etc/nginx/skwal.conf
cat configs/common/ssl.conf > /etc/nginx/ssl.conf

# Create symlink only if it doesn't exist
if [ ! -L /etc/nginx/sites-enabled/skwal_net ]
then
  ln -s /etc/nginx/sites-available/skwal_net /etc/nginx/sites-enabled/skwal_net
fi