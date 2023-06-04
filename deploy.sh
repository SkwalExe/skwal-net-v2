#!/bin/bash
# This script will put the server under
# maintenance mode, pull the latest changes
# from the git repository, and then bring the
# application back online.

cd /var/www/skwal-net-v2/

if [ $HOSTNAME != "skwal-server" ]
then
  echo This script must only be run in production!
  exit 1
fi

touch hooks/maintenance
sudo systemctl stop gunicorn
echo Enabling maintenance mode
sleep 5

git reset --hard HEAD
git clean -f -d
git pull origin main

source /var/www/prod_env/bin/activate
sudo -u skwal pip install -r requirements.txt
python3 skwal_net/manage.py migrate
rm -rf skwal_net/static
python3 skwal_net/manage.py collectstatic --noinput

# set permissions
sudo chown -R skwal:www-data .
sudo chmod -R 775 . # rwxrwxr-x

deactivate

echo Disabling maintenance mode
sudo systemctl start gunicorn
sleep 10
rm -f hooks/maintenance
echo Done!
