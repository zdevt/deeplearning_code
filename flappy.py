#!/usr/bin/python
# -*- coding: utf-8 -*-

#       FileName:  flappy.py
#
#    Description:
#
#        Version:  1.0
#        Created:  2018-05-28 15:01:41
#  Last Modified:  2018-05-28 15:47:27
#       Revision:  none
#       Compiler:  gcc
#
#         Author:  zt ()
#   Organization:

import random
import sys
import pygame

from itertools import cycle
from pygame.locals import *

FPS = 30
SCREENWIDTH = 288
SCREENHEIGHT = 512

PIPEGAPSIZE = 100
BASEY = SCREENHEIGHT * 0.79

(IMAGES, SOUNDS, HITMASKS) = ({ }, { }, { })

PLAYERS_LIST = (('./pic/redbird-upflap.png', './pic/redbird-midflap.png'
                 , './pic/redbird-downflap.png'),
                ('./pic/bluebird-upflap.png',
                 './pic/bluebird-midflap.png',
                 './pic/bluebird-downflap.png'),
                ('./pic/yellowbird-upflap.png',
                 './pic/yellowbird-midflap.png',
                 './pic/yellowbird-downflap.png'))

BACKGROUNDS_LIST = ('./pic/background-day.png',
                    './pic/background-night.png')

PIPES_LIST = ('./pic/pipe-green.png', './pic/pipe-red.png')

try:
    xrange
except NameError:
    print 'NameError'
    xrange = range


def main( ):
    global SCREEN, FPSCLOCK
    pygame.init( )
    FPSCLOCK = pygame.time.Clock( )
    SCREEN = pygame.display.set_mode( (SCREENWIDTH, SCREENHEIGHT) )
    pygame.display.set_caption( 'flappybird zt' )

    IMAGES['numbers'] = (
        pygame.image.load( 'pic/0.png' ).convert_alpha( ),
        pygame.image.load( 'pic/1.png' ).convert_alpha( ),
        pygame.image.load( 'pic/2.png' ).convert_alpha( ),
        pygame.image.load( 'pic/3.png' ).convert_alpha( ),
        pygame.image.load( 'pic/4.png' ).convert_alpha( ),
        pygame.image.load( 'pic/5.png' ).convert_alpha( ),
        pygame.image.load( 'pic/6.png' ).convert_alpha( ),
        pygame.image.load( 'pic/7.png' ).convert_alpha( ),
        pygame.image.load( 'pic/8.png' ).convert_alpha( ),
        pygame.image.load( 'pic/9.png' ).convert_alpha( ),
    )

    IMAGES['gameover'] = pygame.image.load( 'pic/gameover.png' ).convert_alpha( )
    IMAGES['message'] = pygame.image.load( 'pic/message.png' ).convert_alpha( )
    IMAGES['base'] = pygame.image.load( 'pic/base.png' ).convert_alpha( )

    while True:
        randBg = random.randint( 0, len( BACKGROUNDS_LIST ) - 1 )
        IMAGES['background'] = pygame.image.load( BACKGROUNDS_LIST[randBg] ).convert( )

        randPlayer = random.randint( 0, len( PLAYERS_LIST ) - 1 )
        IMAGES['player'] = (
            pygame.image.load( PLAYERS_LIST[randPlayer][0] ).convert_alpha( ),
            pygame.image.load( PLAYERS_LIST[randPlayer][1] ).convert_alpha( ),
            pygame.image.load( PLAYERS_LIST[randPlayer][2] ).convert_alpha( ),
        )

        pipeindex = random.randint( 0, len( PIPES_LIST ) - 1 )
        IMAGES['pipe'] = (
            pygame.transform.rotate( pygame.image.load( PIPES_LIST[pipeindex] ).convert_alpha( ), 180 ),
            pygame.image.load( PIPES_LIST[pipeindex] ).convert_alpha( ),
        )

        HITMASKS['pipe'] = (
            getHitmask( IMAGES['pipe'][0] ),
            getHitmask( IMAGES['pipe'][1] ),
        )

        HITMASKS['player'] = (
            getHitmask( IMAGES['player'][0] ),
            getHitmask( IMAGES['player'][1] ),
            getHitmask( IMAGES['player'][2] ),
        )

        movementInfo = showWelcomeAnimation( )
        crashInfo = mainGame( movementInfo )
        showGameOverScreen( crashInfo )


def showGameOverScreen( data ):
    pass


def showWelcomeAnimation( ):
    pass


def mainGame( data ):
    pass


def getHitmask( data ):
    pass


if __name__ == '__main__':
    main( )
