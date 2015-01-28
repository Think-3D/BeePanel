#!/usr/bin/env python

"""
BEETFT v0.1

BEETFT creates a simple interface to control basic function of the BEETHEFIRST 3D printer.
BEETFT requires Pygame to be installed. Pygame can be downloaded from http://pygame.org
BEETFT is developed by Marcos Gomes
https://github.com/marcosfg/BEETFT


The MIT License (MIT)

Copyright (c) 2014 Marcos Gomes

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,p
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
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

        




