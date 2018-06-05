#!/usr/bin/env python
#-*- coding:utf-8 -*-
#       FileName:  test.py
#
#    Description:
#
#        Version:  1.0
#        Created:  2018-06-04 14:46:20
#  Last Modified:  2018-06-05 15:13:51
#       Revision:  none
#       Compiler:  gcc
#
#         Author:  zt ()
#   Organization:

import pygame
from pygame.locals import *
from sys import exit

FPS = 10
display_res = (288, 512)

file1 = 'pic/bluebird-upflap.png'
file2 = 'pic/bluebird-midflap.png'
file3 = 'pic/bluebird-downflap.png'

img = []


def test():
    global SCREEN, FPSCLOCK
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    SCREEN = pygame.display.set_mode(display_res)
    pygame.display.set_caption('flappybird zt')

    img.append(pygame.image.load(file1).convert())
    img.append(pygame.image.load(file2).convert())
    img.append(pygame.image.load(file3).convert())
    i = 0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
        i = i + 1
        SCREEN.blit(img[i % 3], (100, 100))
        pygame.display.update()


if __name__ == '__main__':
    test()
