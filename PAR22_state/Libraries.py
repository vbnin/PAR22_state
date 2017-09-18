#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Developeurs : VBNIN + CKAR - IPEchanges.
Ce fichier est une librairie requise par le script PAR22_state_SNMP.py
"""

# Import des librairies
import RPi.GPIO as GPIO
from pysnmp.hlapi import *
import time
import logging
import re

# Activation du logger
logger = logging.getLogger(__name__)

# Définition de la commande SNMP Get
def SNMPget(IPAddr, OID):
    try:
        errorIndication, errorStatus, errorIndex, varBinds = next(
            getCmd(SnmpEngine(),
                CommunityData('private', mpModel=0),
                UdpTransportTarget((IPAddr, 161)),
                ContextData(),
                ObjectType(ObjectIdentity(OID))))

        if errorIndication:
            logger.error(errorIndication)
            state = '2'
            return state
        elif errorStatus:
            logger.error('%s at %s' % (errorStatus.prettyPrint(),
                            errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
            state = '2'
            return state
        else:
            for varBind in varBinds:
                state = (' = '.join([x.prettyPrint() for x in varBind]))
                logger.debug(state)
                return state
    except:
        logger.error("Erreur générale...")
        state = '2'
        return state
        
# Définition de la fonction de vérification d'état du HPA            
def Tx_state(IPAddr, OidTxState, GpioPin):
    state = SNMPget(IPAddr, OidTxState)
    if state[-1:] == '1':
        if GPIO.input(GpioPin) == 0:
            GPIO.output(GpioPin, 1)
            logger.info("IBUC PAR22 {0} : transmission active (pin GPIO : {1})".format(IPAddr, GpioPin))
        else:
            pass
    elif state[-1:] == '2':
        for i in range(3):
            GPIO.output(GpioPin, 1)
            time.sleep(0.3)
            GPIO.output(GpioPin, 0)
            time.sleep(0.3)
            i +=1
        logger.error("IBUC PAR22 {0} en alarme ou injoignable !!!".format(IPAddr))
    else:
        if GPIO.input(GpioPin) == 1:
            GPIO.output(GpioPin, 0)
            logger.info("IBUC PAR22 {0} : transmission inactive (pin GPIO : {1})".format(IPAddr, GpioPin))
        else:
            pass

def HpaInfo(Nb, IPAddr, OidModel, OidSN, OidFW, OidTSH, OidTTH, OidTx):
    Infos = {'Model':SNMPget(IPAddr, OidModel),
             'Serial Number':SNMPget(IPAddr, OidSN),
             'Firmware':SNMPget(IPAddr, OidFW),
             'Total System Hours':SNMPget(IPAddr, OidTSH),
             'Total Transmit Hours':SNMPget(IPAddr, OidTTH)
             'Etat actuel de la transmission':SNMPget(IPAddr, OidTx)
             }
    logger.info("*** Spécifications du HPA #" + Nb + " ***")
    logger.info("Adresse IP : " + IPAddr)
    for key in Infos:
        m = re.search('(.*)\ =\ (.*)', Infos[key])
        if m is not None:
            logger.info(key + " : " + m.group(2))
    logger.info("***")
    
def PrintException(msg):
    print("***********************************************************************")
    print(msg)
    print("***********************************************************************")
