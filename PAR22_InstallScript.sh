#!/bin/bash

cd /home/pi/
sudo cp -fR PAR22_state/ /usr/local/bin/
cd /usr/local/bin/PAR22_state/PAR22_state/
sudo chmod +x core.py
echo -e "$(sudo crontab -u root -l)\n@reboot python /usr/local/bin/PAR22_state/PAR22_state/core.py -c 'config.ini'" | sudo crontab -u root -
echo "*** Installation terminée ***"
