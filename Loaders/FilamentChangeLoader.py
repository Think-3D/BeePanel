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

FilamentChageLoader Class

This class is responsible for loading the interface components configuration 
from the .json configuration file.

This class exports the following methods:

__init__()            Initializes current class
GetFont(fType,fSyze)    returns pygame font from a given font type and syze
GetButtonsList()        returns interface button list
GetLblsText()            returns interface labels text list
GetLblsFont()            returns interface labels font list
GetLblsFontColor()            returns interface labels font color list
GetLblTopXPos()            returns interface top label X coordinate list
GetLblTopYPos()            returns interface top label Y coordinate list
GetLblsXPos()            returns interface labels X coordinate list
GetLblsYPos()            returns interface labels Y coordinate list
GetImagePath()        returns heating image path
GetImageX()        returns image X coordinate
GetImageY()        returns image Y coordinate
GetProcessBar()    returns prograss bar object
GetPickerX()        returns picker x coordinate
GetPickerY()        returns picker y coordinate
GetPickerWidth()        returns picker width
GetPickerHeight()        returns picker height
GetPickerFontSize()        returns picker font size
GetPickerFontColor()        returns picker font color
GetPickerFont()            returns picker font
GetSelectedLblFont()        returns Selected label Font
GetSelectedLblFontColor()    returns Selected label Font colot
GetSelectedLblX()            returns Selected label x coordinate
GetSelectedLblY()            returns Selected label y coordinate
"""


__author__ = "BVC Electronic Solutions"
__license__ = ""

import json

import BeePanel_Button
import FileFinder
import ProgressBar
import pygame

class FilamentChangeLoader():
    
    interfaceJson = None
    topLblJson = []
    buttonsJson = []
    lbltext = []
    
    lblTopFont = []
    lblTopFontColor = []
    lblTopXPos = []
    lblTopYPos = []
    
    interfaceButtons = []
    
    imagePath = None
    imageX = 100
    imageY = 0
    
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
        
        self.topLblJson.append(json.loads(json.dumps(self.interfaceJson['FirstTopLabel'])))
        self.topLblJson.append(json.loads(json.dumps(self.interfaceJson['SecondTopLabel'])))
        self.topLblJson.append(json.loads(json.dumps(self.interfaceJson['ThirdTopLabel'])))
        
        self.buttonsJson.append(json.loads(json.dumps(self.interfaceJson['FirstButtons'])))
        self.buttonsJson.append(json.loads(json.dumps(self.interfaceJson['SecondButtons'])))
        self.buttonsJson.append(json.loads(json.dumps(self.interfaceJson['ThirdButtons'])))
        
        """
        Load Top Labels Configuration
        """
        for lbl in self.topLblJson:
            lblFontType = lbl['FontType']
            lblFontSize = int(float(lbl['FontSize'])*self.displayHeight)
            lblFColor = lbl['lblFontColor']
            self.lblTopXPos.append(int(float(lbl['X'])*self.displayWidth))
            self.lblTopYPos.append(int(float(lbl['Y'])*self.displayHeight))
            self.lbltext.append(lbl['Text'])
            
            font = self.GetFont(lblFontType,lblFontSize)
            
            self.lblTopFont.append(font)
            
            splitColor = lblFColor.split(",")
            fontColor = pygame.Color(int(splitColor[0]),int(splitColor[1]),int(splitColor[2]))
            self.lblTopFontColor.append(fontColor)
        
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
                                                fType,fSize, None, None, None, btnName)
                    newBtn = jogBtn.GetTextButton()
                    newBtn._propSetName(btnTitle)
                    filButtons.append(newBtn)
                elif btnType == "Img":
                    btnTitle = btn['Title']
                    normalPath = btn['NormalPath']
                    downPath = btn['DownPath']
                    highlightedPath = btn['HighlightedPath']
                    btnName = btn['ButtonName']
                
                    jogBtn = BeePanel_Button.Button(btnX,btnY,btnWidth,btnHeight,btnTitle,
                                                None,None,None,None,None,None,
                                                None,None,
                                                normalPath,downPath,highlightedPath,
                                                btnName)
                    newBtn = jogBtn.GetImageButton()
                    newBtn._propSetName(btnTitle)
                    filButtons.append(newBtn)
        
            self.interfaceButtons.append(filButtons)
        
        """
        Load Heating Image Configuration
        """
        imageJson = json.loads(json.dumps(self.interfaceJson['FirstImage']))
        self.imagePath = ff.GetAbsPath(imageJson['ImgPath'])
        self.imageX = int(float(imageJson['X'])*self.displayWidth)
        self.imageY = int(float(imageJson['Y'])*self.displayHeight)
        
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
        
        
        
        """
        Selected Color Label Configuration
        """
        colorLblJson = json.loads(json.dumps(self.interfaceJson['SelectedColorLbl']))
        lblFontType = colorLblJson['FontType']
        lblFontSize = int(float(colorLblJson['FontSize'])*self.displayHeight)
        lblFColor = colorLblJson['FontColor']
        self.selectedLblX = int(float(colorLblJson['X'])*self.displayWidth)
        self.selectedLblY = int(float(colorLblJson['Y'])*self.displayHeight)
            
        splitColor = lblFColor.split(",")
        self.selectedLblFontColor = pygame.Color(int(splitColor[0]),int(splitColor[1]),int(splitColor[2]))
        self.selectedLblFont = self.GetFont(lblFontType,lblFontSize)
            
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
    def GetButtonsList(self,interfaceState):
        r"""
        GetButtonsList method
        
        arguments:
            interfaceState - number of current interface state
        
        returns interface buttons list
        """
        return self.interfaceButtons[interfaceState]
    
    """*************************************************************************
                                GetlblText Method 
    
    
    *************************************************************************"""
    def GetlblText(self,interfaceState):
        r"""
        GetlblText method
        
        arguments:
            interfaceState - number of current interface state
            
        returns labels text
        """
        
        return self.lbltext[interfaceState]
    
    """*************************************************************************
                                GetlblFont Method 
    
    
    *************************************************************************"""
    def GetlblFont(self,interfaceState):
        r"""
        GetlblFont method
        
        arguments:
            interfaceState - number of current interface state
            
        returns labels pygame font
        """
        return self.lblTopFont[interfaceState]
    
    """*************************************************************************
                                GetlblFontColor Method 
    
    
    *************************************************************************"""
    def GetlblFontColor(self,interfaceState):
        r"""
        GetlblFontColor method
        
        arguments:
            interfaceState - number of current interface state
            
        returns labels font color
        """
        return self.lblTopFontColor[interfaceState]
    
    
    """*************************************************************************
                                GetlblTopXPos Method 
    
    
    *************************************************************************"""
    def GetlblTopXPos(self,interfaceState):
        r"""
        GetlblTopXPos method
        
        arguments:
            interfaceState - number of current interface state
            
        returns top label x coordinate
        """
        return self.lblTopXPos[interfaceState]
    
    """*************************************************************************
                                GetlblTopYPos Method 
    
    
    *************************************************************************"""
    def GetlblTopYPos(self,interfaceState):
        r"""
        GetlblTopYPos method
        
        arguments:
            interfaceState - number of current interface state
            
        returns top label y coordinate
        """
        return self.lblTopYPos[interfaceState]
    
    """*************************************************************************
                                GetImagePath Method 
    
    
    *************************************************************************"""
    def GetImagePath(self):
        r"""
        GetImagePath method
        
        returns image path
        """
        return self.imagePath
    
    """*************************************************************************
                                GetImageX Method 
    
    
    *************************************************************************"""
    def GetImageX(self):
        r"""
        GetImageX method
        
        returns image x coordinate
        """
        return self.imageX
    
    """*************************************************************************
                                GetImageY Method 
    
    
    *************************************************************************"""
    def GetImageY(self):
        r"""
        GetImageY method
        
        returns image y coordinate
        """
        return self.imageY
    
    """*************************************************************************
                                GetProgessBar Method 
    
    
    *************************************************************************"""
    def GetProgessBar(self):
        r"""
        GetProgessBar method
        
        returns GetProgessBar object
        """
        return self.progressBar
    
    """*************************************************************************
                                GetPickerX Method 
    
    
    *************************************************************************"""
    def GetPickerX(self):
        r"""
        GetPickerX method
        
        returns picker x coordinate
        """
        return self.pickerX
    
    """*************************************************************************
                                GetPickerY Method 
    
    
    *************************************************************************"""
    def GetPickerY(self):
        r"""
        GetPickerY method
        
        returns picker y coordinate
        """
        return self.pickerY
    
    """*************************************************************************
                                GetPickerWidth Method 
    
    
    *************************************************************************"""
    def GetPickerWidth(self):
        r"""
        GetPickerWidth method
        
        returns picker width
        """
        return self.pickerWidth
    
    """*************************************************************************
                                GetPickerHeight Method 
    
    
    *************************************************************************"""
    def GetPickerHeight(self):
        r"""
        GetPickerHeight method
        
        returns picker height
        """
        return self.pickerHeight
    
    """*************************************************************************
                                GetPickerFontSize Method 
    
    
    *************************************************************************"""
    def GetPickerFontSize(self):
        r"""
        GetPickerFontSize method
        
        returns picker font size
        """
        return self.pickerFontSize
    
    """*************************************************************************
                                GetPickerFontColor Method 
    
    
    *************************************************************************"""
    def GetPickerFontColor(self):
        r"""
        GetPickerFontColor method
        
        returns picker font color
        """
        return self.pickerFontColor
    
    """*************************************************************************
                                GetPickerFont Method 
    
    
    *************************************************************************"""
    def GetPickerFont(self):
        r"""
        GetPickerFont method
        
        returns picker font
        """
        return self.pickerFont
    
    """*************************************************************************
                                GetSelectedLblFont Method 
    
    
    *************************************************************************"""
    def GetSelectedLblFont(self):
        r"""
        GetPickerFont method
        
        returns selected label font
        """
        return self.selectedLblFont
    
    """*************************************************************************
                                GetSelectedLblFontColor Method 
    
    
    *************************************************************************"""
    def GetSelectedLblFontColor(self):
        r"""
        GetSelectedLblFontColor method
        
        returns selected label font color
        """
        return self.selectedLblFontColor
    
    """*************************************************************************
                                GetSelectedLblX Method 
    
    
    *************************************************************************"""
    def GetSelectedLblX(self):
        r"""
        GetSelectedLblX method
        
        returns selected label x coordinate
        """
        return self.selectedLblX
    
    """*************************************************************************
                                GetSelectedLblY Method 
    
    
    *************************************************************************"""
    def GetSelectedLblY(self):
        r"""
        GetSelectedLblY method
        
        returns selected label y coordinate
        """
        return self.selectedLblY