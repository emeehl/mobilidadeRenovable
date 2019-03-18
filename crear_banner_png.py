#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pygame

def xeneraBannerPNG(textos):
    pygame.init()
    
    display_width = 600
    display_height = 360
    
    gameDisplay = pygame.display.set_mode((display_width,display_height))
    pygame.display.set_caption('')
    
    def text_objects(text, font):
        textSurface = font.render(text, True, verde)
        return textSurface, textSurface.get_rect()
    
    def message_display(text, xy, deltaXY):
        x, y = xy; deltaX, deltaY = deltaXY
        largeText = pygame.font.Font('freesansbold.ttf',32)
        TextSurf, TextRect = text_objects(text, largeText)
        TextRect.center = (x + deltaX, y + deltaY)
        gameDisplay.blit(TextSurf, TextRect)
        pygame.display.update()

    black = (0,0,0)
    white = (255,255,255)
    verde = (145, 220, 90)  #0x91DC5A
    
    # Icones tirados de flaticon.com, author: surang
    posX = 60; posY = 40; dX = 230; dY = 155
    bateria = pygame.image.load('iconos/battery.png'); posBateria = (posX + 1.8*dX, posY + dY/1.8)
    industria = pygame.image.load('iconos/factory.png'); posIndustria = (posX, posY)
    fuel = pygame.image.load('iconos/surtidor.png'); posFuel = (posX + dX, posY)
    coche = pygame.image.load('iconos/electric-car.png'); posCoche = (posX, posY + dY)
    arbol = pygame.image.load('iconos/tree.png'); posArbol = (posX + dX, posY + dY)
    
    gameDisplay.fill(black)
    gameDisplay.blit(industria, posIndustria)
    gameDisplay.blit(fuel, posFuel)
    gameDisplay.blit(coche, posCoche)
    gameDisplay.blit(arbol, posArbol)
    gameDisplay.blit(bateria, posBateria)
    
    delta = (40, 100)
    message_display(textoIndustria, posIndustria, delta)
    message_display(textoFuel, posFuel, delta)
    message_display(textoCoche, posCoche, delta)
    message_display(textoArbol, posArbol, delta)
    message_display(textoBateria, posBateria, delta)
    
    pygame.display.update()
    pygame.image.save(gameDisplay, 'co2evitado.png')
    
    pygame.quit()
    
if __name__ == "__main__":
    textoIndustria = '50 t CO2'
    textoFuel = '20 t CO2'
    textoCoche = '30000 km'
    textoArbol = u'5000 árboles'
    textoBateria = '30 MWh'
    textos = [textoIndustria, textoFuel, textoCoche, textoArbol, textoBateria]
    
    xeneraBannerPNG(textos)
    
#quit()
