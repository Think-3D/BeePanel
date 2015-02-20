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

import BeeConnect

import FileFinder
import pygame
import Loaders.WaitForConnectionLoader
from BeeConnect import *
import time

class WaitScreen():
    """
    @var connected: status of USB connection to the BTF      
    """
    connected = False
    screen = None
    exit = False
    
    lblTop = None
    lblBottom = None
    bgImage = None
    
    loader = None
    
    nextPullTime = None
    
    """
    BEEConnect vars
    """
    beeCon = None
    beeCmd = None
    
    """*************************************************************************
                                Init Method 
    
    intis all compoments
    *************************************************************************"""
    def __init__(self, screen):
        """
        .
        """
        self.connected = False
        
        print("Printer Connection: ",self.connected)
        
        
        self.exit = False
        self.screen = screen
        self.currentScreen = 'WaitConnection'
        
        self.loader = Loaders.WaitForConnectionLoader.WaitForConnectionLoader()
        
        lblText = self.loader.GetLblsText()
        lblX = self.loader.GetLblsXPos()
        lblY = self.loader.GetLblsYPos()
        lblFont = self.loader.GetLblsFont()
        lblFontColor = self.loader.GetLblsFontColor()
        
        for i in range(0,len(lblText)):
            lbl = lblFont[i].render(lblText[i],1,lblFontColor[i])
            self.screen.blit(lbl,(lblX[i],lblY[i]))
        
        
        self.bgImage = pygame.image.load(self.loader.GetImagePath())
        imgX = self.loader.GetImageX()
        imgY = self.loader.GetImageY()

        # Draw Image
        self.screen.blit(self.bgImage,(imgX,imgY))

        # update screen
        pygame.display.update()
        
        self.nextPullTime = time.time() + 0.5
        
        while (not self.connected) and (not self.exit):
            # Handle events
            self.handle_events()
            
            t = time.time()
            if t > self.nextPullTime:
                
                self.beeCon = BeeConnect.Connection.Con()
                if(self.beeCon.isConnected() == True):
                    self.beeCmd = BeeConnect.Command.Cmd(self.beeCon)
                    resp = self.beeCmd.startPrinter()
                
                    if('Firmware' in resp):
                        self.connected = self.beeCon.connected
                    elif('Bootloader' in resp):
                        self.beeCon = None
                    else:
                        cleaningTries = 5
                        clean = False
                        while(cleaningTries > 0 and clean == False):
                            clean = self.beeCmd.cleanBuffer()
                            time.sleep(0.5)
                            self.beeCmd.beeCon.close()
                            self.beeCmd.beeCon = None
                            self.beeCmd.beeCon = BeeConnect.Connection.Con()

                            cleaningTries -= 1

                        if(cleaningTries <= 0 or clean == False):
                            self.beeCon.close()
                            self.beeCon = None
                        else:
                            self.beeCon = self.beeCmd.beeCon
                        #return None
                    
                self.nextPullTime = time.time() + 0.5
                print("Wait for connection")
            
        return
    

    """*************************************************************************
                                handle_events
    
    waits for a USB conenction to be stablished
    *************************************************************************"""
    def handle_events(self):
        """handle all events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit = True
                
        return
    
    """*************************************************************************
                                KillAll Method 
    
    Frees every element from memmory
    *************************************************************************""" 
    def KillAll(self):
        
        self.bgImage = None
        self.lblTop = None
        self.lblBottom = None
        self.loader = None
        self.nextPullTime = None
        
        return

        




