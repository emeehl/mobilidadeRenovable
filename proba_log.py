#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 13:43:38 2019

@author: menduinha
"""

import datetime as dt
import time as t


import logging
import logging.handlers


# Xestións dos logs
#LOG_FILENAME = "/tmp/" + dt.datetime.today().strftime('%Y%m%d') + "_co2equiv.log"
LOG_FILENAME = "/tmp/proba.log"
#LOG_FILENAME = "/var/log/co2equiv.log"
LOG_LEVEL = logging.INFO
#Crear o logger e conectarse a el
logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s', \
                              datefmt = '%Y%m%d %H:%M:%S')
#Crear manipulador do logging, formato, etc
#fh = logging.FileHandler(LOG_FILENAME)
fh = logging.handlers.TimedRotatingFileHandler(LOG_FILENAME, \
            when="midnight", backupCount=3)
fh.setLevel(LOG_LEVEL)
fh.setFormatter(formatter)
#Conectar o manipulador co logger
#logger.addHandler(fh)


def proba_log():
    logger.info('Comprobando xeración de logs')
#    logger.debug('Comprobando xeración de logs')
    

if __name__ == "__main__":
    proba_log()