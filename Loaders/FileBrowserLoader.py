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
import ProgressBar

class FileBrowserLoader():
    
    interfaceJson = None
    topLblJson = []
    buttonsJson = []
    topLbltext = []
    lblsJson = []
    
    lblText = []
    lblFont = []
    lblFontColor = []
    lblXPos = []
    lblYPos = []
    lblIndexes = []
    
    lblTopFont = []
    lblTopFontColor = []
    lblTopXPos = []
    lblTopYPos = []
    
    interfaceButtons = []
    
    pickerX = None
    pickerY = None
    pickerWidth = None
    pickerHeight = None
    pickerFontSize = None
    pickerFont = None
    pickerStrlen = None
    pickerRowCount = None
    
    slicingImgJson = None
    transfImgJson = None
    heatImgJson = None
    
    slicingImgPath = None
    transfImgPath = None
    heatImgPath = None
    
    slicingImgX = 100
    transfImgX = 100
    heatImgX = 100
    
    sliceImgY = 0
    transfImgY = 0
    heatfImgY = 0
    
    #Progress Bar
    progressBar = None
    
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
        
        self.topLblJson.append(json.loads(json.dumps(self.interfaceJson['FirstTopLabel'])))
        self.topLblJson.append(json.loads(json.dumps(self.interfaceJson['SecondTopLabel'])))
        self.topLblJson.append(json.loads(json.dumps(self.interfaceJson['ThirdTopLabel'])))
        
        self.buttonsJson.append(json.loads(json.dumps(self.interfaceJson['FirstButtons'])))
        self.buttonsJson.append(json.loads(json.dumps(self.interfaceJson['SecondButtons'])))
        self.buttonsJson.append(json.loads(json.dumps(self.interfaceJson['ThirdButtons'])))
        
        """
        self.lblsJson.append(json.loads(json.dumps(self.interfaceJson['FirstLabels'])))
        self.lblIndexes.append(len(self.lblsJson[0]))
        self.lblsJson.append(json.loads(json.dumps(self.interfaceJson['SecondLabels'])))
        self.lblIndexes.append(len(self.lblsJson[1]))
        self.lblsJson.append(json.loads(json.dumps(self.interfaceJson['ThirdLabels'])))
        """
        
        self.transfImgJson = json.loads(json.dumps(self.interfaceJson['TransfImage']))
        self.heatImgJson = json.loads(json.dumps(self.interfaceJson['HeatImage']))
        
        """
        Load Top Labels Configuration
        """
        for topLbl in self.topLblJson:
            topLblFontType = topLbl['FontType']
            topLblFontSize = int(float(topLbl['FontSize'])*self.displayHeight)
            topLblFColor = topLbl['FontColor']
            self.lblTopXPos.append(int(float(topLbl['X'])*self.displayWidth))
            self.lblTopYPos.append(int(float(topLbl['Y'])*self.displayHeight))
            self.topLbltext.append(topLbl['Text'])
            self.lblTopFont.append(self.GetFont(topLblFontType,topLblFontSize))
            
            splitColor = topLblFColor.split(",")
            fontColor = pygame.Color(int(splitColor[0]),int(splitColor[1]),int(splitColor[2]))
            self.lblTopFontColor.append(fontColor)
        
        """
        Load Labels Configuration
        """
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
        
        """
        Load Buttons Configuration
        """
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
        File Picker Configuration
        """
        filePickerJson = json.loads(json.dumps(self.interfaceJson['FilePicker']))
        self.pickerX = int(float(filePickerJson['X'])*self.displayWidth)
        self.pickerY = int(float(filePickerJson['Y'])*self.displayHeight)
        self.pickerWidth = int(float(filePickerJson['Width'])*self.displayWidth)
        self.pickerHeight = int(float(filePickerJson['Height'])*self.displayHeight)
        self.pickerFontSize = int(float(filePickerJson['FontSize'])*self.displayHeight)
        self.pickerStrlen = int(filePickerJson['StringLen'])
        self.pickerRowCount = int(filePickerJson['RowCount'])
        pickerFontColorRGB = filePickerJson['FontColor']
        fontType = filePickerJson['FontType']
            
        font = self.GetFont(fontType,self.pickerFontSize)
        
        self.pickerFont = font
        
        splitColor = pickerFontColorRGB.split(",")
        self.pickerFontColor = pygame.Color(int(splitColor[0]),int(splitColor[1]),int(splitColor[2]))
        
        """
        File Picker Configuration
        """
        #dirJson = json.loads(json.dumps(self.interfaceJson['FileFolders']))
        #self.rpiDir = dirJson['RPI']
        #self.usbDir = dirJson['USB']
        
        """
        Image Files Configuration
        """
        self.transfImgPath = ff.GetAbsPath(self.transfImgJson['ImgPath'])
        self.heatImgPath = ff.GetAbsPath(self.heatImgJson['ImgPath'])
        
        self.transfImgX = int(float(self.transfImgJson['X'])*self.displayWidth)
        self.transfImgY = int(float(self.transfImgJson['Y'])*self.displayHeight)
        
        self.heatImgX = int(float(self.heatImgJson['X'])*self.displayWidth)
        self.heatImgY = int(float(self.heatImgJson['Y'])*self.displayHeight)
        
        """
        Load Progress Bar Configuration
        """
        pBarJson = json.loads(json.dumps(self.interfaceJson['ProgressBar']))
        pBarX = int(float(pBarJson['X'])*self.displayHeight)
        pBarY = int(float(pBarJson['Y'])*self.displayHeight)
        pBarWidth = int(float(pBarJson['Width'])*self.displayHeight)
        pBarHeight = int(float(pBarJson['Height'])*self.displayHeight)
        pBarThickness = int(pBarJson['Thickness'])
        pBarLineColorRGB = pBarJson['LineColor']
        pBarFillColorRGB = pBarJson['bgColor']
        
        splitColor = pBarLineColorRGB.split(",")
        pBarLineColor = pygame.Color(int(splitColor[0]),int(splitColor[1]),int(splitColor[2]))
        
        splitColor = pBarFillColorRGB.split(",")
        pBarFillColor = pygame.Color(int(splitColor[0]),int(splitColor[1]),int(splitColor[2]))
        
        self.progressBar = ProgressBar.ProgressBar(pBarX,pBarY,pBarWidth,pBarHeight,pBarLineColor,pBarFillColor,pBarThickness)
        
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
    
    
    """*************************************************************************
                                BUTTONS
    *************************************************************************"""
    
    """
    GetButtonsList(self)
    
    returns the list with buttons
    """
    def GetButtonsList(self,BrowserState):
        
        return self.interfaceButtons[BrowserState]
    
    """*************************************************************************
                                TOP LABELS
    *************************************************************************"""
    """
    GetToplblText(self)
    
    returns the list with the label text
    """
    def GetToplblText(self,BrowserState):
        
        return self.topLbltext[BrowserState]
    
    """
    GetTopLblFont
    """
    def GetTopLblFont(self,BrowserState):
        return self.lblTopFont[BrowserState]
    
    """
    GetTopLblFontColor
    """
    def GetTopLblFontColor(self,BrowserState):
        return self.lblTopFontColor[BrowserState]
    
    
    """
    GetTopLblXPos
    """
    def GetTopLblXPos(self,BrowserState):
        return self.lblTopXPos[BrowserState]
    
    """
    GetTopLblYPos
    """
    def GetTopLblYPos(self,BrowserState):
        return self.lblTopYPos[BrowserState]
    
    
    """*************************************************************************
                                LABELS
    *************************************************************************"""
    
    """
    GetlblText(self)
    
    returns the list with the label text
    """
    def GetlblText(self,BrowserState):
                
        return self.lblText[BrowserState]
    
    """
    GetlblFont
    """
    def GetlblFont(self,BrowserState):
        
        return self.lblFont[BrowserState]
    
    """
    GetlblFontColor
    """
    def GetlblFontColor(self,BrowserState):
        
        return self.lblFontColor[BrowserState]
    
    
    """
    GetlblTopXPos
    """
    def GetlblTopXPos(self,BrowserState):
        
        return self.lblXPos[BrowserState]
    
    """
    GetlblTopYPos
    """
    def GetlblTopYPos(self,BrowserState):
        
        return self.lblYPos[BrowserState]
    
    """*************************************************************************
                                FILE PICKER
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
    
    """
    GetPickerStrLen
    """
    def GetPickerStrLen(self):
        return self.pickerStrlen
    
    """
    GetPickerRowCount
    """
    def GetPickerRowCount(self):
        return self.pickerRowCount

    
    """*************************************************************************
                                IMAGES
    *************************************************************************"""
    
    """
    GetSlicingImgPath
    """
    def GetSlicingImgPath(self):
        return self.slicingImgPath
    
    """
    GetTransfImgPath
    """
    def GetTransfImgPath(self):
        return self.transfImgPath

    """
    GetHeatImgPath
    """
    def GetHeatImgPath(self):
        return self.heatImgPath

    """
    GetSlicingImgX
    """
    def GetSlicingImgX(self):
        return self.slicingImgX
    
    """
    GetSlicingImgY
    """
    def GetSlicingImgY(self):
        return self.slicingImgY
    
    """
    GetTransfImgX
    """
    def GetTransfImgX(self):
        return self.transfImgX
    
    """
    GetTransfImgY
    """
    def GetTransfImgY(self):
        return self.transfImgY

    """
    GetHeatImgX
    """
    def GetHeatImgX(self):
        return self.heatImgX
    
    """
    GetHeatImgY
    """
    def GetHeatImgY(self):
        return self.heatImgY
    
    """*************************************************************************
                                PROGRES BAR
    *************************************************************************"""
    """
    GetProgessBar
    """
    def GetProgessBar(self):
        return self.progressBar