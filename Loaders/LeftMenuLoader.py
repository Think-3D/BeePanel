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

class LeftMenuLoader():
    
    interfaceButtonsData = None
    carouselButtons = None
    
    carouselItems = None
    carouselX = None
    carouselY = None
    carouselWidth = None
    carouselHeight = None
    carouselButtonHeight = None
    
    buttonNames = None
    buttonTitles = None
    bgColor = None
    font = None
    fontType = None
    fontSize = None
    fontColor = None
    bgR = None
    bgG = None
    bgB = None
    fR = None
    fG = None
    Fb = None
    
    displayWidth = 480
    displayHeight = 320
    
    """*************************************************************************
                                Init Method 
    
    Inits current screen components
    *************************************************************************"""
    def __init__(self, jsonData, dispWidth, dispHeight):
        
        self.displayWidth = dispWidth
        self.displayHeight = dispHeight
        
        carouselJson = json.loads(json.dumps(jsonData['Carousel']))[0]
        carouselButtonsJson = carouselJson['Buttons']
        carouselConfigJson = carouselJson['Configuration']
        
        """
        Carousel Config
        """
        self.carouselItems = int(carouselConfigJson['CarouselItems'])
        self.carouselX = int(float(carouselConfigJson['X'])*self.displayWidth)
        self.carouselY = int(float(carouselConfigJson['Y'])*self.displayHeight)
        self.carouselWidth = int(float(carouselConfigJson['Width'])*self.displayWidth)
        self.carouselHeight = int(float(carouselConfigJson['Height'])*self.displayHeight)
        self.carouselButtonHeight = int(float(carouselConfigJson['ButtonHeight'])*self.displayHeight)
        
        bgColor = carouselConfigJson['bgColor']
        splitColor = bgColor.split(",")
        self.bgR = int(splitColor[0])
        self.bgG = int(splitColor[1])
        self.bgB = int(splitColor[2])
        self.bgColor = pygame.Color(self.bgR,self.bgG,self.bgB)
        
        self.fontType = carouselConfigJson['FontType']
        self.fontSize = int(float(carouselConfigJson['FontSize'])*self.displayHeight)
        self.font = self.GetFont(self.fontType,self.fontSize)
        
        fColor = carouselConfigJson['FontColor']
        splitColor = fColor.split(",")
        self.fR = int(splitColor[0])
        self.fG = int(splitColor[1])
        self.fB = int(splitColor[2])
        self.fontColor = pygame.Color(self.fR,self.fG,self.fB)
        
        self.carouselButtons = []
        for btn in carouselButtonsJson:
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
                self.carouselButtons.append(newBtn)
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
                self.carouselButtons.append(newBtn)
            
            
        leftButtons = jsonData['leftMenuButtons']
        self.buttonNames = []
        self.buttonTitles = []
        for btn in leftButtons:
            btnJson = json.loads(json.dumps(btn))
            title = btnJson['Title']
            btnName = btn['ButtonName']
            self.buttonNames.append(btnName)
            self.buttonTitles.append(title)
        
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
    GetCarouselButtons(self)
    
    
    """
    def GetCarouselButtons(self):
        
        return self.carouselButtons
    
    """
    GetCarouselItems(self)
    
    
    """
    def GetCarouselItems(self):
        
        return self.carouselItems
    
    """
    GetCarouselX(self)
    
    
    """
    def GetCarouselX(self):
        
        return self.carouselX
    
    """
    GetCarouselY(self)
    
    
    """
    def GetCarouselY(self):
        
        return self.carouselY
    
    """
    GetCarouselWidth(self)
    
    
    """
    def GetCarouselWidth(self):
        
        return self.carouselWidth
    
    """
    GetCarouselHeight(self)
    
    
    """
    def GetCarouselHeight(self):
        
        return self.carouselHeight
    
    """
    GetCarouselButtonHeight(self)
    
    
    """
    def GetCarouselButtonHeight(self):
        
        return self.carouselButtonHeight
    
    """
    GetCarouselButtonNames(self)
    
    
    """
    def GetCarouselButtonNames(self):
        
        return self.buttonNames
    
    """
    GetCarouselButtonTitles(self)
    
    
    """
    def GetCarouselButtonTitles(self):
        
        return self.buttonTitles
    
    """
    GetCarouselBgColor(self)
    
    
    """
    def GetCarouselBgColor(self):
        
        return self.bgColor
    
    """
    GetCarouselFontColor(self)
    
    
    """
    def GetCarouselFontColor(self):
        
        return self.fontColor
    
    """
    GetCarouselFont(self)
    
    
    """
    def GetCarouselFont(self):
        
        return self.font
    
    """
    GetCarouselFontType(self)
    
    
    """
    def GetCarouselFontType(self):
        
        return self.fontType
    
    """
    GetCarouselFontSize(self)
    
    
    """
    def GetCarouselFontSize(self):
        
        return self.fontSize
    
    """
    Individual Color Codes
    
    
    """
    def GetBgR(self):
        return self.bgR
    def GetBgG(self):
        return self.bgG
    def GetBgB(self):
        return self.bgB
    
    def GetFR(self):
        return self.fR
    def GetFG(self):
        return self.fG
    def GetFB(self):
        return self.fB