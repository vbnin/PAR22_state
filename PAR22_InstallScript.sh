#!/bin/bash

echo "*** Déplacement du dossier dans /usr/local/bin ***"
cd /home/pi/
sudo mv -f PAR22_state/ /usr/local/bin/

echo "*** Ajout des droits d'exécution ***"
cd /usr/local/bin/PAR22_state/PAR22_state/
sudo chmod +x core.py
sudo chmod +x Libraries.py

echo "*** Activation du script au reboot via sudo crontab ***"
echo -e "$(crontab -u pi -l)\n@reboot sudo /usr/bin/python3 /usr/local/bin/PAR22_state/PAR22_state/core.py -c '/usr/local/bin/PAR22_state/PAR22_state/config.ini'" | crontab -u pi -

echo "*** Installation des packages Python3 pré-requis ***"
sudo pip3 install configparser
sudo pip3 install argparse
sudo pip3 install pysnmp

echo "*** Installation terminée, reboot dans 15 secondes. Pour annuler, pressez 'Ctrl + C' ***"
sleep 15
sudo reboot
