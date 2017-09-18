#!/bin/bash

cd /home/pi/
sudo mv -f PAR22_state/ /usr/local/bin/
echo "*** Déplacement du dossier dans /usr/local/bin ***"
cd /usr/local/bin/PAR22_state/PAR22_state/
sudo chmod +x core.py
sudo chmod +x Libraries.py
echo "*** Ajout des droits d'exécution ***"
echo -e "$(sudo crontab -u root -l)\n@reboot /usr/bin/python3 /usr/local/bin/PAR22_state/PAR22_state/core.py -c '/usr/local/bin/PAR22_state/PAR22_state/config.ini'" | sudo crontab -u root -l
echo "*** Activation du script au reboot via sudo crontab ***"
echo "*** Installation terminée ***"
