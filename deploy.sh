#/bin/bash
# This script will put the server under
# maintenance mode, pull the latest changes
# from the git repository, and then bring the
# application back online.

mv maintenance/maintenance.html maintenance/ACTIVE/maintenance.html
git reset --hard HEAD
git clean -f -d
git pull origin master
sleep 5
mv maintenance/ACTIVE/maintenance.html maintenance/maintenance.html

echo Done!