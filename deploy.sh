#!/bin/bash
# This script will put the server under
# maintenance mode, pull the latest changes
# from the git repository, and then bring the
# application back online.

if [ $HOSTNAME != "esx1" ]
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

echo Disabling maintenance mode
sudo systemctl start gunicorn
sleep 5
rm -f hooks/maintenance
echo Done!
