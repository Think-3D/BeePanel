#!/usr/bin/env python3

"""
* Copyright (c) 2015 BEEVC - Electronic Systems This file is part of BEESOFT
* software: you can redistribute it and/or modify it under the terms of the GNU
* General Public License as published by the Free Software Foundation, either
* version 3 of the License, or (at your option) any later version. BEESOFT is
* distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
* without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
* PARTICULAR PURPOSE. See the GNU General Public License for more details. You
* should have received a copy of the GNU General Public License along with
* BEESOFT. If not, see <http://www.gnu.org/licenses/>.
"""

__author__ = "Marcos Gomes"
__license__ = "MIT"

import pygame
import math

class ProgressBar():
    
    x = 0
    y = 0
    width = 0
    height = 0
    thickness = 0
    
    lineColor = None
    fillColor = None
    
    rect = None
    
    """*************************************************************************
                                Init Method 
    
    Inits current screen components
    *************************************************************************"""
    def __init__(self, x, y, width, height, lineColor, fillColor,thickness):
        
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.lineColor = lineColor
        self.fillColor = fillColor
        self.thickness = thickness
        
        
        return
    
    """
    GetRect
    """
    def DrawRect(self,screen):
        
        self.rect = pygame.draw.rect(screen, 
                                    self.lineColor,
                                    (self.x,self.y,self.width,self.height),
                                    self.thickness)
        
        return
    
    """
    GetRect
    """
    def GetSurface(self,fillWidth, maxFill):
        
        surf = None
        
        if(maxFill == 0):
            surf = pygame.Surface((0,self.height))
        else:
            if(fillWidth <= 0):
                surf = pygame.Surface((0,self.height))
            else:
                fill = math.ceil(fillWidth*self.width/maxFill)
                surf = pygame.Surface((int(fill),self.height))
        
        surf.fill(self.fillColor)
        
        #fillWidth = int((self.nozzleTemperature/self.targetTemperature)*width)
            
            #self.temperatureBarRect = pygame.draw.rect(self.screen, fontColor, (x,y,width,height), 3)
            #self.temperatureBarSurf = pygame.Surface((fillWidth,height))
            #self.temperatureBarSurf.fill(fontColor)
            #self.screen.blit(self.temperatureBarSurf, (x,y))
        return surf
    
    """
    GetPos
    """
    def GetPos(self):
        return (self.x,self.y)