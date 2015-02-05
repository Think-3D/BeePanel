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

import os
import subprocess
from time import time
import math
import FileFinder
import pygame
import platform

class FileBrowserScreen():
    
    """
    Interface state vars
    """
    exit = False
    interfaceState = 0
    exitCallBackResp = None
    
    """
    BEEConnect vars
    """
    #conn = None
    beeCon = None
    beeCmd = None
    
    """
    Labels vars
    """
    lblTopText = None           #list for top label text
    lblTop = None               #Top label object
    lblTopFont = None           #Top label font
    lblTopFontColor = None      #top label color
    
    #lblText = None           #list for label text
    #lbl = None               #label object
    #lblFont = None           #label font
    #lblFontColor = None      #label color
    
    """
    Progress Bar vars
    """
    progressBar = None
    pBarRect = None
    pBarFill = None
    
    """
    Images
    """
    transfImgPath = None
    heatImgPath = None
    
    transfImgX = 0
    transfImgY = 0
    
    heatImgX = 0
    heatImgY = 0
    
    """
    File Picker
    """
    fileFinder = None
    folderList = None
    fileList = None
    pickerList = None
    
    selectedFolderIdx = -1
    selectedFileIdx = -1
    
    selectedFolderName = ""
    selectedFileName = ""
    selectedFilePath = ""
    selectedGCode = False
    selectedRoot = "USB"
    
    pickFileRect = None        #Rect for selected color
    listPosition = 0
    selectedFileIdx = 0
    pickerStrLen = 20
    
    isGCodeFile = False
    verifyGCode = False
    
    pickerStateChanged = True
    
    """
    TRANSFER GCODE VARS
    """
    fileSize = 0
    blocksTransfered = 0
    nBlocks = 0
    blockSize = 0
    totalBytes = 0
    startTime = 0
    gcodeFile = None
    
    """
    HEATING INTERFACE VALS
    """
    nextPullTime = 0
    sdFileName = ""
    pullInterval = 2
    targetTemperature = 220
    nozzleTemperature = 0
    
    """*************************************************************************
                                Init Method 
    
    Inits current screen components
    *************************************************************************"""
    def __init__(self, screen, interfaceLoader, cmd):
        """
        .
        """
        print("Loading File Browser Screen Components")
        
        if(cmd is None):
            self.beeCmd = None
            self.beeCon = None
        else:
            self.beeCmd = cmd
            self.beeCon = self.beeCmd.beeCon
        
        self.screen = screen
        self.interfaceLoader = interfaceLoader
        
        self.interfaceState = 0         #reset interface state
        
        """
        Load lists and settings from interfaceLoader
        """
        self.lblTopFont = self.interfaceLoader.GetTopLblFont(self.interfaceState)
        self.lblTopFontColor = self.interfaceLoader.GetTopLblFontColor(self.interfaceState)
        self.lblTopText = self.interfaceLoader.GetToplblText(self.interfaceState)
        
        #self.lblFont = self.interfaceLoader.GetlblFont(self.interfaceState)
        #self.lblFontColor = self.interfaceLoader.GetlblFontColor(self.interfaceState)
        #self.lblText = self.interfaceLoader.GetlblText(self.interfaceState)
        
        self.buttons = self.interfaceLoader.GetButtonsList(self.interfaceState)
        
        #PROGRESS BAR
        self.progressBar = self.interfaceLoader.GetProgessBar()
        
        #FILE LIST
        self.fileFinder = FileFinder.FileFinder()
        
        self.fileList = self.fileFinder.LoadUSBFolders()
        self.folderList = self.fileList['FolderList']
        #LOAD BTF FILES TO FILE LIST
        print("Loading BTF internal memory gcode files")
        if(self.beeCon is None or self.beeCmd is None):
            self.fileList['BTF'] = {}
        else:
            self.fileList['BTF'] = self.beeCmd.getFileList()
        self.selectedFolderName = ""
        if(len(self.fileList['FolderList']['FileNames']) == 1):
            self.selectedFolderName = self.fileList['FolderList']['FileNames'][0]
        
        #CLEAR AND INITIALIZA PICKER DICTIONARY
        self.selectedRoot = "USB"
        self.pickerList = {}
        self.pickerList['FileNameBuffer'] = []
        self.pickerList['FilePathBuffer'] = []
        self.pickerList['Source'] = 'USB-Drives'
        
        self.transfImg = pygame.image.load(self.interfaceLoader.GetTransfImgPath())
        self.heatImg = pygame.image.load(self.interfaceLoader.GetHeatImgPath())
        
        self.transfImgX = self.interfaceLoader.GetTransfImgX()
        self.transfImgY = self.interfaceLoader.GetTransfImgY()
        
        self.heatImgX = self.interfaceLoader.GetHeatImgX()
        self.heatImgY = self.interfaceLoader.GetHeatImgY()
        
        self.nozzleTemperature = self.beeCmd.GetNozzleTemperature()
        
        #CLEAR EXISTING EVENTS
        retVal = pygame.event.get()
        retVal = None
        
        return

    """*************************************************************************
                                handle_events Method 
    
    Received the event vector and checks if it has any event from interface items
    *************************************************************************"""
    def handle_events(self,retVal):
        """handle all events."""
        for event in retVal:
            buttonEvent = False
            
            for btn in self.buttons:
                if 'click' in btn.handleEvent(event):
                    btnName = btn._propGetName()
                    if btnName == "Up":
                        self.listPosition = self.listPosition - 1
                        self.verifyGCode = True
                        buttonEvent = True
                        break
                    elif btnName == "Down":
                        self.listPosition = self.listPosition + 1
                        self.verifyGCode = True
                        buttonEvent = True
                        break
                    elif btnName == "BTF":
                        self.selectedRoot = 'BTF'
                        buttonEvent = True
                        break
                    elif btnName == "USB":
                        BTFFileList = self.fileList['BTF']
                        self.fileList = self.fileFinder.LoadUSBFolders()
                        self.folderList = self.fileList['FolderList']
                        self.fileList['BTF'] = BTFFileList
                        
                        self.selectedRoot = 'USB'
                        self.selectedFolderName = ""
                        if(len(self.fileList['FolderList']['FileNames']) == 1):
                            self.selectedFolderName = self.fileList['FolderList']['FileNames'][0]
                        
                        buttonEvent = True
                        break
                    elif btnName == "Print":
                        #GET FILE LIST POSITION
                        idx = self.listPosition % len(self.pickerList['FileNameBuffer'])
                        pickerCenterIdx = (self.interfaceLoader.GetPickerRowCount()//2 + idx) % len(self.pickerList['FileNameBuffer'])
                        self.selectedFileName = self.pickerList['FileNameBuffer'][pickerCenterIdx]
                        self.selectedFilePath = self.pickerList['FilePathBuffer'][pickerCenterIdx]
                        
                        print('Selected File: ', self.selectedFileName)
                        print('With path: ',self.selectedFilePath)
                        
                        self.interfaceState = 1
                        self.LoadInterfaceComponents()
                        self.StartTransfer()
                        
                        buttonEvent = True
                        break
                    elif btnName == "Cancel":
                        if(self.interfaceState == 1):
                            self.CancelTransfer()
                        elif(self.interfaceState == 2):
                            self.CancelHeating()
                        buttonEvent = True
                        break
                    
            if(event.type == pygame.MOUSEBUTTONUP and buttonEvent == False and self.interfaceState == 0):
                self.HandlePickerClick(event)
                


        
        return

    """*************************************************************************
                                update Method 
    
    Updates screen components
    *************************************************************************"""
    def update(self):
        
        #UPDATE TOP LABEL TEXT
        #IF IN FILE PICKER INTERFACE, CHANGE THE TOP LABEL ACORDING TO PICKER STATE 
        if(self.interfaceState == 0 and self.selectedFolderName == ''):
            self.lblTopText = 'Choose Drive'
        elif(self.interfaceState == 0 and self.selectedFolderName != ''):
            self.lblTopText = 'Choose GCode File'
        
        self.lblTop = self.lblTopFont.render(self.lblTopText, 1, self.lblTopFontColor)
        
        #UPDARE LABELS TEXT
        #self.lbl = []
        #for i in range(0,len(self.lblText)):
        #    self.lbl.append(self.lblFont[i].render(self.lblText[i], 1, self.lblFontColor[i]))
        
        #UPDATE BUTTONS
        for btn in self.buttons:
            btnName = btn._propGetName()
            if(self.interfaceState == 0):
                if(self.verifyGCode == True):
                    self.VerifySelectedFileType()
                
                if(btnName == 'Print' and self.selectedRoot == 'BTF'):
                    btn.visible = True
                elif(btnName == 'Print' and self.pickerList['Source'] == 'USB-Drives'):
                    btn.visible = False
                elif(btnName == 'Print' and self.pickerList['Source'] == 'USB-Folder'):
                    btn.visible = self.isGCodeFile
            else:
                btn.visible = True
        
        return

    """*************************************************************************
                                draw Method 
    
    Draws current screen
    *************************************************************************""" 
    def draw(self):
        
        #DRAW TOP LABELS
        self.screen.blit(self.lblTop, (self.interfaceLoader.GetTopLblXPos(self.interfaceState),
                                            self.interfaceLoader.GetTopLblYPos(self.interfaceState)))
        
        #DRAW LABELS
        #for i in range(0,len(self.lblText)):
        #    self.screen.blit(self.lbl[i], (self.interfaceLoader.GetlblTopXPos(self.interfaceState)[i],
        #                                    self.interfaceLoader.GetlblTopYPos(self.interfaceState)[i]))
        
        #DRAW BUTTONS
        for btn in self.buttons:
            btn.draw(self.screen)
            btnName = btn._propGetName()
            if (btnName == self.selectedRoot):
                pygame.draw.rect(self.screen, btn._propGetFgColor(), btn._propGetRect(), 3)
        
        """        
            FILE PICKER INTERFACE

        """
        if self.interfaceState == 0:
            #LOAD FILE PICKER CONFIGURATION
            x = self.interfaceLoader.GetPickerX()
            y = self.interfaceLoader.GetPickerY()
            width = self.interfaceLoader.GetPickerWidth()
            height = self.interfaceLoader.GetPickerHeight()
            pickerColor = self.interfaceLoader.GetPickerFontColor()
            fontSize = self.interfaceLoader.GetPickerFontSize()
            pickerFont = self.interfaceLoader.GetPickerFont()
            lblOffset = (height-fontSize)//2
            
            #EXTRACT LIST FROM FILELIST DICT
            self.pickerList = {}
            self.pickerList['FileNameBuffer'] = []
            self.pickerList['FilePathBuffer'] = []
            if(self.selectedRoot == 'USB'):
                if(self.selectedFolderName == ""):
                    self.pickerList['Source'] = 'USB-Drives'
                    self.pickerList['FileNameBuffer'] = self.fileList['FolderList']['FileNames']
                    self.pickerList['FilePathBuffer'] = self.fileList['FolderList']['FilePaths']
                else:
                    self.pickerList['Source'] = 'USB-Folder'
                    self.pickerList['FileNameBuffer'] = self.fileList[self.selectedFolderName]['FileNames']
                    self.pickerList['FilePathBuffer'] = self.fileList[self.selectedFolderName]['FilePaths']
            elif(self.selectedRoot == 'BTF'):
                self.pickerList['Source'] = 'BTF'
                self.pickerList['FileNameBuffer'] = self.fileList['BTF']['FileNames']
                self.pickerList['FilePathBuffer'] = self.fileList['BTF']['FilePaths']
            
            #CHECK IF THERE ARE MORE FILES THAN AVAILABLE PICKER LINES
            listRange = len(self.pickerList['FileNameBuffer'])
            if listRange >= self.interfaceLoader.GetPickerRowCount():
                listRange = self.interfaceLoader.GetPickerRowCount()
            
            #FILL AVAILABLE LINES WITH TEXT
            for i in range(0, listRange):
                
                #GET FILE PICKER POSITION
                pos = i + self.listPosition
            
                #CENTER POS OFFSET
                centerOffset = 0
                if(listRange < self.interfaceLoader.GetPickerRowCount()):
                    halfPicker = self.interfaceLoader.GetPickerRowCount()//2
                    topOffset = -(listRange-self.interfaceLoader.GetPickerRowCount())//2
                    centerOffset += halfPicker - topOffset
                
                #GET FILE LIST POSITION
                idx = pos % len(self.pickerList['FileNameBuffer'])
                
                #IF FILE NAME TOO LONG TRUNCATE
                fileName = self.pickerList['FileNameBuffer'][idx]
                lblStr = ''
                if len(fileName) > self.pickerStrLen:
                    lblStr += fileName[:self.pickerStrLen-3] + "..."
                else:
                    lblStr += fileName
                
                fileLbl = None
                yPos = 0
                
                #CENTER ITEM SHOULD BE WRITEN IN BOLD
                if ((i == listRange//2) and 
                        ((listRange >= self.interfaceLoader.GetPickerRowCount()) or (listRange < self.interfaceLoader.GetPickerRowCount()))):
                    fileLbl = pickerFont.render(lblStr, 1, pickerColor)

                else:
                    ff = FileFinder.FileFinder()
                    font = pygame.font.Font(ff.GetAbsPath("/Fonts/DejaVuSans-Light.ttf"),fontSize)
                    fileLbl = font.render(lblStr, 1, pickerColor)
                
                #CALCULATE Y POSITION AND OFFSET LABEL FROM BORDERS
                if listRange >= self.interfaceLoader.GetPickerRowCount():
                    yPos = y+lblOffset+((-1+i)*height)
                else:
                    #yPos = y+lblOffset+((-(halfPicker - topOffset)+i)*height)
                    yPos = y + lblOffset + height * (i - centerOffset)
                
                #DRAW FILE NAME LABEL
                self.screen.blit(fileLbl, (x + int(0.1*height),yPos))
                
            
            #DRAW CENTER FOCUS RECT
            self.pickFileRect = pygame.draw.rect(self.screen, pickerColor, (x,y,width,height), 3)
            """        
                FILE TRANSFER INTERFACE

            """
        elif self.interfaceState == 1:
            # Draw Image
            self.screen.blit(self.transfImg,(self.transfImgX,self.transfImgY))
            # Draw Progress Bar
            self.progressBar.DrawRect(self.screen)
            
            self.screen.blit(self.progressBar.GetSurface(self.blocksTransfered,self.nBlocks),
                                self.progressBar.GetPos())
            """        
                HEATING INTERFACE

            """
        elif self.interfaceState == 2:
            # Draw Image
            self.screen.blit(self.heatImg,(self.heatImgX,self.heatImgY))
            # Draw Progress Bar
            self.progressBar.DrawRect(self.screen)
            
            self.screen.blit(self.progressBar.GetSurface(self.nozzleTemperature,self.targetTemperature),
                                self.progressBar.GetPos())
                
        return
    
    """*************************************************************************
                                HandlePickerClick Method 
    
    Frees every element from memmory
    *************************************************************************""" 
    def HandlePickerClick(self,event):
        
        pos = pygame.mouse.get_pos()
        posX = pos[0]
        posY = pos[1]
        
        width = self.interfaceLoader.GetPickerWidth()
        height = self.interfaceLoader.GetPickerHeight()
        pickerXMin = self.interfaceLoader.GetPickerX()
        pickerXMax = pickerXMin + width
        pickerYMin = self.interfaceLoader.GetPickerY() - (self.interfaceLoader.GetPickerRowCount()/2 * height)
        pickerYMax = pickerYMin + (self.interfaceLoader.GetPickerRowCount() * height)
        
        idxChange = 0
        self.verifyGCode = False
        if (posX>pickerXMin) and (posX<pickerXMax) and (posY>pickerYMin) and (posY<pickerYMax):
                relY = (posY - self.interfaceLoader.GetPickerY())/(height/2)
                idxChange = int(relY//2)
                self.listPosition += idxChange
                self.verifyGCode = True
        
        #OPEN USB FOLDER
        if(idxChange == 0 and self.pickerList['Source'] == 'USB-Drives'):
            
            #GET FILE LIST POSITION
            idx = self.listPosition % len(self.pickerList['FileNameBuffer'])
            pickerCenterIdx = (self.interfaceLoader.GetPickerRowCount()//2 + idx) % len(self.pickerList['FileNameBuffer'])
            self.selectedFolderName = self.pickerList['FileNameBuffer'][pickerCenterIdx]
            self.draw()
            self.verifyGCode = True
        
        #TRANSFER FILER
        elif(idxChange == 0 and self.pickerList['Source'] == 'USB-Folder'):
            
            #GET FILE LIST POSITION
            idx = self.listPosition % len(self.pickerList['FileNameBuffer'])
            pickerCenterIdx = (self.interfaceLoader.GetPickerRowCount()//2 + idx) % len(self.pickerList['FileNameBuffer'])
            
            self.selectedFileName = self.pickerList['FileNameBuffer'][pickerCenterIdx]
            self.selectedFilePath = self.pickerList['FilePathBuffer'][pickerCenterIdx]
            """
            print('Selected File: ', self.selectedFileName)
            print('With path: ',self.selectedFilePath)
            
            self.interfaceState = 1
            self.LoadInterfaceComponents()
            self.StartTransfer()
            """
        
        return
    
    """*************************************************************************
                                VerifySelectedFileType Method 
    
    Frees every element from memmory
    *************************************************************************""" 
    def VerifySelectedFileType(self):
        
        pickerCenterIdx = self.interfaceLoader.GetPickerRowCount()//2 - 1
            
        self.selectedFileName = self.pickerList['FileNameBuffer'][pickerCenterIdx]
        self.selectedFilePath = self.pickerList['FilePathBuffer'][pickerCenterIdx]
        
        if(not os.path.isfile(self.selectedFilePath)):
            #print('file does not exits')
            self.isGCodeFile = False
        
        if(self.selectedFilePath.endswith('.gcode')):
            self.isGCodeFile = True
        
        self.verifyGCode = False
        
        return
    
    """*************************************************************************
                                GetCurrentScreenName Method 
    
    Frees every element from memmory
    *************************************************************************""" 
    def GetCurrentScreenName(self):
        
        return "Browser"
    
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
        
        #TRANSFERING FILE
        if(self.interfaceState == 1):
            startPos = self.totalBytes
            blockTransfered = False
            while(blockTransfered == False):
                blockTransfered = self.beeCmd.sendBlock(startPos,self.gcodeFile)
                if(blockTransfered is None):
                    print("Transfer aborted")
                    return False

                self.totalBytes += self.beeCmd.MESSAGE_SIZE
            
            self.blocksTransfered += 1
            print("   :","Transfered ", str(self.blocksTransfered), "/", str(self.nBlocks), " blocks ", self.totalBytes, "/", self.fileSize, " bytes")
            
            if(self.blocksTransfered >= self.nBlocks):
                #TRANSFERED ENDED
                self.EndTransfer()
            
        #HEATING
        elif(self.interfaceState == 2):
            currentTime = time()
            if(currentTime > self.nextPullTime):
                self.nozzleTemperature = self.beeCmd.GetNozzleTemperature()
                print('Nozzle Temperature: ', self.nozzleTemperature)
                
                if(self.nozzleTemperature >= self.targetTemperature):
                    self.nozzleTemperature = self.targetTemperature
                    
                    self.beeCmd.home()
                    self.beeCmd.startSDPrint();
                    return "Printing"
            
                self.nextPullTime = time() + self.pullInterval
        
            
        return 
    
    """*************************************************************************
                                StartTransfer Method 
    
    Initializes File Transfer
    *************************************************************************"""
    def StartTransfer(self):
        
        #check if file exists
        if(os.path.isfile(self.selectedFilePath) == False):
            print("File does not exist")
            return
        
        #Load File
        print("   :","Loading File")
        self.fileSize = os.path.getsize(self.selectedFilePath)
        print("   :","File Size: ", self.fileSize, "bytes")
        
        self.blockSize = self.beeCmd.MESSAGE_SIZE * self.beeCmd.BLOCK_SIZE
        self.nBlocks = math.ceil(self.fileSize/self.blockSize)
        print("   :","Number of Blocks: ", self.nBlocks)
        
        #RUN ESTIMATOR
        #TODO SEND M31 WITH ESTIMATED TIME
        
        fnSplit = self.selectedFileName.split(".")
        self.sdFileName = fnSplit[0]
        
        #CREATE SD FILE
        resp = self.beeCmd.CraeteFile(self.sdFileName)
        if(not resp):
            return
        
        #Start transfer
        self.blocksTransfered = 0
        self.totalBytes = 0
        
        self.startTime = time()
        
        self.gcodeFile = open(self.selectedFilePath, 'rb')
        
        self.beeCmd.transmisstionErrors = 0
        #START PRE-HEAT
        self.beeCmd.SetNozzleTemperature(self.targetTemperature)
        
        return
    
    """*************************************************************************
                                CancelTransfer Method 
    
    Cancels ongoing transfer
    *************************************************************************"""
    def CancelTransfer(self):
        
        self.cancelTransfer = False
        self.blocksTransfered = 0
        self.nBlocks = 0
        
        self.interfaceState = 0
        self.LoadInterfaceComponents()
        print('Transfer Canceled')
        
        #CANCEL HEATING
        self.beeCmd.SetNozzleTemperature(0)
        
        return
    """*************************************************************************
                                EndTransfer Method 
    
    Ends Transfer and starts Heating
    *************************************************************************"""
    def EndTransfer(self):
        
        elapsedTime = time()- self.startTime
        avgSpeed = self.fileSize//elapsedTime
        print("Elapsed time: ",elapsedTime)
        print("Average Transfer Speed: ", avgSpeed)
        
        #OPEN SD FILE
        resp = self.beeCmd.OpenFile(self.sdFileName)
        if(not resp):
            return
        
        print("Heating")
        #Heat Nozzle
        self.beeCmd.SetNozzleTemperature(self.targetTemperature)
        
        self.interfaceState = 2
        self.LoadInterfaceComponents()
        
        
        return
        
    """*************************************************************************
                                CancelHeating Method 
    
    Cancel Heating and return to file picker
    *************************************************************************"""
    def CancelHeating(self):
        
        self.beeCmd.SetNozzleTemperature(0)
        self.interfaceState = 0
        self.LoadInterfaceComponents()
        
        return
    
    """*************************************************************************
                                LoadInterfaceComponents Method 
    
    Updates interface components
    *************************************************************************"""
    def LoadInterfaceComponents(self):
        
        """
        Load new buttons and labels from interfaceLoader
        """
        self.lblTopFont = None
        self.lblTopFontColor = None
        self.lblTopText = None
        
        #self.lblFont = None
        #self.lblFontColor = None
        #self.lblText = None
        
        self.buttons = None
        
        self.lblTopFont = self.interfaceLoader.GetTopLblFont(self.interfaceState)
        self.lblTopFontColor = self.interfaceLoader.GetTopLblFontColor(self.interfaceState)
        self.lblTopText = self.interfaceLoader.GetToplblText(self.interfaceState)
        
        #self.lblFont = self.interfaceLoader.GetlblFont(self.interfaceState)
        #self.lblFontColor = self.interfaceLoader.GetlblFontColor(self.interfaceState)
        #self.lblText = self.interfaceLoader.GetlblText(self.interfaceState)
        
        self.buttons = self.interfaceLoader.GetButtonsList(self.interfaceState)
        
        return
       