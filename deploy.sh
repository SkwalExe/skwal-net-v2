#/bin/bash
# This script will put the server under
# maintenance mode, pull the latest changes
# from the git repository, and then bring the
# application back online.

mv maintenance/maintenance.html maintenance/ACTIVE/maintenance.html
sleep 5
git reset --hard HEAD
git clean -f -d
git pull origin main

# The git reset and git clean commands will automatically 
# move the maintenance.html file back to the maintenance 
# directory. So we dont need to do that.
# mv maintenance/ACTIVE/maintenance.html maintenance/maintenance.html

echo Done!
