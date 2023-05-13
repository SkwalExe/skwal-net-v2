#!/bin/bash
# This script will put the server under
# maintenance mode, pull the latest changes
# from the git repository, and then bring the
# application back online.

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

source /home/skwal/prod_env/bin/activate
pip install -r requirements.txt
python3 skwal_net/manage.py migrate
rm -rf skwal_net/static
python3 skwal_net/manage.py collectstatic --noinput
deactivate

echo Disabling maintenance mode
sudo systemctl start gunicorn
sleep 10
rm -f hooks/maintenance
echo Done!
