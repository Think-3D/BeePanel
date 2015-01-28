#!/usr/bin/env python

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
    
    bee = None
    
    """*************************************************************************
                                Init Method 
    
    *************************************************************************"""
    def __init__(self, interfaceJson):
        r"""
        __init__ Method
        
        Initializes current class
        """
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
        Load Buttons Configuration
        """
        self.interfaceButtons = []
        for btns in self.buttonsJson:
            filButtons = []
            for btn in btns:
                btnX = int(btn['X'])
                btnY = int(btn['Y'])
                btnWidth = int(btn['Width'])
                btnHeight = int(btn['Height'])
                btnType = btn['ButtonType']
                
            
                if btnType == "Text":
                    btnTitle = btn['Title']
                    bgColor = btn['bgColor'].split(",")
                    fColor = btn['FontColor'].split(",")
                    fType = btn['FontType']
                    fSize = int(btn['FontSize'])
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