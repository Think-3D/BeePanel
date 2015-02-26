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

import time
import socket
import netifaces
import os

class PrinterInfoScreen():
    
    screen = None
    
    lblText = None           #list for label text
    lbl = None               #label object
    lblFont = None           #label font
    lblFontColor = None      #label color
    
    lblVal = None               #label object
    lblValFont = None           #label font
    lblValFontColor = None      #label color
    
    status = None
    fw = None
    localIp = '0.0.0.0'
    wirelessIP = None
    wirelessSSID = 'Disconnected'
    
    interfaceLoader = None
    
    nextPullTime = None
    pullInterval = 20
    
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
    def __init__(self, screen, interfaceLoader, comm):
        
        self.screen = screen
        self.interfaceLoader = interfaceLoader
        
        self.nextPullTime = time.time()
        self.Pull()
        
        self.beeCmd = comm
        
        print("Loading Printer Info Screen Components")
        
        """
        Load lists and settings from interfaceLoader
        """
        self.lblFont = self.interfaceLoader.GetlblFont()
        self.lblFontColor = self.interfaceLoader.GetlblFontColor()
        self.lblText = self.interfaceLoader.GetlblText()
        self.lblXPos = self.interfaceLoader.GetlblXPos()
        self.lblYPos = self.interfaceLoader.GetlblYPos()
        
        self.lblValFont = self.interfaceLoader.GetlblValFont()
        self.lblValFontColor = self.interfaceLoader.GetlblValFontColor()
        self.lblValXPos = self.interfaceLoader.GetlblValXPos()
        
        self.getIP()
        
        return

    """*************************************************************************
                                handle_events Method 
    
    Received the event vector and checks if it has any event from interface items
    *************************************************************************"""
    def handle_events(self,retVal):
        """handle all events."""
        for event in retVal:
            pass
        
        return

    """*************************************************************************
                                update Method 
    
    Updates screen components
    *************************************************************************"""
    def update(self):
        
        self.lbl = []
        self.lblVal = []
        for i in range(0,len(self.lblText)):
            self.lbl.append(self.lblFont[i].render(self.lblText[i], 1, self.lblFontColor[i]))
            
            fieldText = self.lblText[i]
            valText = ""
            if fieldText == "Printer Status:":
                valText = self.status
            elif fieldText == "Firmware:":
                valText = self.fw
            elif fieldText == "BeeConnect:":
                valText = "v0.1"
            elif fieldText == "Local IP:":
                valText = self.localIp
            elif fieldText == "Wireless SSID:":
                valText = self.wirelessSSID
            elif fieldText == "Wireless IP:":
                valText = self.wirelessIP
            
            self.lblVal.append(self.lblValFont.render(valText, 1, self.lblValFontColor))
            
        return

    """*************************************************************************
                                draw Method 
    
    Draws current screen
    *************************************************************************""" 
    def draw(self):
        
        for i in range(0,len(self.lblText)):
            self.screen.blit(self.lbl[i],(self.lblXPos[i],self.lblYPos[i]))
            self.screen.blit(self.lblVal[i],(self.lblValXPos,self.lblYPos[i]))
        
        return
    
    """*************************************************************************
                                GetCurrentScreenName Method 
    
    Frees every element from memmory
    *************************************************************************""" 
    def GetCurrentScreenName(self):
        
        return "Printer Info"
    
    """*************************************************************************
                                KillAll Method 
    
    Frees every element from memmory
    *************************************************************************""" 
    def KillAll(self):
        
        self.screen = None
        self.lblText = None
        self.lbl = None
        self.lblFont = None
        self.lblFontColor = None
        self.lblVal = None
        self.lblValFont = None
        self.lblValFontColor = None
        self.status = None
        self.fw = None
        self.wirelessIP = None
        self.wirelessSSID = None
        self.interfaceLoader = None
        self.nextPullTime = None
        self.pullInterval = None
        
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
        
        t = time.time()
        if t > self.nextPullTime:
            
            if(self.beeCmd is None):
                return
            
            self.nextPullTime = time.time() + self.pullInterval
            
            self.status = self.beeCmd.getStatus()
            self.fw = self.beeCmd.GetFirmwareVersion()
            self.getIP()
        
        return
    
    """*************************************************************************
                                getIP Method 
    
    
    *************************************************************************""" 
    def getIP(self):
        
        #GET ETHERNET ADDRESS
        try:
            self.localIp = netifaces.ifaddresses('eth0')[2][0]['addr']
        except:
            self.localIp = 'Disconnected'
        
        #GET WLAN ADDRESS
        try:
            self.wirelessIP = netifaces.ifaddresses('wlan0')[2][0]['addr']
        except:
            self.wirelessIP = 'Disconnected'
        
        #GET WIRELESS SSID
        #iwconfig wlan0 | grep 'ESSID:' | awk '{print $4}' | sed 's/ESSID://g' | sed 's/"//g'
        self.wirelessSSID = os.popen('iwconfig wlan0 | grep '+ "'ESSID:' | awk '{print $4}' | sed 's/ESSID://g' | sed 's/"+ '"//g' + "'").read()[:-1]
        
        return