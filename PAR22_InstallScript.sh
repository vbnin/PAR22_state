#!/bin/bash

sudo cp PAR22_state/ /usr/local/bin/
echo -e "$(sudo crontab -u root -l)\n@reboot python /usr/local/bin/PAR22_state/core.py -c "config.ini" > /var/log/PAR22_state.log 2>&1" | sudo crontab -u root -
