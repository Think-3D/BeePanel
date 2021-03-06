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

import pygame
from BeeConnect import *

class JogScreen():
    
    screen = None
    
    lblFont = None
    lblTop = None
    lblFontColor = None
    
    jogButtons = None
    
    multiplier = "1"
    multiplierRect = None
    
    interfaceLoader = None
    
    exitNeedsHoming = False
    exitCallBackResp = None
    
    """*************************************************************************
                                Init Method 
    
    Inits current screen components
    *************************************************************************"""
    def __init__(self, screen, interfaceLoader, comm):
        
        self.comm = comm
        
        self.screen = screen
        self.interfaceLoader = interfaceLoader
        
        self.lblFont = self.interfaceLoader.GetlblFont()
        self.lblFontColor = self.interfaceLoader.GetlblFontColor()
        
        self.jogButtons = self.interfaceLoader.GetButtonsList()
        
        self.multiplier = 1
        
        print("Loading Jog Screen Components")
        
        return
        
        

    """*************************************************************************
                                handle_events Method 
    
    Received the event vector and checks if it has any event from interface items
    *************************************************************************"""
    def handle_events(self,retVal):
        """handle all events."""
        for event in retVal:
            
            for btn in self.jogButtons:
                if 'click' in btn.handleEvent(event):
                    btnName = btn._propGetName()
                    
                    if (btnName == '0.1') or (btnName == '1') or (btnName == '10'):
                        self.multiplier = btnName
                    elif btnName == "HomeXY":
                        print("G28 X0 Y0")
                        self.comm.homeXY()
                    elif btnName == "HomeZ":
                        print("G28 Z0")
                        self.comm.homeZ()
                    elif btnName == "X+":
                        val = float(self.multiplier)
                        print("X",val)
                        self.comm.move(val,None,None,None)
                    elif btnName == "X-":
                        val = -1 * float(self.multiplier)
                        print("X",val)
                        self.comm.move(val,None,None,None)
                    elif btnName == "Y+":
                        val = float(self.multiplier)
                        print("Y",val)
                        self.comm.move(None,val,None,None)
                    elif btnName == "Y-":
                        val = -1 * float(self.multiplier)
                        print("Y",val)
                        self.comm.move(None,val,None,None)
                    elif btnName == "Z+":
                        val = float(self.multiplier)
                        print("Z",val)
                        self.comm.move(None,None,val,None)
                    elif btnName == "Z-":
                        val = -1 * float(self.multiplier)
                        print("Z",val)
                        self.comm.move(None,None,val,None)
                        
        
        return

    """*************************************************************************
                                update Method 
    
    Updates screen components
    *************************************************************************"""
    def update(self):
        
        self.lblTop = self.lblFont.render("Jog as you like:", 1, self.lblFontColor)
        
        for btn in self.jogButtons:
            btn.visible = True

        return

    """*************************************************************************
                                draw Method 
    
    Draws current screen
    *************************************************************************""" 
    def draw(self):
        
        self.screen.blit(self.lblTop, (self.interfaceLoader.GetlblXPos(),
                                            self.interfaceLoader.GetlblYPos()))
                                            
        for btn in self.jogButtons:
            btn.draw(self.screen)
            if btn._propGetName() == str(self.multiplier):
                pygame.draw.rect(self.screen, btn._propGetFgColor(), btn._propGetRect(), 3)
        
        #pygame.draw.rect(screen, color, (x,y,width,height), thickness)
        
        return
    
    """*************************************************************************
                                GetCurrentScreenName Method 
    
    Frees every element from memmory
    *************************************************************************""" 
    def GetCurrentScreenName(self):
        
        return "Jog"
    
    """*************************************************************************
                                KillAll Method 
    
    Frees every element from memmory
    *************************************************************************""" 
    def KillAll(self):
        
        self.lblFont = None
        self.lblTop = None
        self.lblFontColor = None
        
        self.jogButtons = None
        
        self.multiplier = "1"
        self.multiplierRect = None
        
        self.interfaceLoader = None
        
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