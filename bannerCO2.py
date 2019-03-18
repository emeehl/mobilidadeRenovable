#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pygame
from co2equiv import obterDatos

def xeneraBannerPNG(textos):
    pygame.init()
    
    display_width = 640
    display_height = 400
      
    gameDisplay = pygame.display.set_mode((display_width,display_height))
    pygame.display.set_caption('')
    
    def text_objects(text, font):
        textSurface = font.render(text, True, verde)
        return textSurface, textSurface.get_rect()
    
    def message_display(text, xy, deltaXY, size=32):
        x, y = xy; deltaX, deltaY = deltaXY
        largeText = pygame.font.Font('freesansbold.ttf',size)
        TextSurf, TextRect = text_objects(text, largeText)
        TextRect.center = (x + deltaX, y + deltaY)
        gameDisplay.blit(TextSurf, TextRect)
        pygame.display.update()

    black = (0,0,0)
#    white = (255,255,255)
    verde = (145, 220, 90)  #0x91DC5A
    
    textoPanel = textos['inversor']; textoIndustria = textos['eIndustria']
    textoCoche = textos['eCoche']; textoArbol = textos['arbol']
    
    # Icones tirados de flaticon.com, author: surang
    banner = pygame.image.load('iconos/banner.png')
    gameDisplay.fill(black)
    delta = (0,0); tipoGrande = 48; tipoMedio = 28
    gameDisplay.blit(banner, delta)
    message_display(textoPanel, (350, 120), delta, tipoGrande)
    message_display(textoIndustria, (90, 340), delta, tipoMedio)
    message_display(textoCoche, (270, 340), delta, tipoMedio)
    message_display(textoArbol, (510, 340), delta, tipoMedio)
    
    pygame.display.update()
    pygame.image.save(gameDisplay, 'co2evitado.png')
    
    pygame.quit()
    
if __name__ == "__main__":
    textoIndustria = '50 t CO2'
    textoFuel = '20 t CO2'
    textoCoche = '30000 km'
    textoArbol = u'5000 árboles'
    textoBateria = '30 MWh'
#    textos = [textoIndustria, textoFuel, textoCoche, textoArbol, textoBateria]
    textos = {'inversor': textoBateria, 'eIndustria': textoIndustria,
              'eCoche': textoCoche,     'arbol': textoArbol}
    
#    xeneraBannerPNG(textos)
    xeneraBannerPNG(obterDatos())
    
#quit()
