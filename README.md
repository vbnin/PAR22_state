# PAR22_state v1.1
Script de retour d'état des HPA PAR22

Ce script Python a été conçu pour obtenir via SNMP des informations sur les amplificateurs IBUC Terrasat.

Attention, ce script utilise la library Rpi.GPIO de Raspberry. Il n'est pas exécutable autrement que sur Raspberry Pi.

*** Instructions d'installation : ***
0 - Prérequis : Le Raspberry doit être connecté à internet pour télécharger les paquets Python3 requis

1 - Déposer le dossier complet dans '/home/pi/'

2 - Exécuter le script d'installation avec : "sudo ./PAR22_InstallationScript.sh"

3 - Après redémarrage automatique du Raspberry, le script sera exécuté à chaque reboot et ses logs sont accessibles dans '/var/log/PAR22_state.log'.

-vbnin-
