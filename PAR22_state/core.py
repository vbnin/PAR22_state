#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Developeurs : VBNIN + CKAR - IPEchanges.

Ce script est destiné à relever l'état de transmission des amplificateurs
bi-feed de la PAR22 via leur protocole SNMP. 
Ne fonctionne que sur Raspberry Pi.
"""

# Import des librairies
import time
import logging
import ConfigParser
import RPi.GPIO as GPIO
from logging.handlers import RotatingFileHandler
from argparse import ArgumentParser
from Libraries import SNMPget, Tx_state, HpaInfo, PrintException

# Activation du logger principal
try:
    handler = RotatingFileHandler('/var/log/PAR22_state.log', maxBytes=10000000, backupCount=5)
    handler.setFormatter(logging.Formatter('%(asctime)s : %(message)s'))
    logging.basicConfig(level=logging.INFO, format='%(asctime)s : %(message)s')
    logger = logging.getLogger(__name__)
    logger.addHandler(handler)
except:
    PrintException("Impossible d'initialiser le fichier de logs.")
    exit()

# Récupération des variables de démarrage
parser = ArgumentParser()
parser.add_argument("-c", "--config", dest="config", help="Préciser le chemin du fichier config.ini")
args = parser.parse_args()

# Lecture du fichier de Configuration et attribution des variables
try:
    config = ConfigParser.ConfigParser()
    config.read(args.config)
    Hpa1Addr = config.get('ADDRESS','Hpa1Addr')
    Hpa2Addr = config.get('ADDRESS','Hpa2Addr')
    OidModel = config.get('OID','OidModel')
    OidSerial = config.get('OID','OidSerial')
    OidFirmware = config.get('OID','OidFirmware')
    OidTotalSystemHours = config.get('OID','OidTotalSystemHours')
    OidTotalTransmitHours = config.get('OID','OidTotalTransmitHours')
    OidTxState = config.get('OID','OidTxState')
    GpioPin1 = int(config.get('GPIO','GpioPin1'))
    GpioPin2 = int(config.get('GPIO','GpioPin2'))

except:
    PrintException("Fichier de configuration invalide ou non précisé.\n\033[1;31mPour rappel :\033[1;33m sudo ./core.py -c 'emplacement du fichier de configuration'\033[0m")
    exit()

# Démarrage de la boucle de vérification d'état de transmission
logger.info("Initialisation du script...")
time.sleep(2)

# Initialisation de l'état des leds
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(GpioPin1, GPIO.OUT)
GPIO.output(GpioPin1, 0)
GPIO.setup(GpioPin2, GPIO.OUT)
GPIO.output(GpioPin2, 0)

# Récupération infos des HPA
HpaInfo('1', Hpa1Addr, OidModel, OidSerial, OidFirmware, OidTotalSystemHours, OidTotalTransmitHours, OidTxState)
HpaInfo('2', Hpa2Addr, OidModel, OidSerial, OidFirmware, OidTotalSystemHours, OidTotalTransmitHours, OidTxState)
logger.info("Lancement de la vérification de l'état des IBUC de la PAR22...")

# Lancement de la boucle de test
try:
    while True:
        Tx_state(Hpa1Addr, OidTxState, GpioPin1)
        time.sleep(1)
        Tx_state(Hpa2Addr, OidTxState, GpioPin2) 
        time.sleep(1)
finally:
    GPIO.cleanup()
