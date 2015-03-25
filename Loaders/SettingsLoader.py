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

class SettingsLoader():
    
    interfaceJson = None
    lblsJson = None
    buttonsJson = None
    lblFontColor = None
    lblXPos = None
    lblYPos = None
    lblText = None
    lblFont = None
    
    interfaceButtons = None
    
    displayWidth = 480
    displayHeight = 320
    
    """*************************************************************************
                                Init Method 
    
    Inits current screen components
    *************************************************************************"""
    def __init__(self, interfaceJson, dispWidth, dispHeight):
        r"""
        __init__ method
        
        Initialization method. Loads configurations from the json file
        """
        
        self.displayWidth = dispWidth
        self.displayHeight = dispHeight
        
        self.interfaceJson = interfaceJson
        
        self.lblsJson = []
        self.buttonsJson = []
        self.lblFontColor = []
        self.lblXPos = []
        self.lblYPos = []
        self.lblText = []
        self.lblFont = []
        
        self.lblsJson.append(json.loads(json.dumps(self.interfaceJson['Labels'])))
        self.buttonsJson.append(json.loads(json.dumps(self.interfaceJson['Buttons'])))
        
        """
        Load Labels Configuration
        """
        for lbls in self.lblsJson:
            lblJson = json.loads(json.dumps(lbls))
            for lbl in lblJson:
                lblFontType = lbl['FontType']
                lblFontSize = int(float(lbl['FontSize'])*self.displayHeight)
                lblFColor = lbl['FontColor']
                self.lblXPos.append(int(float(lbl['X']))*self.displayWidth)
                self.lblYPos.append(int(float(lbl['Y']))*self.displayHeight)
                self.lblText.append(lbl['Text'])
                self.lblFont.append(self.GetFont(lblFontType,lblFontSize))
                
                splitColor = lblFColor.split(",")
                fontColor = pygame.Color(int(splitColor[0]),int(splitColor[1]),int(splitColor[2]))
                self.lblFontColor.append(fontColor)
        
        """
        Load Buttons Configuration
        """
        self.interfaceButtons = []
        for btns in self.buttonsJson:
            filButtons = []
            for btn in btns:
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
                                                fType,fSize,None,None,None,btnName)
                                                
                    newBtn = jogBtn.GetTextButton()
                    newBtn._propSetName(btnTitle)
                    filButtons.append(newBtn)
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
                    filButtons.append(newBtn)
        
            self.interfaceButtons.append(filButtons)
            
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
    
    returns the list with buttons
    """
    def GetButtonsList(self):
        
        return self.interfaceButtons[0]
    
    """
    GetLblsText
    """
    def GetLblsText(self):
        return self.lblText
    
    """
    GetLblsFont
    """
    def GetLblsFont(self):
        return self.lblFont
    
    """
    GetLblsFontColor
    """
    def GetLblsFontColor(self):
        return self.lblFontColor
    
    """
    GetLblsXPos
    """
    def GetLblsXPos(self):
        return self.lblXPos
    
    """
    GetLblsYPos
    """
    def GetLblsYPos(self):
        return self.lblYPos