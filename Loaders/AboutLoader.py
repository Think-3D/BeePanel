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

r"""

AboutLoader Class

This class is responsible for loading the interface components configuration 
from the .json configuration file.

This class exports the following methods:

__init__()            Initializes current class
GetFont(fType,fSyze)    returns pygame font from a given font type and syze
GetButtonList()        returns interface button list
GetLblsText()            returns interface text labels list
GetLblsFont()            returns interface labels font list
GetLblsFontColor()            returns interface labels font color list
GetLblsXPos()            returns interface labels X coordinate list
GetLblsYPos()            returns interface labels Y coordinate list
"""


__author__ = "BVC Electronic Solutions"
__license__ = ""

import json

import BeePanel_Button
import FileFinder
import pygame

class AboutLoader():
    
    interfaceJson = None
    lblsJson = None
    buttonsJson = None
    lblFontColor = None
    lblXPos = None
    lblYPos = None
    lblText = None
    lblFont = None
    
    interfaceButtons = None
    
    txtFields = None
    txtFieldsJson = None
    txtFieldXPos = None
    txtFieldYPos = None
    txtFieldFont = None
    txtFieldFontColor = None
    
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
        
        """
        Load Labels Configuration
        """
        self.lblsJson = []
        self.lblsJson.append(json.loads(json.dumps(self.interfaceJson['Labels'])))
        
        self.lblFontColor = []
        self.lblXPos = []
        self.lblYPos = []
        self.lblText = []
        self.lblFont = []
        for lbls in self.lblsJson:
            lblJson = json.loads(json.dumps(lbls))
            for lbl in lblJson:
                lblFontType = lbl['FontType']
                lblFontSize = int(float(lbl['FontSize'])*self.displayHeight)
                lblFColor = lbl['FontColor']
                self.lblXPos.append(int(float(lbl['X'])*self.displayWidth))
                self.lblYPos.append(int(float(lbl['Y'])*self.displayHeight))
                self.lblText.append(lbl['Text'])
                self.lblFont.append(self.GetFont(lblFontType,lblFontSize))
                
                splitColor = lblFColor.split(",")
                fontColor = pygame.Color(int(splitColor[0]),int(splitColor[1]),int(splitColor[2]))
                self.lblFontColor.append(fontColor)
        
        """
        Load Buttons Configuration
        """
        self.buttonsJson = []
        self.buttonsJson.append(json.loads(json.dumps(self.interfaceJson['Buttons'])))
        
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
            
        """
        Load Text Fields Configuration
        """
        self.txtFieldsJson = []
        self.txtFieldsJson.append(json.loads(json.dumps(self.interfaceJson['TextFields'])))
        
        self.txtFields = []
        self.txtFieldXPos = []
        self.txtFieldYPos = []
        self.txtFieldFont = []
        self.txtFieldFontColor = []
        for tFields in self.txtFieldsJson:
            tFieldsJson = json.loads(json.dumps(tFields))
            for tField in tFieldsJson:
                tFieldFontType = tField['FontType']
                tFieldFontSize = int(float(tField['FontSize'])*self.displayHeight)
                tFieldFColor = tField['FontColor']
                self.txtFieldXPos.append(int(float(tField['X'])*self.displayWidth))
                self.txtFieldYPos.append(int(float(tField['Y'])*self.displayHeight))
                self.txtFieldFont.append(self.GetFont(tFieldFontType, tFieldFontSize))
                
                splitColor = tFieldFColor.split(",")
                fontColor = pygame.Color(int(splitColor[0]),int(splitColor[1]),int(splitColor[2]))
                self.txtFieldFontColor.append(fontColor)
                    
        return
    
    """*************************************************************************
                                GetFont Method 
    
    *************************************************************************"""
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
    
    """*************************************************************************
                                GetButtonsList Method 
    
    *************************************************************************"""
    def GetButtonsList(self):
        r"""
        GetButtonsList method
        
        returns list with interface buttons
        """
        
        return self.interfaceButtons[0]
    
    """*************************************************************************
                                GetLblsText Method 
    
    *************************************************************************"""
    def GetLblsText(self):
        r"""
        GetLblsText method
        
        returns list with interface labels Text
        """
        
        return self.lblText
    
    """*************************************************************************
                                GetLblsFont Method 
    
    *************************************************************************"""
    def GetLblsFont(self):
        r"""
        GetLblsFont method
        
        returns list with interface labels Font
        """
        return self.lblFont
    
    """*************************************************************************
                                GetLblsFontColor Method 
    
    *************************************************************************"""
    def GetLblsFontColor(self):
        r"""
        GetLblsFontColor method
        
        returns list with interface labels Font Color
        """
        return self.lblFontColor
    
    """*************************************************************************
                                GetLblsXPos Method 
    
    *************************************************************************"""
    def GetLblsXPos(self):
        r"""
        GetLblsXPos method
        
        returns list with interface labels X coordinates
        """
        return self.lblXPos
    
    """*************************************************************************
                                GetLblsYPos Method 
    
    *************************************************************************"""
    def GetLblsYPos(self):
        r"""
        GetLblsYPos method
        
        returns list with interface labels Y coordinates
        """
        return self.lblYPos
    
    """*************************************************************************
                                GetTxtFieldsFont Method 
    
    *************************************************************************"""
    def GetTxtFieldsFont(self):
        r"""
        GetTxtFieldsFont method
        
        returns list with interface Text Fields Font
        """
        return self.txtFieldFont
    
    """*************************************************************************
                                GetTxtFieldsFontColor Method 
    
    *************************************************************************"""
    def GetTxtFieldsFontColor(self):
        r"""
        GetTxtFieldsFontColor method
        
        returns list with interface Text Fields Font Color
        """
        return self.txtFieldFontColor
    
    """*************************************************************************
                                GetTxtFieldsXPos Method 
    
    *************************************************************************"""
    def GetTxtFieldsXPos(self):
        r"""
        GetTxtFieldsXPos method
        
        returns list with interface Text Fields X coordinates
        """
        return self.txtFieldXPos
    
    """*************************************************************************
                                GetTxtFieldsYPos Method 
    
    *************************************************************************"""
    def GetTxtFieldsYPos(self):
        r"""
        GetTxtFieldsYPos method
        
        returns list with interface Text Fields Y coordinates
        """
        return self.txtFieldYPos