#!/bin/bash
# This script will check for the hooks/redeploy file
# and if it exists, it will pull the latest changes
# from the git repository by calling deploy.sh.

while true; do
  if [ -f hooks/redeploy ]; then
    rm -f hooks/redeploy
    ./deploy.sh
  fi
  sleep 5
done