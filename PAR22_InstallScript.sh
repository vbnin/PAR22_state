#!/bin/bash

sudo cp PAR22_state/ /usr/local/bin/
(sudo crontab -l 2>/dev/null; echo "@reboot python /usr/local/bin/PAR22_state/core.py -c "config.ini" > /var/log/PAR22_state.log 2>&1") | crontab -
