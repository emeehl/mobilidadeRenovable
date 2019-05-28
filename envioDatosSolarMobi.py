#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 30 22:27:46 2019

@author: menduinha
"""

import json, requests
import os
import datetime as d
import obterDatos

import logging
import logging.handlers

home = os.environ['HOME']
#rutaLog = home + '/Google.Drive/log/'
#rutaScripts = home + '/Google.Drive/scripts/'
#rutaLog = '/var/log/envioDatosSolarMobi/'
rutaScripts = home + '/scripts/'
rutaLog = rutaScripts + 'log/'

# Xestións dos logs
#LOG_FILENAME = "/tmp/" + dt.datetime.today().strftime('%Y%m%d') + "_co2equiv.log"
LOG_FILENAME = rutaLog + "envioDatosSolarMobi.log"
#LOG_LEVEL = logging.DEBUG
LOG_LEVEL = logging.INFO
#Crear o logger e conectarse a el
logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', \
                              datefmt = '%Y%m%d %H:%M:%S')
#Crear manipulador do logging, formato, etc
#fh = logging.FileHandler(LOG_FILENAME)
fh = logging.handlers.TimedRotatingFileHandler(LOG_FILENAME, \
            when="midnight", backupCount=3)
fh.setLevel(LOG_LEVEL)
fh.setFormatter(formatter)
#Conectar o manipulador co logger
logger.addHandler(fh)

try:
    # Obtemos os valores acumulados no último periodo de 15 min (cun retraso de 3 min)
    logger.debug('Obtendo valores acumulados do último perido')
    agora = d.datetime.today()# - d.timedelta(hours=10)
    res = obterDatos.datosAcumulados(agora, acum = 15, retraso = 3)
    
    # Lemos os parámetros de conexión 
    logger.debug('Lendo arquivo de parámetros de conexión: inversor.json')
    nomeArquivo = rutaScripts + 'inversor.json'
    f = open(nomeArquivo, mode='r')
    datosConexion = json.load(f)
    f.close()
    
    # Executamos un POST á URL lida (co código de conexión obtido), enciando un JSON cos valores
    # Os valores están formateados como str representando float de 3 decimais (separador
    # decimal: punto), a data ten o formato indicado.
    url = datosConexion['api']
    logger.debug('Formateando os valores obtidos do último periodo')
    medicion = {'fechahora': res['data'].strftime('%Y-%m-%d %H:%M:%S'),
                'potenciatotalac': str('%.3f' % res['PacTot']),
                'energiadiaria': str('%.3f' % res['EPeriodo']),
                'energiatotal': str('%.3f' % res['ETotal'])}
    logger.debug('Enviando datos JSON')
    
    payload = {"codigoseccom": datosConexion['codigoseccom'], "medicion": json.dumps(medicion)}
    resposta = requests.post(url, data=payload)
    if resposta.ok:
        logger.info('Enviado ok: ' + json.dumps(medicion))
        logger.info('Resposta: ' + resposta.text)
    else:
        logger.error('Ocorreu un erro na transmisión: ' + resposta.text)
        logger.error('Código de erro: ' + resposta.status_code)
except KeyError:
    logger.error('Non se conseguíu obter valores para o último periodo')
except FileNotFoundError:
    logger.error('Non se encontrou o arquivo de parámetros de conexión')
logger.removeHandler(fh)

