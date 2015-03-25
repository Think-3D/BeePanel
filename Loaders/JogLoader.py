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

import BeePanel_Button
import FileFinder
import pygame

class JogLoader():
    
    interfaceJson = None
    lblJson = None
    ButtonsJson = None
    
    lblFont = None
    lblFontColor = None
    lblXPos = None
    lblYPos = None
    
    interfaceButtons = []
    
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
        self.lblJson = json.loads(json.dumps(self.interfaceJson['TopLabel']))
        self.ButtonsJson = json.loads(json.dumps(self.interfaceJson['Buttons']))
        
        lblFontType = self.lblJson['FontType']
        lblFontSize = int(float(self.lblJson['FontSize'])*self.displayHeight)
        lblFColor = self.lblJson['lblFontColor']
        self.lblXPos = int(float(self.lblJson['X'])*self.displayWidth)
        self.lblYPos = int(float(self.lblJson['Y'])*self.displayHeight)
        
        self.lblFont = self.GetFont(lblFontType,lblFontSize)
        
        splitColor = lblFColor.split(",")
        self.lblFontColor = pygame.Color(int(splitColor[0]),int(splitColor[1]),int(splitColor[2]))
        
        
        for btn in self.ButtonsJson:
            btnX = int(float(btn['X'])*self.displayWidth)
            btnY = int(float(btn['Y'])*self.displayHeight)
            btnWidth = int(float(btn['Width'])*self.displayWidth)
            btnHeight = int(float(btn['Height'])*self.displayHeight)
            btnType = btn['ButtonType']
            
            if btnType == "Text":
                btnTitle = btn['Title']
                bgColor = btn['bgColor'].split(",")
                fColor = btn['FontColor'].split(",")
                fType = btn['FontType']
                fSize = int(float(btn['FontSize'])*self.displayHeight)
                btnName = btn['ButtonName']
                
                jogBtn = BeePanel_Button.Button(btnX,btnY,btnWidth,btnHeight,btnTitle,
                                                int(bgColor[0]),int(bgColor[2]),int(bgColor[2]),
                                                int(fColor[0]),int(fColor[2]),int(fColor[2]),
                                                fType,fSize, None, None, None, btnName)
                newBtn = jogBtn.GetTextButton()
                newBtn._propSetName(btnTitle)
                self.interfaceButtons.append(newBtn)
            elif btnType == "Img":
                btnTitle = btn['Title']
                normalPath = btn['NormalPath']
                downPath = btn['DownPath']
                highlightedPath = btn['HighlightedPath']
                btnName = btn['ButtonName']
                
                jogBtn = BeePanel_Button.Button(btnX,btnY,btnWidth,btnHeight,None,
                                                None,None,None,None,None,None,
                                                None,None,
                                                normalPath,downPath,highlightedPath,
                                                btnName)
                newBtn = jogBtn.GetImageButton()
                newBtn._propSetName(btnTitle)
                self.interfaceButtons.append(newBtn)
                
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
    GetButtonsList(self)
    
    returns the list with the jog buttons
    """
    def GetButtonsList(self):
        
        return self.interfaceButtons
    
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
    