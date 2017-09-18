#!/bin/bash

cd /home/pi/
sudo mv -f PAR22_state/ /usr/local/bin/
echo "*** Déplacement du dossier dans /usr/local/bin ***"
cd /usr/local/bin/PAR22_state/PAR22_state/
sudo chmod +x core.py
sudo chmod +x Libraries.py
echo "*** Ajout des droits d'exécution ***"
echo -e "$(crontab -u pi -l)\n@reboot sudo /usr/bin/python /usr/local/bin/PAR22_state/PAR22_state/core.py -c '/usr/local/bin/PAR22_state/PAR22_state/config.ini'" | crontab -u pi -
echo "*** Activation du script au reboot via sudo crontab ***"
echo "*** Installation terminée, reboot dans 15 secondes. Pour annuler, pressez 'Ctrl + C' ***"
sleep 15
sudo reboot
