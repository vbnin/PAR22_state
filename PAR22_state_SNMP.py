#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
v1.4 - Python3 - 31/08/17 - VBNIN + CKAR - IPEchanges.

Ce script est destiné à relever l'état de transmission des amplificateurs
bi-feed de la PAR22 via leur protocole SNMP
"""

# Import des librairies
from argparse import ArgumentParser
import RPi.GPIO as GPIO
import time
import logging
import ConfigParser
from Libraries import SNMPget, log, Tx_state, HpaInfo

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

# Initialisation de l'état des leds
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(GpioPin1, GPIO.OUT)
GPIO.output(GpioPin1, 0)
GPIO.setup(GpioPin2, GPIO.OUT)
GPIO.output(GpioPin2, 0)

# Démarrage de la boucle de vérification d'état de transmission
time.sleep(0)
log("info", "Récupération des infos du 1er HPA :")
HpaInfo(Hpa1Addr, OidModel, OidSerial, OidFirmware, OidTotalSystemHours, OidTotalTransmitHours)
log("info", "Récupération des infos du 1er HPA :")
HpaInfo(Hpa2Addr, OidModel, OidSerial, OidFirmware, OidTotalSystemHours, OidTotalTransmitHours)
log("info", "Lancement de la verification de l'etat des IBUC de la PAR22.")
try:
    while True:
        Tx_state(Hpa1Addr, OidTxState, GpioPin1)
        time.sleep(1)
        Tx_state(Hpa2Addr, OidTxState, GpioPin2) 
        time.sleep(1)
finally:
	GPIO.cleanup()
