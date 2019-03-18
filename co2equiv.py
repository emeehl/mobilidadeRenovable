#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  4 10:59:37 2019

@author: Víctor M. Álvarez
"""


import paho.mqtt.client as mqtt
import re
import datetime as dt
import time as t


import logging
import logging.handlers
import sys

#from bannerCO2 import xeneraBannerPNG

# Variables globais
conectado = False #Retén o estado de conexión ao broker mqtt

# Variables mqtt
broker = 'iot.eclipse.org'
porto = 1883

#broker = 'm11.cloudmqtt.com' #Broker CloudMQTT
#porto = 12948                #Porto CloudMQTT
#user = 'mobRenovable'
#password = 'm0bR3n0v4bl3'

# Canais mqtt (topics)
xeral = 'mobRenovable/'
diaria = xeral + 'diaria/'
total = xeral + 'total/'
equivalencias = ['enerxia', 'co2', 'distancia', 'arboles']
canaisDiarias = [diaria + eq for eq in equivalencias]
canaisTotais = [total + eq for eq in equivalencias]


# Xestións dos logs
#LOG_FILENAME = "/tmp/" + dt.datetime.today().strftime('%Y%m%d') + "_co2equiv.log"
LOG_FILENAME = "/tmp/co2equiv.log"
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
logger.addHandler(fh)

#class MyLogger(object):
#    def __init__(self, logger, level):
#        self.logger = logger
#        self.level = level
#        
#    def write(self, message):
#        if message.rstrip() != "":
#            self.logger.log(self.level, message.rstrip())
#            
#sys.stdout = MyLogger(logger, logging.INFO)
#sys.stderr = MyLogger(logger, logging.ERROR)

def obterEnerxia():
    """
    Consulta os arquivos de log na ruta '/var/log/sbfspot.3/' para obter a 
    enerxía xerada no día e globalmente.
    
    Devolve:
        Unha lista co resultado en kWh. O primeiro elemento é o total
    do día e o segundo elemento o total global.
    """
    hoxe = dt.datetime.today()
    
    # Ruta log sbfspot.3
    #ruta = /var/log/sbfspot.3/
    ruta = '/home/menduinha/Escritorio/sbfspot.3/'
    nomeArquivo = 'ULaboral_Culleredo_' + hoxe.strftime('%Y%m%d') + '.log'
    ruta += nomeArquivo
    
    enerxHoxe = re.compile('.*EToday:\s*(?P<EToday>\d*.\d*)kWh.*')
    enerxTotal = re.compile('.*ETotal:\s*(?P<ETotal>\d*.\d*)kWh.*')
    #enerxia = re.compile('.*EToday:\s*(?P<EToday>\d*.\d*)kWh.*\s*' + \
    #                     '.*ETotal:\s*(?P<ETotal>\d*.\d*)kWh.*')
    eHoxe = None; eTotal = None
    f = open(ruta, 'r')
    for row in f:
        hoxe = enerxHoxe.search(row)
        total = enerxTotal.search(row)
        if hoxe:
            eHoxe = hoxe.group('EToday')
        if total:
            eTotal = total.group('ETotal')
    f.close()
    if eHoxe and eTotal:
        resultado = [float(eHoxe), float(eTotal)]
    else:
        resultado = None
    return resultado

def obterEquivalencias(enerxia):
    """
    A partir dun valor de enerxia en kWh, obtén o equivalente en kg de CO2, 
    distancia percorrida (km) por un coche eléctrico e número de árbores 
    equivalentes que fixarían o CO2 aforrado.
    
    As equivalencias empregadas son:
        (0) o propio valor en kWh
        (a) 420 g de CO2 evitado por cada 1 kWh producido;
        (b) 100 km percorridos por coche eléctrico por cada 15 kWh;
        (c) 13 kg de CO2 fixado por árbol e ano.
        
    Devolve:
        Unha lista cos resultados en kg de CO2 evitados, km percorridos en
        coche eléctrico e número de árbores equivalentes ao CO2 evitado.
        Nesta mesma orde.    
    """
    equivalencias = [1., .420, 100./15, .420/13]
    return [enerxia * eq for eq in equivalencias]

def axustaUnidades(equivalencias):
    """
    A partir da lista de valores de obterEquivalencias(), axusta as unidades
    a MWh, t C02, miles km e miles arboles, segundo sexa o caso.
    
    Devolve:
        Unha lista de textos, nos que se inclúen as unidades correspondentes.
        Na mesma orde.
    """
    unidades = ['kWh', 'kg CO2', 'km eCar', 'arboles/ano']
    miles = ['MWh', 't CO2', 'miles km', 'miles arboles']
    millons = ['GWh', 'kt CO2', 'millons km' ' millons arbores']
    resultado = []
    for i in range(len(equivalencias)):
        if equivalencias[i] > 1000000:
            resultado.append(str(round(equivalencias[i]/1000000., 1)) + ' ' + \
                                 millons[i])
        elif equivalencias[i] > 1000:
            resultado.append(str(round(equivalencias[i]/1000., 1)) + ' ' + \
                                 miles[i])
        else:
            resultado.append(str(round(equivalencias[i], 1)) + ' ' + \
                             unidades[i])
    return resultado

def obterDatos():
    """
    A partir da saída de axustaUnidades, converte o resultado nun diccionario
    que pode consultar o módulo 'bannerCO2'.
    """
    resultado = {'inversor': '', 'eIndustria': '', 'eCoche': '', 'arbol': ''}
    producion = obterEnerxia()
    prodDiaria, prodTotal = producion
    if producion:
        datos = axustaUnidades(obterEquivalencias(prodTotal))
        resultado = {'inversor': datos[0], 
                     'eIndustria': datos[1],
                     'eCoche': datos[2], 
                     'arbol': datos [3]}
    return resultado

def on_connect(client, userdata, flags, rc):
    global conectado
    logger.debug('Empezando on_connect()')
    if rc == 0:
        conectado = True
        logger.debug('Conectado ao broker, co rc: ' + str(rc))
    else:
        conectado = False
        logger.debug('Non conectado ao broker, co rc: ' + str(rc))
    logger.debug('Rematando on_connect()')
    
def on_disconnect(client, userdata, rc):
    global conectado
    logger.debug('Desconectado, rc: ' + rc)
    logger.debug('Desconectado, conectado: ' + conectado)
    

def on_message(client, userdata, msg):
    pass

def publicar():
    producion = obterEnerxia()
    prodDiaria, prodTotal = producion
    if producion:
        logger.debug('Empezando publicacion no broker')
        mensaxes = axustaUnidades(obterEquivalencias(prodDiaria))
#        logger.info(mensaxes)
        for i in range(len(mensaxes)):
            c = canaisDiarias[i]; m = mensaxes[i]
            cliente.publish(c, m)
            logger.info('Publicado no canal ' + c + ': ' + m)
        mensaxes = axustaUnidades(obterEquivalencias(prodTotal))
#        xeneraBannerPNG(mensaxes)
        for i in range(len(mensaxes)):
            c = canaisTotais[i]; m = mensaxes[i]
            cliente.publish(c, m)
            logger.info('Publicado no canal ' + c + ': ' + m)
        logger.debug('Rematando publicacion no broker')
    t.sleep(.1) #Deixa tempo para que remate a publicación antes de saír do script


if __name__ == "__main__":
    cliente = mqtt.Client()
    cliente.on_connect = on_connect
    cliente.on_message = on_message
    cliente.on_disconnect = on_disconnect
    cliente.connect(broker, porto, 60)
#    client.connect("iot.eclipse.org", 1883, 60)
    
#   cliente.loop_start()  #Mellor loop_start, proporciona un fio non bloqueante
#   client.loop_forever() #loop_forever proporciona un fío bloqueante
    
#    while conectado != True: #Espera a que a conexión sexa efectiva
#        t.sleep(.1)
#        
    publicar()
    cliente.disconnect()
#    while conectado == True:  #Espera a que a desconexión sexa efectiva
#        t.sleep(.1)
    logger.debug('Desconectado do broker')
    logger.removeHandler(fh)
        

    
