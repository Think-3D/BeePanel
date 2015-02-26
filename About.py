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

from BeeConnect import *
import os
import pygame
import FileFinder

class AboutScreen():
    
    screen = None
    interfaceLoader = None
    
    """
    Labels
    """
    lblFontColor = None
    lblXPos = None
    lblYPos = None
    lblText = None
    lblFont = None
    lbls = None
    lbl = None
    
    """
    Buttons
    """
    buttons = None
    
    """
    Text Fields
    """
    txtFieldFontColor = None
    txtFieldXPos = None
    txtFieldYPos = None
    txtFieldFont = None
    
    updateTxtFieldText = ''
    txtFields = None
    
    """
    File Finder
    """
    ff = None
    
    updateReady = None
    
    exitNeedsHoming = False
    exitCallBackResp = None
    
    """
    BEEConnect vars
    """
    beeCmd = None
    
    """*************************************************************************
                                Init Method 
    
    Inits current screen components
    *************************************************************************"""
    def __init__(self, screen, interfaceLoader, cmd):
        """
        .
        """
        print("Loading About Screen Components")
        
        self.beeCmd = cmd
        
        self.screen = screen
        self.interfaceLoader = interfaceLoader
        
        self.updateReady = False
        
        self.lblFontColor = self.interfaceLoader.GetLblsFontColor()
        self.lblXPos = self.interfaceLoader.GetLblsXPos()
        self.lblYPos = self.interfaceLoader.GetLblsYPos()
        self.lblText = self.interfaceLoader.GetLblsText()
        self.lblFont = self.interfaceLoader.GetLblsFont()
        
        self.buttons = self.interfaceLoader.GetButtonsList()
        
        self.txtFieldFontColor = self.interfaceLoader.GetTxtFieldsFontColor()
        self.txtFieldXPos = self.interfaceLoader.GetTxtFieldsXPos()
        self.txtFieldYPos = self.interfaceLoader.GetTxtFieldsYPos()
        self.txtFieldFont = self.interfaceLoader.GetTxtFieldsFont()
        
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
                    
                    if btnName == "Check For Updates":
                        self.Check4Updates()
                    elif btnName == "Update":
                        print("Updating...")
                        self.Update()
        
        return

    """*************************************************************************
                                update Method 
    
    Updates screen components
    *************************************************************************"""
    def update(self):
        
        """
        Update labels
        """
        self.lbls = []
        for i in range(len(self.lblText)):
            self.lbls.append(self.lblFont[i].render(self.lblText[i], 1, self.lblFontColor[i]))
        
        """
        Update Text Fields
        """
        self.txtFields = []
        self.txtFields.append(self.txtFieldFont[0].render(self.updateTxtFieldText,1,self.txtFieldFontColor[0]))
        
        """
        Update Buttons
        """
        for btn in self.buttons:
            if btn._propGetName() == "Update":
                btn.visible = self.updateReady
            else:
                btn.visible = True
        
        return

    """*************************************************************************
                                draw Method 
    
    Draws current screen
    *************************************************************************""" 
    def draw(self):
            
        """
        Draw Labels
        """
        for i in range(0,len(self.lblText)):
            self.screen.blit(self.lbls[i], (self.lblXPos[i],self.lblYPos[i]))
        
        """
        Draw text Fields
        """
        self.screen.blit(self.txtFields[0],(self.txtFieldXPos[0],self.txtFieldYPos[0]))
        
        """
        Draw Buttons
        """
        for btn in self.buttons:
            btn.draw(self.screen)
            
        return
    
    """*************************************************************************
                                GetCurrentScreenName Method 
    
    Frees every element from memmory
    *************************************************************************""" 
    def GetCurrentScreenName(self):
        
        return "About"
    
    """*************************************************************************
                                KillAll Method 
    
    Frees every element from memmory
    *************************************************************************""" 
    def KillAll(self):
        
        self.screen = None
        self.interfaceLoader = None

        self.lblFontColor = None
        self.lblXPos = None
        self.lblYPos = None
        self.lblText = None
        self.lblFont = None

        self.lbl = None

        self.buttons = None

        self.updateReady = None
    
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
                                Check4Updates Method 
    
    Check For github updates
    *************************************************************************""" 
    def Check4Updates(self):
        
        os.system('git remote update')
        
        r = os.popen('git status -uno').read()
        
        if('Your branch is behind' in r):
            self.updateReady = True
        else:
            self.updateReady = False
        
        if(self.updateReady):
            self.updateTxtFieldText = 'New Update Available'
        else:
            self.updateTxtFieldText = 'Already Up-to-date'
        
        return
    
    """*************************************************************************
                                Update Method 
    
    Update variables
    *************************************************************************""" 
    def Update(self):
        
        self.ShowLoadingScreen()
        os.system('git pull')
        os.system('python3 setup.py install')
        
        self.exitCallBackResp = "Exit"
            
        return
    
    """*************************************************************************
                                ShowLoadingScreen Method 
    
    Shows Loading Screen 
    *************************************************************************"""  
    def ShowLoadingScreen(self):
        
        #Clear String
        self.screen.fill(pygame.Color(255,255,255))
        
        if(self.ff is None):
            self.ff = FileFinder.FileFinder()
        
        moovingImgPath = self.ff.GetAbsPath('/Images/loading.png')
        
        moovingImg = pygame.image.load(moovingImgPath)

        # Draw Image
        self.screen.blit(moovingImg,(72,32))
        
        # update screen
        pygame.display.update()
        
        pygame.event.get()
        
        return
    
    