#/bin/bash
# This script will put the server under
# maintenance mode, pull the latest changes
# from the git repository, and then bring the
# application back online.

touch maintenance/ACTIVE
echo Enabling maintenance mode
sleep 5

git reset --hard HEAD
git clean -f -d
git pull origin main

rm -f maintenance/ACTIVE
echo Disabling maintenance mode
sleep 5
echo Done!
