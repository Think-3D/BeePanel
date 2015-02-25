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

class WaitForConnectionLoader():
    
    jsonPath = "/Json/WaitForConnectionConfiguration.json"
    
    interfaceJson = None
    
    lblsJson = None
    lblFontColor = None
    lblXPos = None
    lblYPos = None
    lblText = None
    lblFont = None
    
    imgJson = None
    imagePath = None
    imageX = None
    imageY = None
    
    """*************************************************************************
                                Init Method 
    
    Inits current screen components
    *************************************************************************"""
    def __init__(self):
        
        ff = FileFinder.FileFinder()
        
        """
        Get wait screen Configuration
        """
        f = open(ff.GetAbsPath(self.jsonPath),'r')                          #load json as text file
        self.interfaceJson = json.load(f)                                     #parse the json file
        
        self.wait4connectionJson = self.interfaceJson['WaitForConnection'][0]
        
        self.lblsJson = []
        self.lblFontColor = []
        self.lblXPos = []
        self.lblYPos = []
        self.lblText = []
        self.lblFont = []
        
        self.lblsJson.append(json.loads(json.dumps(self.wait4connectionJson['Labels'])))
        self.imgJson = json.loads(json.dumps(self.wait4connectionJson['Image']))
        
        """
        Load Labels Configuration
        """
        for lbls in self.lblsJson:
            lblJson = json.loads(json.dumps(lbls))
            for lbl in lblJson:
                lblFontType = lbl['FontType']
                lblFontSize = int(lbl['FontSize'])
                lblFColor = lbl['FontColor']
                self.lblXPos.append(int(lbl['X']))
                self.lblYPos.append(int(lbl['Y']))
                self.lblText.append(lbl['Text'])
                self.lblFont.append(self.GetFont(lblFontType,lblFontSize))
                
                splitColor = lblFColor.split(",")
                fontColor = pygame.Color(int(splitColor[0]),int(splitColor[1]),int(splitColor[2]))
                self.lblFontColor.append(fontColor)
        
        """
        Loade Image Configurtation
        """
        self.imagePath = ff.GetAbsPath(self.imgJson['ImgPath'])
        self.imageX = int(self.imgJson['X'])
        self.imageY = int(self.imgJson['Y'])
        
        f.close()
        
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
    
    """
    GetImagePath
    """
    def GetImagePath(self):
        return self.imagePath    
    """
    GetImageX
    """
    def GetImageX(self):
        return self.imageX
    
    """
    GetImageY
    """
    def GetImageY(self):
        return self.imageY