#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 17 17:28:47 2019

@author: menduinha
"""

import numpy as np
import datetime as d
import re, glob

"""
Unidades
# datetime , texto, texto, numeroSerie
# W cc, W cc, A cc, A cc
# V cc, V cc
# W ca, W ca, W ca (por fases)
# A ca, A ca, A ca (por fases)
# V ca, V ca, V ca (por fases)
# W cc totais, W dc totais, %
# kWh hoxe, kWh total
# Hz, horas, horas
# %, texto, texto
# ºC
"""
#tipo = np.dtype( \
#        [('data', 'object'), ('nomeDisp', 'U20'), ('tipoDisp','U16'), ('numSerie', np.uint16), \
#         ('Pdc1', np.float64), ('Pdc2', np.float64), ('Idc1', np.float64), ('Idc2', np.float64), \
#         ('Udc1', np.float64), ('Udc2', np.float64), \
#         ('Pac1', np.float64), ('Pac2', np.float64), ('Pac3', np.float64), \
#         ('Iac1', np.float64), ('Iac2', np.float64), ('Iac3', np.float64), \
#         ('Uac1', np.float64), ('Uac2', np.float64), ('Uac3', np.float64), \
#         ('PdcTot', np.float64), ('PacTot', np.float64), ('Efficiency', np.float64), \
#         ('EToday', np.float64), ('ETotal', np.float64), \
#         ('Frequency', np.float64), ('OperatingTime', np.float64), ('FeedInTime', np.float64), \
#         ('BT_Signal', np.float64), ('Condition', 'U6'), ('GridRelay', 'U30'), \
#         ('Temperature', np.float64)])   
#
#datos = np.array([], tipo)

#hoxe = d.datetime.today()
#ruta = '/home/pi/Escritorio/smadata/'
ruta = '/home/menduinha/Escritorio/smadata/'
patronArquivo = 'ULaboral_Culleredo-Spot-'
ext = '.csv'

def lerArquivo(arquivo):
    data = u'(?P<data>\d{4}-\d{2}-\d{2}\s*\d{2}:\d{2}:\d{2});'
    nomeDisp = u'(?P<nomeDisp>STP\s*\d*\w*-\d*\s*\d*);'; tipoDisp = u'(?P<tipoDisp>STP\s*\d*\w*-\d*);'
    numSerie = u'(?P<numSerie>\d*);'
    Pdc1 = u'(?P<Pdc1>\d*,\d*);'; Pdc2 = u'(?P<Pdc2>\d*,\d*);'
    Idc1 = u'(?P<Idc1>\d*,\d*);'; Idc2 = u'(?P<Idc2>\d*,\d*);'
    Udc1 = u'(?P<Udc1>\d*,\d*);'; Udc2 = u'(?P<Udc2>\d*,\d*);'
    Pac1 = u'(?P<Pac1>\d*,\d*);'; Pac2 = u'(?P<Pac2>\d*,\d*);'; Pac3 = u'(?P<Pac3>\d*,\d*);'
    Iac1 = u'(?P<Iac1>\d*,\d*);'; Iac2 = u'(?P<Iac2>\d*,\d*);'; Iac3 = u'(?P<Iac3>\d*,\d*);'
    Uac1 = u'(?P<Uac1>\d*,\d*);'; Uac2 = u'(?P<Uac2>\d*,\d*);'; Uac3 = u'(?P<Uac3>\d*,\d*);'
    PdcTot = u'(?P<PdcTot>\d*,\d*);'; PacTot = u'(?P<PacTot>\d*,\d*);'; Efficiency = u'(?P<Efficiency>\d*,\d*);'
    EToday = u'(?P<EToday>\d*,\d*);'; ETotal = u'(?P<ETotal>\d*,\d*);'
    Frequency = u'(?P<Frequency>\d*,\d*);'; OperatingTime = u'(?P<OperatingTime>\d*,\d*);'; FeedInTime = u'(?P<FeedInTime>\d*,\d*);'
    BT_Signal = u'(?P<BT_Signal>\d*,\d*);'; Condition = u'(?P<Condition>\w*);'; GridRelay = u'(?P<GridRelay>[\w\s]*);'
    Temperature = u'(?P<Temperature>\d*,\d*)'
    patron = data + nomeDisp + tipoDisp + numSerie + \
             Pdc1 + Pdc2 + Idc1 + Idc2 + Udc1 + Udc2 + \
             Pac1 + Pac2 + Pac3 + Iac1 + Iac2 + Iac3 + Uac1 + Uac2 + Uac3 + \
             PdcTot + PacTot + Efficiency + EToday + ETotal + Frequency + \
             OperatingTime + FeedInTime + BT_Signal + Condition + GridRelay + \
             Temperature
    comp = re.compile(patron)
    tipo = np.dtype( \
            [('data', 'object'), \
             ('Pdc1', np.float64), ('Pdc2', np.float64), \
             ('Idc1', np.float64), ('Idc2', np.float64), \
             ('Udc1', np.float64), ('Udc2', np.float64), \
             ('Pac1', np.float64), ('Pac2', np.float64), ('Pac3', np.float64), \
             ('Iac1', np.float64), ('Iac2', np.float64), ('Iac3', np.float64), \
             ('Uac1', np.float64), ('Uac2', np.float64), ('Uac3', np.float64), \
             ('PdcTot', np.float64), ('PacTot', np.float64), ('Efficiency', np.float64), \
             ('EToday', np.float64), ('ETotal', np.float64), \
             ('Frequency', np.float64), ('OperatingTime', np.float64), ('FeedInTime', np.float64), \
             ('Temperature', np.float64)])  
    datos = np.array([], tipo)
    try:
        f = open(arquivo, 'r')
        for row in f:
            res = comp.search(row)
            if res:
                rData = d.datetime.strptime(res.group('data'), '%Y-%m-%d %H:%M:%S')
                rPdc1 = float(res.group('Pdc1').replace(',', '.'))
                rPdc2 = float(res.group('Pdc2').replace(',', '.'))
                rIdc1 = float(res.group('Idc1').replace(',', '.'))
                rIdc2 = float(res.group('Idc2').replace(',', '.'))
                rUdc1 = float(res.group('Udc1').replace(',', '.'))
                rUdc2 = float(res.group('Udc2').replace(',', '.'))
                rPac1 = float(res.group('Pac1').replace(',', '.'))
                rPac2 = float(res.group('Pac2').replace(',', '.'))
                rPac3 = float(res.group('Pac3').replace(',', '.'))
                rIac1 = float(res.group('Iac1').replace(',', '.'))
                rIac2 = float(res.group('Iac2').replace(',', '.'))
                rIac3 = float(res.group('Iac3').replace(',', '.'))
                rUac1 = float(res.group('Uac1').replace(',', '.'))
                rUac2 = float(res.group('Uac2').replace(',', '.'))
                rUac3 = float(res.group('Uac3').replace(',', '.'))
                rPdcTot = float(res.group('PdcTot').replace(',', '.'))
                rPacTot = float(res.group('PacTot').replace(',', '.'))
                rEfficiency = float(res.group('Efficiency').replace(',', '.'))
                rEToday = float(res.group('EToday').replace(',', '.'))
                rETotal = float(res.group('ETotal').replace(',', '.'))
                rFrequency = float(res.group('Frequency').replace(',', '.'))
                rOperatingTime = float(res.group('OperatingTime').replace(',', '.'))
                rFeedInTime = float(res.group('FeedInTime').replace(',', '.'))
                rTemperature = float(res.group('Temperature').replace(',', '.'))
                datos = np.append(datos, np.array([(rData, \
                                             rPdc1, rPdc2, rIdc1, rIdc2, rUdc1, rUdc2, \
                                             rPac1, rPac2, rPac3, rIac1, rIac2, rIac3, \
                                             rUac1, rUac2, rUac3, rPdcTot, rPacTot, \
                                             rEfficiency, rEToday, rETotal, \
                                             rFrequency, rOperatingTime, rFeedInTime, \
                                             rTemperature)], dtype = tipo))
        f.close()
    except FileNotFoundError:
        pass
    return datos

def prodDiaria(dia):
    """
    Proporciona a produción diaria en kWh para unha data determinada.
    O formato do día debe ser '%Y%m%d'
    """
    try:
        nomeArquivo = glob.glob(ruta + d.datetime.strptime(dia, '%Y%m%d').strftime('%Y') + \
                                '/*Spot-' + dia + '.csv')[0]
        producion = lerArquivo(nomeArquivo)['EToday'].max()
    except (IndexError, ValueError):
        producion = 0.
    return producion

def prodMensual(mes):
    """
    Proporciona a produción mensual en kWh para un mes determinado.
    O formato do mes debe ser '%Y%m'
    """
    arquivos = glob.glob(ruta + d.datetime.strptime(mes, '%Y%m').strftime('%Y') + \
                         '/*Spot-' + mes + '*.csv')
    patron = re.compile('.*(?P<dia>' + mes + '\d{2}).*')
    dias = []
    for arq in arquivos:
        r = patron.match(arq)
        if r:
            dias.append(r.group('dia'))
#    mes = d.datetime.strptime(mes, '%Y%m')
#    inicio = mes
#    fin = d.datetime(mes.year, mes.month+1, 1) - d.timedelta(days=1)
#    datas = [(inicio + d.timedelta(days=i)).strftime('%Y%m%d') for i in range((fin-inicio).days + 1)]
    eMensual = 0.
    for dia in dias:
        eMensual += prodDiaria(dia)        
    return eMensual

