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

class Display():
    
    """
    Display Configuration
    """
    display = []
    displayWidth = 0
    displayHeight = 0
    displayType = ""
    
    """
    Display Appearence
    """
    bgColor = None
    splitLineX = 100
    lineColor = None
    lineThickness = 3
    
    def __init__(self, type="Adafruit PiTFT Resistive", width=320, height=240,
                        bgColor="255,255,255",linePos=100, lineColor="0,0,0", lineThickness=3):
        self.displayWidth = width
        self.displayHeight = height
        self.displayType = type
        self.splitLineX = linePos
        self.lineThickness = lineThickness
        
        bgColorSplit=bgColor.split(",")
        bgR = int(bgColorSplit[0])
        bgG = int(bgColorSplit[1])
        bgB = int(bgColorSplit[2])
        
        self.bgColor = pygame.Color(bgR,bgG,bgB)
        
        lineColorSplit=lineColor.split(",")
        lR = int(lineColorSplit[0])
        lG = int(lineColorSplit[1])
        lB = int(lineColorSplit[2])
        
        self.lineColor = pygame.Color(lR,lG,lB)
    
    
    """
    GetBEEScreen(self)
    
    returns the screen object with the configured dimensions
    """
    def GetBEEScreen(self):
        screen = pygame.display.set_mode((self.displayWidth,self.displayHeight))
        
        return screen
    
    """
    GetbgColor(self)
    
    returns pygame.Color object with the Background color
    """
    def GetbgColor(self):
        
        return self.bgColor
    
    """
    GetLineColor(self)
    
    returns pygame.Color object with the Split Line color
    """
    def GetLineColor(self):
        
        return self.lineColor
    
    """
    DrawLine(self)
    
    Draws the split line
    """
    def DrawLine(self,screen):
        pygame.draw.line(screen, self.lineColor,
                                (self.splitLineX, 0),
                                (self.splitLineX, self.displayHeight),
                                self.lineThickness)
        return