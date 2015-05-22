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

import json

import FileFinder
import pygame

class PrinterInfoLoader():
    
    interfaceJson = None
    
    lblJson = None
    lblValJson = None
    
    lblFont = None
    lblFontColor = None
    lblXPos = None
    lblYPos = None
    lblText = None
    
    lblValFont = None
    lblValFontColor = None
    
    lblValXPos = None
    lblValFont = None
    lblValFontColor = None
    
    displayWidth = 480
    displayHeight = 320
    
    """*************************************************************************
                                Init Method 
    
    Inits current screen components
    *************************************************************************"""
    def __init__(self, interfaceJson, dispWidth, dispHeight):
        
        self.displayWidth = dispWidth
        self.displayHeight = dispHeight
        
        self.interfaceJson = interfaceJson
        
        
        self.lblJson = json.loads(json.dumps(self.interfaceJson['Labels']))
        self.lblValJson = json.loads(json.dumps(self.interfaceJson['ValuesSettings']))
        
        """
        Values Labels Configuration
        
        "X":"220",
                    "FontType":"Bold",
                    "FontSize":"12",
                    "FontColor":"0,0,0"
        """
        self.lblValXPos = int(float(self.lblValJson['X'])*self.displayWidth)
        lblValFontType = self.lblValJson['FontType']
        lblValFontSize = int(float(self.lblValJson['FontSize'])*self.displayHeight)
        self.lblValFont = self.GetFont(lblValFontType,lblValFontSize)
        lblValFColor = self.lblValJson['FontColor']
        splitColor = lblValFColor.split(",")
        self.lblValFontColor = pygame.Color(int(splitColor[0]),int(splitColor[1]),int(splitColor[2]))
        
        """
        Load Labels Configuration
        """
        self.lblText = []
        self.lblXPos = []
        self.lblYPos = []
        self.lblFont = []
        self.lblFontColor = []
        
        for lbl in self.lblJson:
            lblFontType = lbl['FontType']
            lblFontSize = int(float(lbl['FontSize'])*self.displayHeight)
            lblFColor = lbl['FontColor']
            
            self.lblXPos.append(int(float(lbl['X'])*self.displayWidth))
            self.lblYPos.append(int(float(lbl['Y'])*self.displayHeight))
            self.lblText.append(lbl['Text'])
            
            font = self.GetFont(lblFontType,lblFontSize)
            
            self.lblFont.append(font)
            
            splitColor = lblFColor.split(",")
            fontColor = pygame.Color(int(splitColor[0]),int(splitColor[1]),int(splitColor[2]))
            self.lblFontColor.append(fontColor)
        
        return
    
    """
    GetFont
    """
    def GetFont(self,fontType,fontSize):
        r"""
        GetFont method
        
        Receives as arguments:
            fontType - Regular,Bold,Italic,Light
            fontSize - font size
        
        Returns:
            pygame font object
        """
        
        ff = FileFinder.FileFinder()
        
        font = None
        if fontType == "Regular":
            font = pygame.font.Font(ff.GetAbsPath("/Fonts/DejaVuSans-Regular.ttf"),fontSize)
        elif fontType == "Bold":
            font = pygame.font.Font(ff.GetAbsPath("/Fonts/DejaVuSans-Bold.ttf"),fontSize)
        elif fontType == "Italic":
            font = pygame.font.Font(ff.GetAbsPath("/Fonts/DejaVuSans-Italic.ttf"),fontSize)
        elif fontType == "Light":
            font = pygame.font.Font(ff.GetAbsPath("/Fonts/DejaVuSans-Light.ttf"),fontSize)
            
        return font
    
    """
    GetlblText(self)
    
    returns the list with the label text
    """
    def GetlblText(self):
        return self.lblText
    
    """
    GetlblFont
    """
    def GetlblFont(self):
        return self.lblFont
    
    """
    GetlblFontColor
    """
    def GetlblFontColor(self):
        return self.lblFontColor
    
    
    """
    GetlblXPos
    """
    def GetlblXPos(self):
        return self.lblXPos
    
    """
    GetlblYPos
    """
    def GetlblYPos(self):
        return self.lblYPos
    
    """
    GetlblValFont
    """
    def GetlblValFont(self):
        return self.lblValFont
    
    """
    GetlblValFontColor
    """
    def GetlblValFontColor(self):
        return self.lblValFontColor
    
    
    """
    GetlblValXPos
    """
    def GetlblValXPos(self):
        return self.lblValXPos