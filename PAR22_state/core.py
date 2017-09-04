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
from Libraries import SNMPget, log, Tx_state, HpaInfo

# Activation du logger principal
logging.basicConfig(level=logging.INFO, format='%(asctime)s : %(message)s')
logger = logging.getLogger(__name__)
handler = RotatingFileHandler('/var/log/PAR22_state.log', maxBytes=100, backupCount=5)
logger.addHandler(handler)

# Récupération des variables de démarrage
parser = ArgumentParser()
parser.add_argument("-c", "--config", dest="config", help="Préciser le chemin du fichier config.ini")
args = parser.parse_args()

# Lecture du fichier de Configuration et attribution des variables
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



# Démarrage de la boucle de vérification d'état de transmission
log("info", "Initialisation du script...")
time.sleep(2)

# Initialisation de l'état des leds
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(GpioPin1, GPIO.OUT)
GPIO.output(GpioPin1, 0)
GPIO.setup(GpioPin2, GPIO.OUT)
GPIO.output(GpioPin2, 0)

# Récupération infos des HPA
HpaInfo('1', Hpa1Addr, OidModel, OidSerial, OidFirmware, OidTotalSystemHours, OidTotalTransmitHours)
HpaInfo('2', Hpa2Addr, OidModel, OidSerial, OidFirmware, OidTotalSystemHours, OidTotalTransmitHours)
log("info", "Lancement de la vérification de l'état des IBUC de la PAR22...")

# Lancement de la boucle de test
try:
    while True:
        Tx_state(Hpa1Addr, OidTxState, GpioPin1)
        time.sleep(1)
        Tx_state(Hpa2Addr, OidTxState, GpioPin2) 
        time.sleep(1)
finally:
    GPIO.cleanup()
