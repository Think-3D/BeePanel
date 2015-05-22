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


import pygame
from BeeConnect import *
import FileFinder

class CalibrationScreen():
    
    ff = None
    calibrationState = 0
    
    interfaceLoader = None
    lbl = None
    lblText = ["Adjust Bed Height","Adjust Left Bolt","Adjust Right Bolt"]
    
    buttons = None
    
    exitNeedsHoming = True
    exitCallBackResp = None
    
    """
    Images
    """
    rightBoltImgPath = None
    leftBoltImgPath = None
    rightBoltImgX = 0
    rightBoltImgY = 0
    leftBoltImgX = 0
    leftBoltImgY = 0
    
    """
    BEEConnect vars
    """
    beeCmd = None
    
    """*************************************************************************
                                Init Method 
    
    Inits current screen components
    *************************************************************************"""
    def __init__(self, screen, interfaceLoader, cmd):
        
        print("Loading Calibration Screen Components")
        
        self.beeCmd = cmd
        
        self.screen = screen
        self.interfaceLoader = interfaceLoader
        
        self.calibrationState = 0
        
        self.lblFont = self.interfaceLoader.GetlblFont(self.calibrationState)
        self.lblFontColor = self.interfaceLoader.GetlblFontColor(self.calibrationState)
        
        self.buttons = self.interfaceLoader.GetButtonsList(self.calibrationState)
        
        self.rightBoltImg = pygame.image.load(self.interfaceLoader.GetRightImgPath())
        self.leftBoltImg = pygame.image.load(self.interfaceLoader.GetLeftImgPath())
        self.rightBoltImgX = self.interfaceLoader.GetRightImgX()
        self.rightBoltImgY = self.interfaceLoader.GetRightImgY()
        self.leftBoltImgX = self.interfaceLoader.GetLeftImgX()
        self.leftBoltImgY = self.interfaceLoader.GetLeftImgY()
        
        
        self.ShowWaitScreen()
        self.beeCmd.GoToFirstCalibrationPoint()
        pygame.event.get()
        
        return

    """*************************************************************************
                                handle_events Method 
    
    Received the event vector and checks if it has any event from interface items
    *************************************************************************"""
    def handle_events(self,retVal):
        """handle all events."""
        for event in retVal:
            
            for btn in self.buttons:
                if 'click' in btn.handleEvent(event):
                    btnName = btn._propGetName()
                    
                    if btnName == "Next":
                        self.calibrationState = self.calibrationState + 1
                        if self.calibrationState > 2:
                            self.exitCallBackResp = "Restart"
                            self.calibrationState = 2
                        else:
                            self.lblFont = None
                            self.lblFontColor = None
                            self.buttons = None
                            self.lblFont = self.interfaceLoader.GetlblFont(self.calibrationState)
                            self.lblFontColor = self.interfaceLoader.GetlblFontColor(self.calibrationState)
                            self.buttons = self.interfaceLoader.GetButtonsList(self.calibrationState)
                            if self.calibrationState == 1:
                                self.ShowWaitScreen()
                                self.beeCmd.GoToSecondCalibrationPoint()
                            elif self.calibrationState == 2:
                                self.ShowWaitScreen()
                                self.beeCmd.GoToThirdCalibrationPoint()
                    
                    elif btnName == "+0.5mm":
                        print("Move +0.5mm")
                        self.beeCmd.move(None,None,float(+0.5),None)
                    elif btnName == "+0.05mm":
                        print("Move +0.05mm")
                        self.beeCmd.move(None,None,float(+0.05),None)
                    elif btnName == "-0.05mm":
                        print("Move -0.05mm")
                        self.beeCmd.move(None,None,float(-0.05),None)
                    elif btnName == "-0.5mm":
                        print("Move -0.5mm")
                        self.beeCmd.move(None,None,float(-0.5),None)
                
                pygame.event.get()
                    
        return

    """*************************************************************************
                                update Method 
    
    Updates screen components
    *************************************************************************"""
    def update(self):
        
        self.lbl = self.lblFont.render(self.lblText[self.calibrationState], 1, self.lblFontColor)
        
        for btn in self.buttons:
            btn.visible = True
        
        return

    """*************************************************************************
                                draw Method 
    
    Draws current screen
    *************************************************************************""" 
    def draw(self):
        
        self.screen.blit(self.lbl, (self.interfaceLoader.GetlblXPos(self.calibrationState),
                                            self.interfaceLoader.GetlblYPos(self.calibrationState)))
        
        for btn in self.buttons:
            btn.draw(self.screen)
        
        if self.calibrationState == 1:
            # Draw Image
            self.screen.blit(self.leftBoltImg,(self.leftBoltImgX,self.leftBoltImgY))
        elif self.calibrationState == 2:
            # Draw Image
            self.screen.blit(self.rightBoltImg,(self.rightBoltImgX,self.rightBoltImgY))
        
        
        return
    
    """*************************************************************************
                                GetCurrentScreenName Method 
    
    Frees every element from memmory
    *************************************************************************""" 
    def GetCurrentScreenName(self):
        
        return "Calibration"
    
    """*************************************************************************
                                KillAll Method 
    
    Frees every element from memmory
    *************************************************************************""" 
    def KillAll(self):
        
        self.calibrationState = None
        self.interfaceLoader = None
        self.lbl = None
        self.lblText = None
        self.buttons = None
        self.rightBoltImgPath = None
        self.leftBoltImgPath = None
        self.rightBoltImgX = None
        self.rightBoltImgY = None
        self.leftBoltImgX = None
        self.leftBoltImgY = None
        
        return
    
    """*************************************************************************
                                ExitCallBack Method 
    
    Tells the main class to load the default interface
    *************************************************************************""" 
    def ExitCallBack(self):
        
        return self.exitCallBackResp
    
    """*************************************************************************
                                Pull Method 
    
    Pull variables
    *************************************************************************""" 
    def Pull(self):
        
        return
    
    """*************************************************************************
                                ShowWaitScreen Method 
    
    Shows Wait Screen 
    *************************************************************************"""  
    def ShowWaitScreen(self):
        
        #Clear String
        self.screen.fill(pygame.Color(255,255,255))
        
        if(self.ff is None):
            self.ff = FileFinder.FileFinder()
        
        moovingImgPath = self.ff.GetAbsPath('/Images/moving.png')
        
        moovingImg = pygame.image.load(moovingImgPath)

        # Draw Image
        self.screen.blit(moovingImg,(0,0))
        
        # update screen
        pygame.display.update()
        
        pygame.event.get()
        
        return