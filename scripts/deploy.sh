#!/bin/bash
# This script will put the server under
# maintenance mode, pull the latest changes
# from the git repository, and then bring the
# application back online.

# Go to the project root
cd $(dirname $0)/..

if [ $HOSTNAME != "skwal-server" ]
then
  echo This script must only be run in production!
  exit 1
fi

# Enable maintenance and stop services
touch hooks/maintenance
sudo systemctl stop gunicorn
echo Enabling maintenance mode
sleep 5

# Pull latest changes
sudo -u skwal git reset --hard HEAD
sudo -u skwal git clean -f -d
sudo -u skwal git pull origin main

# Update dependencies, database, and static files
source /var/www/prod_env/bin/activate
sudo -u skwal pip install -r requirements.txt
sudo -u skwal python3 skwal_net/manage.py migrate
rm -rf skwal_net/static
sudo -u skwal python3 skwal_net/manage.py collectstatic --noinput
deactivate

# set permissions
sudo chown -R skwal:www-data .
sudo chmod -R 775 . # rwxrwxr-x

# Restart services and disable maintenance mode
echo Disabling maintenance mode
sudo systemctl start gunicorn
sleep 10
rm -f hooks/maintenance
echo Done!
