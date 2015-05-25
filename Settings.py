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

import os
import FileFinder
import pygame

class SettingsScreen():
    
    screen = None
    interfaceLoader = None
    
    lblFontColor = None
    lblXPos = None
    lblYPos = None
    lblText = None
    lblFont = None
    
    lbl = None
    
    buttons = None
    
    updateReady = None
    
    exitNeedsHoming = False
    exitCallBackResp = None
    
    fileFinder = None
    folderList = None
    fileList = None
    wifiFile = None
    """*************************************************************************
                                Init Method 
    
    Inits current screen components
    *************************************************************************"""
    def __init__(self, screen, interfaceLoader, comm):
        """
        .
        """
        print("Loading Settings Screen Components")
        
        self.screen = screen
        self.interfaceLoader = interfaceLoader
        
        self.updateReady = False
        
        self.lblFontColor = self.interfaceLoader.GetLblsFontColor()
        self.lblXPos = self.interfaceLoader.GetLblsXPos()
        self.lblYPos = self.interfaceLoader.GetLblsYPos()
        self.lblText = self.interfaceLoader.GetLblsText()
        self.lblFont = self.interfaceLoader.GetLblsFont()
        
        self.buttons = self.interfaceLoader.GetButtonsList()
        
        self.search4WifiConf();
        
        
        
        
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
                    
                    if btnName == "Update Cura":
                        print("Updating Cura...")
                    elif btnName == "Update WiFi":
                        self.search4WifiConf();
                        if(self.wifiFile is not None):
                            osCMD = 'sudo cp ' + self.wifiFile + ' /etc/wpa_supplicant/wpa_supplicant.conf'
                            print("Updating WiFi...")
                            print(osCMD)
                            os.system(osCMD)
                    elif btnName == "Screen Calibration":
                        os.system("sudo TSLIB_FBDEVICE=/dev/fb1 TSLIB_TSDEVICE=/dev/input/touchscreen ts_calibrate")
                    elif btnName == "Quit BEETFT":
                        #pygame.quit()
                        self.exitCallBackResp = "Quit"
        
        return

    """*************************************************************************
                                update Method 
    
    Updates screen components
    *************************************************************************"""
    def update(self):
        
        self.lbls = []
        for i in range(0,len(self.lblText)):
            self.lbls.append(self.lblFont[i].render(self.lblText[i], 1, self.lblFontColor[i]))
        
        for btn in self.buttons:
            btn.visible = True
                
        return

    """*************************************************************************
                                draw Method 
    
    Draws current screen
    *************************************************************************""" 
    def draw(self):
        
        for i in range(0,len(self.lblText)):
            self.screen.blit(self.lbls[i], (self.lblXPos[i],self.lblYPos[i]))
        
        for btn in self.buttons:
            btn.draw(self.screen)
        
        return
    
    """*************************************************************************
                                GetCurrentScreenName Method 
    
    Frees every element from memmory
    *************************************************************************""" 
    def GetCurrentScreenName(self):
        
        return "Settings"
    
    """*************************************************************************
                                KillAll Method 
    
    Frees every element from memmory
    *************************************************************************""" 
    def KillAll(self):
        
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
                                search4WifiConf Method 
    
    Pull variables
    *************************************************************************""" 
    def search4WifiConf(self):
        
        self.wifiFile = None
        
        #FILE LIST
        self.fileFinder = FileFinder.FileFinder()
        self.fileList = self.fileFinder.LoadUSBFolders('.conf')
        self.folderList = self.fileList['FolderList']
        
        for folder in self.folderList['FileNames']:
            files = self.fileList[folder]
            for i in range(len(files['FileNames'])):
                if(files['FileNames'][i] == 'wifi.conf'):
                    self.wifiFile = files['FilePaths'][i]
                    
        if(self.wifiFile is not None):
            print('Founf wifi.conf in: ',self.wifiFile);
        
        return