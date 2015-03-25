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

CalibrationLoader Class

This class is responsible for loading the interface components configuration 
from the .json configuration file.

This class exports the following methods:

__init__()            Initializes current class
GetFont(fType,fSyze)    returns pygame font from a given font type and syze
GetLeftButtonList()        returns interface button list
GetLblsFont()            returns interface labels font list
GetLblsFontColor()            returns interface labels font color list
GetLblsXPos()            returns interface labels X coordinate list
GetLblsYPos()            returns interface labels Y coordinate list
GetLeftImagePath()        returns left image path
GetRightImagePath()        returns right image path
GetLeftImgX()        returns left image X coordinate
GetLeftImgY()        returns left image Y coordinate
GetRightImgX()        returns right image X coordinate
GetRightImgY()        returns right image Y coordinate
"""


__author__ = "BVC Electronic Solutions"
__license__ = ""

import json

import BeePanel_Button
import FileFinder
import pygame

class CalibrationLoader():
    
    interfaceJson = None
    lblJson = []
    buttonsJson = []
    
    lblFont = []
    lblFontColor = []
    lblXPos = []
    lblYPos = []
    
    interfaceButtons = []
    
    leftImgJson = None
    rightImgJson = None
    leftImgPath = None
    rightImgPath = None
    leftImgX = 100
    rightImgX = 100
    sliceImgY = 0
    rightImgY = 0
    
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
        
        ff = FileFinder.FileFinder()
        
        self.interfaceJson = interfaceJson
        
        self.lblJson.append(json.loads(json.dumps(self.interfaceJson['FirstLabel'])))
        self.lblJson.append(json.loads(json.dumps(self.interfaceJson['SecondLabel'])))
        self.lblJson.append(json.loads(json.dumps(self.interfaceJson['ThirdLabel'])))
        
        self.buttonsJson.append(json.loads(json.dumps(self.interfaceJson['FirstButtons'])))
        self.buttonsJson.append(json.loads(json.dumps(self.interfaceJson['SecondButtons'])))
        self.buttonsJson.append(json.loads(json.dumps(self.interfaceJson['ThirdButtons'])))
        
        self.leftImgJson = json.loads(json.dumps(self.interfaceJson['LeftBoltImg']))[0]
        self.rightImgJson = json.loads(json.dumps(self.interfaceJson['RightBoltImg']))[0]
        
        
        for lbl in self.lblJson:
            lblFontType = lbl['FontType']
            lblFontSize = int(float(lbl['FontSize'])*self.displayHeight)
            lblFColor = lbl['lblFontColor']
            self.lblXPos.append(int(float(lbl['X'])*self.displayWidth))
            self.lblYPos.append(int(float(lbl['Y'])*self.displayHeight))
            
            self.lblFont.append(self.GetFont(lblFontType,lblFontSize))
            
            splitColor = lblFColor.split(",")
            fontColor = pygame.Color(int(splitColor[0]),int(splitColor[1]),int(splitColor[2]))
            self.lblFontColor.append(fontColor)
            
        for btns in self.buttonsJson:
            calButtons = []
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
                                                fType,fSize, None, None, None, btnName)
                                                
                    newBtn = jogBtn.GetTextButton()
                    newBtn._propSetName(btnTitle)
                    calButtons.append(newBtn)
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
                    calButtons.append(newBtn)
        
            self.interfaceButtons.append(calButtons)
            
        """
        Image Files Configuration
        """
        self.leftImgPath = ff.GetAbsPath(self.leftImgJson['ImgPath'])
        self.rightImgPath = ff.GetAbsPath(self.rightImgJson['ImgPath'])
        self.leftImgX = int(float(self.leftImgJson['X'])*self.displayWidth)
        self.leftImgY = int(float(self.leftImgJson['Y'])*self.displayHeight)
        self.rightImgX = int(float(self.rightImgJson['X'])*self.displayWidth)
        self.rightImgY = int(float(self.rightImgJson['Y'])*self.displayHeight)
            
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
    def GetButtonsList(self,calibrationState):
        r"""
        GetLeftButtonsList method
        
        returns buttons list for the selected interface state
        
        arguments:
            calibrationState - interface state
            
        returns:
            buttons list
        """
        
        return self.interfaceButtons[calibrationState]
    
    """*************************************************************************
                                GetlblFont Method 
    
    *************************************************************************"""
    def GetlblFont(self,calibrationState):
        r"""
        GetlblFont method
        
        returns label font list for the selected interface state
        
        arguments:
            calibrationState - interface state
            
        returns:
            labels font list
        """
        return self.lblFont[calibrationState]
    
    """*************************************************************************
                                GetlblFontColor Method 
    
    *************************************************************************"""
    def GetlblFontColor(self,calibrationState):
        r"""
        GetlblFontColor method
        
        returns label font color list for the selected interface state
        
        arguments:
            calibrationState - interface state
            
        returns:
            labels font color list
        """
        return self.lblFontColor[calibrationState]
    
    
    """*************************************************************************
                                GetlblXPos Method 
    
    *************************************************************************"""
    def GetlblXPos(self,calibrationState):
        r"""
        GetlblXPos method
        
        returns label x coordinates list for the selected interface state
        
        arguments:
            calibrationState - interface state
            
        returns:
            labels x coordinate list
        """
        return self.lblXPos[calibrationState]
    
    
    """*************************************************************************
                                GetlblYPos Method 
    
    *************************************************************************"""
    def GetlblYPos(self,calibrationState):
        r"""
        GetlblYPos method
        
        returns label Y coordinates list for the selected interface state
        
        arguments:
            calibrationState - interface state
            
        returns:
            labels Y coordinate list
        """
        return self.lblYPos[calibrationState]
    
    
    """*************************************************************************
    ****************************IMAGES******************************************
    *************************************************************************"""
    
    """*************************************************************************
                                GetLeftImgPath Method 
    
    *************************************************************************"""
    def GetLeftImgPath(self):
        r"""
        GetLeftImgPath method
        
        returns left image path
        """
        return self.leftImgPath
    
    """*************************************************************************
                                GetRightImgPath Method 
    
    *************************************************************************"""
    def GetRightImgPath(self):
        r"""
        GetRightImgPath method
        
        returns right image path
        """
        return self.rightImgPath
    
    
    """*************************************************************************
                                GetLeftImgX Method 
    
    *************************************************************************"""
    def GetLeftImgX(self):
        r"""
        GetLeftImgX method
        
        returns left image X coordinate
        """
        return self.leftImgX
    
    """*************************************************************************
                                GetLeftImgY Method 
    
    *************************************************************************"""
    def GetLeftImgY(self):
        r"""
        GetLeftImgY method
        
        returns left image Y coordinate
        """
        return self.leftImgY
    
    """*************************************************************************
                                GetRightImgX Method 
    
    *************************************************************************"""
    def GetRightImgX(self):
        r"""
        GetRightImgX method
        
        returns Right image X coordinate
        """
        return self.rightImgX
    
    """*************************************************************************
                                GetRightImgY Method 
    
    *************************************************************************"""
    def GetRightImgY(self):
        r"""
        GetRightImgY method
        
        returns Right image Y coordinate
        """
        return self.rightImgY