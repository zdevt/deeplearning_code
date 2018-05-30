#!/usr/bin/python
# -*- coding: utf-8 -*-

#       FileName:  flappy.py
#
#    Description:
#
#        Version:  1.0
#        Created:  2018-05-28 15:01:41
#  Last Modified:  2018-05-30 16:49:44
#       Revision:  none
#       Compiler:  gcc
#
#         Author:  zt ()
#   Organization:

from itertools import cycle
import random
import sys

import pygame
from pygame.locals import *

FPS = 30
SCREENWIDTH = 288
SCREENHEIGHT = 512

PIPEGAPSIZE = 100
BASEY = SCREENHEIGHT * 0.79

(IMAGES, HITMASKS) = ({}, {})

PLAYERS_LIST = (('pic/redbird-upflap.png', 'pic/redbird-midflap.png',
                 'pic/redbird-downflap.png'),
                ('pic/bluebird-upflap.png', 'pic/bluebird-midflap.png',
                 'pic/bluebird-downflap.png'),
                ('pic/yellowbird-upflap.png','pic/yellowbird-midflap.png',
                 'pic/yellowbird-downflap.png'))

BACKGROUNDS_LIST = ('pic/background-day.png', 'pic/background-night.png')

PIPES_LIST = ('pic/pipe-green.png', 'pic/pipe-red.png')

try:
    xrange
except NameError:
    print 'NameError'
    xrange = range


def main():
    global SCREEN, FPSCLOCK
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    pygame.display.set_caption('flappybird zt')

    IMAGES['numbers'] = (
        pygame.image.load('pic/0.png').convert_alpha(),
        pygame.image.load('pic/1.png').convert_alpha(),
        pygame.image.load('pic/2.png').convert_alpha(),
        pygame.image.load('pic/3.png').convert_alpha(),
        pygame.image.load('pic/4.png').convert_alpha(),
        pygame.image.load('pic/5.png').convert_alpha(),
        pygame.image.load('pic/6.png').convert_alpha(),
        pygame.image.load('pic/7.png').convert_alpha(),
        pygame.image.load('pic/8.png').convert_alpha(),
        pygame.image.load('pic/9.png').convert_alpha(),
    )

    IMAGES['gameover'] = pygame.image.load('pic/gameover.png').convert_alpha()
    IMAGES['message'] = pygame.image.load('pic/message.png').convert_alpha()
    IMAGES['base'] = pygame.image.load('pic/base.png').convert_alpha()

    while True:
        randBg = random.randint(0, len(BACKGROUNDS_LIST) - 1)
        IMAGES['background'] = \
            pygame.image.load(BACKGROUNDS_LIST[randBg]).convert()

        randPlayer = random.randint(0, len(PLAYERS_LIST) - 1)

        IMAGES['player'] = \
            (pygame.image.load(PLAYERS_LIST[randPlayer][0]).convert_alpha(),
             pygame.image.load(PLAYERS_LIST[randPlayer][1]).convert_alpha(),
             pygame.image.load(PLAYERS_LIST[randPlayer][2]).convert_alpha())

        pipeindex = random.randint(0, len(PIPES_LIST) - 1)

        IMAGES['pipe'] = \
            (pygame.transform.rotate(pygame.image.load(PIPES_LIST[pipeindex]).convert_alpha(),
             180),
             pygame.image.load(PIPES_LIST[pipeindex]).convert_alpha())

        HITMASKS['pipe'] = (getHitmask(IMAGES['pipe'][0]),
                            getHitmask(IMAGES['pipe'][1]))

        HITMASKS['player'] = (getHitmask(IMAGES['player'][0]),
                              getHitmask(IMAGES['player'][1]),
                              getHitmask(IMAGES['player'][2]))

        movementInfo = showWelcomeAnimation()

        crashInfo = mainGame(movementInfo)

        showGameOverScreen(crashInfo)


def showWelcomeAnimation():
    playerIndex = 0
    playerIndexGen = cycle([0, 1, 2, 1])
    loopIter = 0

    playerx = int(SCREENWIDTH * 0.2)
    playery = int((SCREENHEIGHT - IMAGES['player'][0].get_height()) / 2)

    messagex = int((SCREENWIDTH - IMAGES['message'].get_width()) / 2)
    messagey = int(SCREENHEIGHT * 0.12)

    basex = 0
    baseShift = IMAGES['base'].get_width() - IMAGES['background'].get_width()
    playerShmVals = {'val': 0, 'dir': 1}

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or event.type == KEYDOWN \
                and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE
                                          or event.key == K_UP):
                return {
                    'playery': playery + playerShmVals['val'],
                    'basex': basex,
                    'plyerIndexGen': playerIndexGen
                }

        if (loopIter + 1) % 5 == 0:
            playerIndex = next(playerIndexGen)

        loopIter = (loopIter + 1) % 30
        basex = -((-basex + 4) % baseShift)

        playerShm(playerShmVals)

        SCREEN.blit(IMAGES['background'], (0, 0))
        SCREEN.blit(IMAGES['player'][playerIndex],
                    (playerx, playery + playerShmVals['val']))

        SCREEN.blit(IMAGES['message'], (messagex, messagey))
        SCREEN.blit(IMAGES['base'], (basex, BASEY))

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def mainGame(movementInfo):
    score = playerIndex = loopIter = 0
    playerIndexGen = movementInfo['playerIndexGen']

    (playerx, playery) = (int(SCREENWIDTH * 0.2), movementInfo['playery'])

    basex = movementInfo['basex']
    baseShift = IMAGES['base'].get_width() - IMAGES['background'].getwitdh()

    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    upperPipes = [{
        'x': SCREENWIDTH + 200,
        'y': newPipe1[0]['y']
    }, {
        'x': SCREENWIDTH + 200 + SCREENWIDTH / 2,
        'y': newPipe2[0]['y']
    }]

    lowerPipes = [{
        'x': SCREENWIDTH + 200,
        'y': newPipe1[1]['y']
    }, {
        'x': SCREENWIDTH + 200 + SCREENWIDTH / 2,
        'y': newPipe2[1]['y']
    }]

    pipeVelX = -4

    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1
    playerRot = 45
    playerVelRot = 3
    playerRotThr = 20
    playerFlapAcc = -9
    playerFlapped = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or event.type == KEYDOWN \
                and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE
                                          or event.key == K_UP):
                if playery > -2 * IMAGES['player'][0].get_height():
                    playerVelY = playerFlapAcc
                    playerFlapped = True

        crashTest = checkCrash({
            'x': playerx,
            'y': playery,
            'index': playerIndex
        }, upperPipes, lowerPipes)

        if crashTest[0]:
            return {
                'y': playery,
                'groundCrash': crashTest[1],
                'basex': basex,
                'upperPipes': upperPipes,
                'lowerPipes': lowerPipes,
                'score': score,
                'playerVelY': playerVelY,
                'playerRot': playerRot,
            }

        playerMidPos = playerx + IMAGES['player'][0].get_width() / 2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + IMAGES['pipe'][0].get_width() / 2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                score += 1

        if (loopIter + 1) % 3 == 0:
            playerIndex = next(playerIndexGen)

        loopIter = (loopIter + 1) % 30
        basex = -((-basex + 100) % baseShift)

        if playerRot > -90:
            playerRot -= playerVelRot

        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
            playerFlapped = False

            playerRot = 45

        playerHeight = IMAGES['player'][playerIndex].get_height()
        playery += min(playerVelY, BASEY - playery - playerHeight)

        for (uPipe, lPipe) in zip(upperPipes, lowerPipes):
            uPipe['x'] += pipeVelX
            lPipe['x'] += pipeVelX

        if 0 < upperPipes[0]['x'] < 5:
            newPipe = getRandomPipe()
            upperPipes.append(newPipe[0])
            lowerPipes.append(newPipe[1])

        if upperPipes[0]['x'] < -IMAGES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        SCREEN.blit(IMAGES['background'], (0, 0))

        for (uPipe, lPipe) in zip(upperPipes, lowerPipes):
            SCREEN.blit(IMAGES['pipe'][0], (uPipe['x'], uPipe['y']))
            SCREEN.blit(IMAGES['pipe'][1], (lPipe['x'], lPipe['y']))

        SCREEN.blit(IMAGES['base'], (basex, BASEY))

        showScore(score)

        visibleRot = playerRotThr
        if playerRot <= playerRotThr:
            visibleRot = playerRot

        playerSurface = pygame.transform.rotate(IMAGES['player'][playerIndex],
                                                visibleRot)
        SCREEN.blit(playerSurface, (playerx, playery))

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def showGameOverScreen(crashInfo):
    score = crashInfo['score']
    playerx = SCREENWIDTH * 0.2
    playery = crashInfo['y']
    playerHeight = IMAGES['player'][0].get_height()
    playerVelY = crashInfo['playerVelY']
    playerAccY = 2
    playerRot = crashInfo['playerRot']
    playerVelRot = 7

    basex = crashInfo['basex']

    (upperPipes, lowerPipes) = (crashInfo['upperPipes'],
                                crashInfo['lowerPipes'])

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or event.type == KEYDOWN \
                and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN and (event.key == K_SPACE
                                          or event.key == K_UP):
                if playery + playerHeight >= BASEY - 1:
                    return

        if playery + playerHeight < BASEY - 1:
            player += min(playerVelY, BASEY - playery - playerHeight)

        if playerVelY < 15:
            playerVelY += playerAccY

        if not crashInfo['groundCrash']:
            if playerRot > -90:
                playerRot -= playerVelRot

        SCREEN.blit(IMAGES['background'], (0, 0))

        for (uPipe, lPipe) in zip(upperPipes, lowerPipes):
            SCREEN.blit(IMAGES['pipe'][0], (uPipe['x'], uPipe['y']))
            SCREEN.blit(IMAGES['pipe'][1], (lPipe['x'], lPipe['y']))

        SCREEN.blit(IMAGES['base'], (basex, BASEY))
        showScore(score)

        playerSurface = pygame.transform.rotate(IMAGES['player'][1], playerRot)
        SCREEN.blit(playerSurface, (playerx, playery))

        FPSCLOCK.tick(FPS)
        pygame.display.update()


def playerShm(playerShm):
    if abs(playerShm['val']) == 8:
        playerShm['dir'] *= -1

    if playerShm['dir'] == 1:
        playerShm['val'] += 1
    else:
        playerShm['val'] -= 1


def getRandomPipe():
    gapY = random.randrange(0, int(BASEY * 0.6 - PIPEGAPSIZE))
    gapY += int(BASEY * 0.2)
    pipeHeight = IMAGES['pipe'][0].get_height()
    pipeX = SCREENWIDTH + 10

    return [{
        'x': pipeX,
        'y': gapY - pipeHeight
    }, {
        'x': pipeX,
        'y': gapY + PIPEGAPSIZE
    }]


def showScore(score):
    scoreDigits = [int(x) for x in list(str(score))]
    totalWidth = 0

    for digit in scoreDigits:
        totalWidth += IMAGES['numers'][digit].get_width()

    Xoffset = (SCREENWIDTH - totalWidth) / 2

    for digit in scoreDigits:
        SCREEN.blit(IMAGES['numbers'][digit], (Xoffset, SCREENHEIGHT * 0.1))
        Xoffset += IMAGES['numbers'][digit].get_width()


def checkCrash(player, upperPipes, lowerPipes):
    pi = player['index']
    player['w'] = IMAGES['player'][0].get_width()
    player['h'] = IMAGES['player'][0].get_height()

    if player['y'] + player['h'] >= BASEY - 1:
        return [True, True]
    else:
        playerRect = pygame.Rect(player['x'], player['y'], player['w'],
                                 player['h'])
        pipeW = IMAGES['pipe'][0].get_width()
        pipeH = IMAGES['pipe'][0].get_height()

        for (uPipe, lPipe) in zip(upperPipes, lowerPipes):
            uPipeRect = pygame.Rect(uPipe['x'], uPipe['y'], pipeW, pipeH)
            lPipeRect = pygame.Rect(lPipe['x'], lPipe['y'], pipeW, pipeH)

            pHitMask = HITMASKS['player'][pi]
            uHitmask = HITMASKS['pipe'][0]
            lHitmask = HITMASKS['pipe'][1]

            uCollide = pixelCollision(playerRect, uPipeRect, pHitMask,
                                      uHitmask)
            lCollide = pixelCollision(playerRect, lPipeRect, pHitMask,
                                      lHitmask)

            if uCollide or lCollide:
                return [True, False]

    return [False, False]


def pixelCollision(
        rect1,
        rect2,
        hitmask1,
        hitmask2,
):

    rect = rect1.clip(rect2)

    if rect.width == 0 or rect.height == 0:
        return False

    (x1, y1) = (rect.x - rect1.x, rect.y - rect1.y)
    (x2, y2) = (rect.x - rect2.x, rect.y - rect2.y)

    for x in xrange(rect.width):
        for y in xrange(rect.height):
            if hitmask1[x1 + x][y1 + y] and hitmask2[x2 + x][y2 + y]:
                return True

    return False


def getHitmask(image):
    mask = []
    for x in xrange(image.get_width()):
        mask.append([])
        for y in xrange(image.get_height()):
            mask[x].append(bool(image.get_at((x, y))[3]))
    return mask


if __name__ == '__main__':
    main()
