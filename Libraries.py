#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Ce fichier est une librairie requise par le script PAR22_state_SNMP.py
"""

# Import des librairies
import RPi.GPIO as GPIO
from pysnmp.hlapi import *
import time
import logging
import re

# Définition de la fonction de logging
def log(level, msg):
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
    logger = logging.getLogger(__name__)
    if level == "debug":
        logger.debug(msg)
    elif level == "info":
        logger.info(msg)
    else:
        logger.error(msg)

# Définition de la commande SNMP Get
def SNMPget(IPAddr, OID):
    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
            CommunityData('private', mpModel=0),
            UdpTransportTarget((IPAddr, 161)),
            ContextData(),
            ObjectType(ObjectIdentity(OID))))

    if errorIndication:
        log("error", errorIndication)
    elif errorStatus:
        log("error", '%s at %s' % (errorStatus.prettyPrint(),
                            errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
    else:
        for varBind in varBinds:
            state = (' = '.join([x.prettyPrint() for x in varBind]))
            log("debug", state)
            return state
        
# Définition de la fonction de vérification d'état du HPA            
def Tx_state(IPAddr, OidTxState, GpioPin):
    state = SNMPget(IPAddr, OidTxState) 
    if state[-1:] == '1':
        if GPIO.input(GpioPin) == 0:
            GPIO.output(GpioPin, 1)
            log("info", "IBUC PAR22 {0} : transmission active (pin GPIO : {1})".format(IPAddr, GpioPin))
        else:
            pass
    elif state[-1:] == '2':
        for i in range(4):
            GPIO.output(GpioPin, 1)
            time.sleep(0.3)
            GPIO.output(GpioPin, 0)
            time.sleep(0.3)
            i +=1
        log("error", "IBUC PAR22 {0} muted due to alarm !!!".format(IPAddr))
    else:
        if GPIO.input(GpioPin) == 1:
            GPIO.output(GpioPin, 0)
            log("info", "IBUC PAR22 {0} : transmission inactive (pin GPIO : {1})".format(IPAddr, GpioPin))
        else:
            pass

def HpaInfo(IPAddr, OidModel, OidSN, OidFW, OidTSH, OidTTH):
    Infos = {'IPAddr':IPAddr,
             'Model':SNMPget(IPAddr, OidModel),
             'SN':SNMPget(IPAddr, OidSN),
             'FW':SNMPget(IPAddr, OidFW),
             'TSH':SNMPget(IPAddr, OidTSH),
             'TTH':SNMPget(IPAddr, OidTTH)
             }
    m = re.search('(.*)\ =\ (.*)', Infos['Model'])
    print(m.group(2))
    