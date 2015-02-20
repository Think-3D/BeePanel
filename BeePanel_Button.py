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
import pygbutton
import FileFinder

class Button():
    
    """
    pygbutton var
    """
    btn = None
    """
    Button Configuration
    """
    buttonWidth = 0
    buttonHeight = 0
    posX = 0
    posY = 0
    bgColor = None
    fontColor = None
    title = ""
    font = None
    normalSurf = None
    downSurf = None
    highlightSurf = None
    name = None
    
    def __init__(self, x = 0, y = 0, width = 0, height = 0, title="", 
                    bgR=0, bgG=0, bgB=0, fR=0, fG = 0, fB = 0,
                    fontType=None, fontSize = 10,
                    normal=None, down=None, highlight=None, name=""):
                        
        self.buttonWidth = width
        self.buttonHeight = height
        self.posX = x
        self.posY = y
        self.title = title
        self.name = name
        
        if (bgR is not None) or (bgG is not None) or (bgB is not None):
            self.bgColor = pygame.Color(bgR,bgG,bgB)
        
        if (fR is not None) or (fG is not None) or (fB is not None):
            self.fontColor = pygame.Color(fR,fG,fB)
        
        ff = FileFinder.FileFinder()
        
        if fontType=="Regular":
            self.font = pygame.font.Font(ff.GetAbsPath("/Fonts/DejaVuSans-Regular.ttf"),fontSize)
        elif fontType=="Bold":
            self.font = pygame.font.Font(ff.GetAbsPath("/Fonts/DejaVuSans-Bold.ttf"),fontSize)
        elif fontType=="Italic":
            self.font = pygame.font.Font(ff.GetAbsPath("/Fonts/DejaVuSans-Italic.ttf"),fontSize)
        elif fontType=="Light":
            self.font = pygame.font.Font(ff.GetAbsPath("/Fonts/DejaVuSans-Light.ttf"),fontSize)
        
        if normal is not None:
            self.normalSurf = ff.GetAbsPath(normal)
        if down is not None:
            self.downSurf = ff.GetAbsPath(down)
        if highlight is not None:
            self.highlightSurf = ff.GetAbsPath(highlight)
        
        
    def GetTextButton(self):
        self.btn = pygbutton.PygButton((self.posX,  self.posY, self.buttonWidth, self.buttonHeight),
                                                self.title, self.bgColor, self.fontColor, self.font,
                                                None,None,None,
                                                self.name)
                                                
        
        #caption='', bgcolor=LIGHTGRAY, fgcolor=BLACK, font=None,
        #normal=None, down=None, highlight=None, bName=None
        
        return self.btn
    
    def GetImageButton(self):
        
        self.btn = pygbutton.PygButton((self.posX,  self.posY, self.buttonWidth, self.buttonHeight),
                                                None, None, None, None,
                                                self.normalSurf, self.downSurf, self.highlightSurf,
                                                self.name)
        
        return self.btn
