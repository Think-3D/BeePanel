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
import ProgressBar
import pygame

class PrintingLoader():
    
    interfaceJson = None
    
    interfacelabels = None
    lblsJson = None
    lblFontColor = None
    lblXPos = None
    lblYPos = None
    lblText = None
    lblFont = None 
    lblIndexes = None
    
    timeLblFontColor = None
    timeLblXPos = None
    timeLblYPos = None
    timeLblText = None
    timeLblFont = None
    
    colorLblFontColor = None
    colorLblXPos = None
    colorLblYPos = None
    colorLblText = None
    colorLblFont = None 
    
    buttonsJson = None
    interfaceButtons = None
    
    images = None
    imagesJson = None
    imagePath = None
    imageX = None
    imageY = None
    
    #Progress Bar
    progressBar = None
    
    #Color Picker
    pickerX = 0
    pickerY = 0
    pickerWidth = 0
    pickerHeight = 0
    pickerFontSize = 0
    pickerFontColorRGB = "0,0,0"
    pickerFontColor = None
    pickerFont = None
    
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
        
        ff = FileFinder.FileFinder()
        
        self.interfaceJson = interfaceJson
        
        self.buttonsJson = []
        
        self.lblsJson = []
        self.lblFontColor = []
        self.lblXPos = []
        self.lblYPos = []
        self.lblText = []
        self.lblFont = []
        self.lblIndexes = []
        
        self.images = []
        self.imagesJson = []
        self.imagePath = []
        self.imageX = []
        self.imageY = []
        
        self.lblsJson.append(json.loads(json.dumps(self.interfaceJson['PrintingTopLabel'])))
        self.lblIndexes.append(len(self.lblsJson[0]))
        self.lblsJson.append(json.loads(json.dumps(self.interfaceJson['PausedTopLabel'])))
        self.lblIndexes.append(len(self.lblsJson[1]))
        self.lblsJson.append(json.loads(json.dumps(self.interfaceJson['ShutdownTopLabel'])))
        self.lblIndexes.append(len(self.lblsJson[2]))
        self.lblsJson.append(json.loads(json.dumps(self.interfaceJson['FilamentTopLabel'])))
        self.lblIndexes.append(len(self.lblsJson[3]))
        self.lblsJson.append(json.loads(json.dumps(self.interfaceJson['PickerTopLabel'])))
        self.lblIndexes.append(len(self.lblsJson[4]))
        self.lblsJson.append(json.loads(json.dumps(self.interfaceJson['FinishTopLabel'])))
        self.lblIndexes.append(len(self.lblsJson[5]))
        
        self.buttonsJson.append(json.loads(json.dumps(self.interfaceJson['PrintingButtons'])))
        self.buttonsJson.append(json.loads(json.dumps(self.interfaceJson['PausedButtons'])))
        self.buttonsJson.append(json.loads(json.dumps(self.interfaceJson['ShutdownButtons'])))
        self.buttonsJson.append(json.loads(json.dumps(self.interfaceJson['FilamentButtons'])))
        self.buttonsJson.append(json.loads(json.dumps(self.interfaceJson['PickerButtons'])))
        self.buttonsJson.append(json.loads(json.dumps(self.interfaceJson['FinishButtons'])))
        
        self.imagesJson.append(json.loads(json.dumps(self.interfaceJson['PrintingImage'])))
        self.imagesJson.append(json.loads(json.dumps(self.interfaceJson['PausedImage'])))
        self.imagesJson.append(json.loads(json.dumps(self.interfaceJson['ShutdownImage'])))
        self.imagesJson.append('')                                                              #Filament Change IMG
        self.imagesJson.append('')                                                              #Picker IMG
        self.imagesJson.append(json.loads(json.dumps(self.interfaceJson['FinishImage'])))
        
        """
        Time Label Configuration
        """
        timeLblJson = json.loads(json.dumps(self.interfaceJson['TimeLabel']))
        
        self.timeLblXPos = int(float(timeLblJson['X'])*self.displayWidth)
        self.timeLblYPos = int(float(timeLblJson['Y'])*self.displayHeight)
        self.timeLblText = timeLblJson['Text']
        
        self.timeLblFont = self.GetFont(timeLblJson['FontType'],int(float(timeLblJson['FontSize'])*self.displayHeight))
        
        timeFontColor = timeLblJson['FontColor']
        splitColor = timeFontColor.split(",")
        self.timeLblFontColor = pygame.Color(int(splitColor[0]),int(splitColor[1]),int(splitColor[2]))
        
        """
        Color Label Configuration
        """
        colorLblJson = json.loads(json.dumps(self.interfaceJson['ColorLabel']))
        
        self.colorLblXPos = int(float(colorLblJson['X'])*self.displayWidth)
        self.colorLblYPos = int(float(colorLblJson['Y'])*self.displayHeight)
        self.colorLblText = colorLblJson['Text']
        
        self.colorLblFont = self.GetFont(colorLblJson['FontType'],int(float(colorLblJson['FontSize'])*self.displayHeight))
        
        colorFontColor = colorLblJson['FontColor']
        splitColor = colorFontColor.split(",")
        self.colorLblFontColor = pygame.Color(int(splitColor[0]),int(splitColor[1]),int(splitColor[2]))
        
        """
        Load Labels Configuration
        """
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
        self.interfaceButtons = []
        for btns in self.buttonsJson:
            filButtons = []
            for btn in btns:
                btnX = int(float(btn['X'])*self.displayWidth)
                btnY = int(float(btn['Y'])*self.displayHeight)
                btnWidth = int(float(btn['Width'])*self.displayHeight)
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
        Load Image Configuration
        """
        for img in self.imagesJson:
            if(img != ''):
                imgJson = json.loads(json.dumps(img))
                for img in imgJson:
                    self.imagePath.append(ff.GetAbsPath(img['ImgPath']))
                    self.imageX.append(int(float(img['X'])*self.displayHeight))
                    self.imageY.append(int(float(img['Y'])*self.displayHeight))
            else:
                self.imagePath.append('')
                self.imageX.append('')
                self.imageY.append('')
                    
        
        """
        Load Progress Bar Configuration
        """
        pBarJson = json.loads(json.dumps(self.interfaceJson['ProgressBar']))
        pBarX = int(float(pBarJson['X'])*self.displayWidth)
        pBarY = int(float(pBarJson['Y'])*self.displayHeight)
        pBarWidth = int(float(pBarJson['Width'])*self.displayWidth)
        pBarHeight = int(float(pBarJson['Height'])*self.displayHeight)
        pBarThickness = int(pBarJson['Thickness'])
        pBarLineColorRGB = pBarJson['LineColor']
        pBarFillColorRGB = pBarJson['bgColor']
        
        splitColor = pBarLineColorRGB.split(",")
        pBarLineColor = pygame.Color(int(splitColor[0]),int(splitColor[1]),int(splitColor[2]))
        
        splitColor = pBarFillColorRGB.split(",")
        pBarFillColor = pygame.Color(int(splitColor[0]),int(splitColor[1]),int(splitColor[2]))
        
        self.progressBar = ProgressBar.ProgressBar(pBarX,pBarY,pBarWidth,pBarHeight,pBarLineColor,pBarFillColor,pBarThickness)
        
        """
        Color Picker Configuration
        """
        colorPickerJson = json.loads(json.dumps(self.interfaceJson['ColorPicker']))
        self.pickerX = int(float(colorPickerJson['X'])*self.displayWidth)
        self.pickerY = int(float(colorPickerJson['Y'])*self.displayHeight)
        self.pickerWidth = int(float(colorPickerJson['Width'])*self.displayWidth)
        self.pickerHeight = int(float(colorPickerJson['Height'])*self.displayHeight)
        self.pickerFontSize = int(float(colorPickerJson['FontSize'])*self.displayHeight)
        pickerFontColorRGB = colorPickerJson['FontColor']
        fontType = colorPickerJson['FontType']
            
        font = self.GetFont(fontType,self.pickerFontSize)
        
        self.pickerFont = font
        
        splitColor = pickerFontColorRGB.split(",")
        self.pickerFontColor = pygame.Color(int(splitColor[0]),int(splitColor[1]),int(splitColor[2]))
                
        return

    """*************************************************************************
                                FONT
    *************************************************************************"""
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

    """*************************************************************************
                                BUTTONS
    *************************************************************************"""
    
    """
    GetButtonsList(self)
    
    returns the list with buttons
    """
    def GetButtonsList(self,interfaceState):
        
        return self.interfaceButtons[interfaceState]
    
    """*************************************************************************
                                LABELS
    *************************************************************************"""
    """
    GetLblsText
    """
    def GetLblsText(self,interfaceState):
        return self.lblText[interfaceState]
    
    """
    GetLblsFont
    """
    def GetLblsFont(self,interfaceState):
        return self.lblFont[interfaceState]
    
    """
    GetLblsFontColor
    """
    def GetLblsFontColor(self,interfaceState):
        return self.lblFontColor[interfaceState]
    
    """
    GetLblsXPos
    """
    def GetLblsXPos(self,interfaceState):
        return self.lblXPos[interfaceState]
    
    """
    GetLblsYPos
    """
    def GetLblsYPos(self,interfaceState):
        return self.lblYPos[interfaceState]
    
    """
    GetTimeLblText
    """
    def GetTimeLblText(self,interfaceState):
        if interfaceState == 0:
            return self.timeLblText
        if interfaceState == 5:
            return ''
    
    """
    GetTimeLblFont
    """
    def GetTimeLblFont(self,interfaceState):
        if interfaceState == 0 or interfaceState == 5:
            return self.timeLblFont
    
    """
    GetTimeLblFontColor
    """
    def GetTimeLblFontColor(self,interfaceState):
        if interfaceState == 0 or interfaceState == 5:
            return self.timeLblFontColor
    
    """
    GetTimeLblXPos
    """
    def GetTimeLblXPos(self,interfaceState):
        if interfaceState == 0 or interfaceState == 5:
            return self.timeLblXPos
    
    """
    GetTimeLblYPos
    """
    def GetTimeLblYPos(self,interfaceState):
        if interfaceState == 0 or interfaceState == 5:
            return self.timeLblYPos
    
    """
    GetColorLblText
    """
    def GetColorLblText(self,interfaceState):
        if interfaceState == 3:
            return self.colorLblText
    
    """
    GetColorLblFont
    """
    def GetColorLblFont(self,interfaceState):
        if interfaceState == 3:
            return self.colorLblFont
    
    """
    GetColorLblFontColor
    """
    def GetColorLblFontColor(self,interfaceState):
        if interfaceState == 3:
            return self.colorLblFontColor
    
    """
    GetColorLblXPos
    """
    def GetColorLblXPos(self,interfaceState):
        if interfaceState == 3:
            return self.colorLblXPos
    
    """
    GetColorLblYPos
    """
    def GetColorLblYPos(self,interfaceState):
        if interfaceState == 3:
            return self.colorLblYPos

    """*************************************************************************
                                IMAGES
    *************************************************************************"""
    
    """
    GetImagePath
    """
    def GetImagePath(self,interfaceState):
            return self.imagePath[interfaceState]
    
    """
    GetImageX
    """
    def GetImageX(self,interfaceState):
            return self.imageX[interfaceState]
    
    """
    GetImageY
    """
    def GetImageY(self,interfaceState):
            return self.imageY[interfaceState]
    
    """*************************************************************************
                                PICKER
    *************************************************************************"""
    
    """
    GetProgessBar
    """
    def GetProgessBar(self,interfaceState):
        if(interfaceState == 0):
            return self.progressBar 
        else:
            return
    
    """*************************************************************************
                                PROGRES BAR
    *************************************************************************"""
    
    """
    GetPickerX
    """
    def GetPickerX(self):
        return self.pickerX
    
    """
    GetPickerY
    """
    def GetPickerY(self):
        return self.pickerY
    
    """
    GetPickerWidth
    """
    def GetPickerWidth(self):
        return self.pickerWidth
    
    """
    GetPickerHeight
    """
    def GetPickerHeight(self):
        return self.pickerHeight
    
    """
    GetPickerFontSize
    """
    def GetPickerFontSize(self):
        return self.pickerFontSize
    
    """
    GetPickerFontColor
    """
    def GetPickerFontColor(self):
        return self.pickerFontColor
    
    """
    GetPickerFont
    """
    def GetPickerFont(self):
        return self.pickerFont
        
        