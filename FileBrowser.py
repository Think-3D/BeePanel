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

class FileBrowserScreen():
    
    exit = False
    interfaceState = 0
    
    lblTopText = None           #list for top label text
    lblTop = None               #Top label object
    lblTopFont = None           #Top label font
    lblTopFontColor = None      #top label color
    
    lblText = None           #list for label text
    lbl = None               #label object
    lblFont = None           #label font
    lblFontColor = None      #label color
    
    buttons = None              #list for interface buttons
    
    selectedRoot = "USB"
    selctedRootRect = None
    usbOpened = False
    
    cancelTransfer = False
    initTransfer = False
    blocksTransfered = 0
    nBlocks = 0
    
    startPrint = False
    
    """
    File Picker
    """
    fileList = None
    pickFileRect = None        #Rect for selected color
    listPosition = 0
    selectedFileIdx = 0
    pickerStrLen = 20
    usbDev = None
    usbPaths = None
    usbNames = None
    selPickerName = None
    pickerLabels = []
    selectedFileName = None
    selectedFolderName = ""
    selectedGCode = False
    
    pickerStateChanged = True
    
    """
    Slicer
    """
    ready2Print = False
    selectedRes = "ResLow"
    selectedFill = "FillLow"
    pullInterval = 1         #pull interval for simulation mode
    nextPullTime = None
    
    """
    Images
    """
    slicingImgPath = None
    transfImgPath = None
    heatImgPath = None
    
    slicingImgX = 0
    slicingImgY = 0
    
    transfImgX = 0
    transfImgY = 0
    
    heatImgX = 0
    heatImgY = 0
    
    """
    Heating vars
    """
    targetTemperature = 220     
    nozzleTemperature = 0
    
    """
    Progress Bar vars
    """
    progressBar = None
    pBarRect = None
    pBarFill = None
    
    """
    BEEConnect vars
    """
    #conn = None
    beeCon = None
    beeCmd = None
    
    exitNeedsHoming = True
    exitCallBackResp = None
    
    """*************************************************************************
                                Init Method 
    
    Inits current screen components
    *************************************************************************"""
    def __init__(self, screen, interfaceLoader, cmd):
        """
        .
        """
        print("Loading File Browser Screen Components")
        
        self.beeCmd = cmd
        self.beeCon = self.beeCmd.beeCon
        
        self.firstNextReady = False
        self.ready2Print = False
        
        self.screen = screen
        self.interfaceLoader = interfaceLoader
        
        self.interfaceState = 0         #reset interface state
        
        self.cancelTransfer = False
        self.initTransfer = False
        
        self.pickerStateChanged = True
        
        """
        Load lists and settings from interfaceLoader
        """
        self.lblTopFont = self.interfaceLoader.GetTopLblFont(self.interfaceState)
        self.lblTopFontColor = self.interfaceLoader.GetTopLblFontColor(self.interfaceState)
        self.lblTopText = self.interfaceLoader.GetToplblText(self.interfaceState)
        
        self.lblFont = self.interfaceLoader.GetlblFont(self.interfaceState)
        self.lblFontColor = self.interfaceLoader.GetlblFontColor(self.interfaceState)
        self.lblText = self.interfaceLoader.GetlblText(self.interfaceState)
        
        self.buttons = self.interfaceLoader.GetButtonsList(self.interfaceState)
        
        #PROGRESS BAR
        self.progressBar = self.interfaceLoader.GetProgessBar()
        
        #FILE LIST
        self.LoadFileList("USB")
        #Verify if there is onlu one USB drive
        if(len(self.fileList) == 1):
            self.LoadFileList(self.usbPaths[0])
            self.selectedFolderName = self.usbPaths[0]
            self.usbOpened = True
        
        self.pickerStrLen = self.interfaceLoader.GetPickerStrLen()
        
        self.slicingImg = pygame.image.load(self.interfaceLoader.GetSlicingImgPath())
        self.transfImg = pygame.image.load(self.interfaceLoader.GetTransfImgPath())
        self.heatImg = pygame.image.load(self.interfaceLoader.GetHeatImgPath())
        
        self.slicingImgX = self.interfaceLoader.GetSlicingImgX()
        self.slicingImgY = self.interfaceLoader.GetSlicingImgY()
        
        self.transfImgX = self.interfaceLoader.GetTransfImgX()
        self.transfImgY = self.interfaceLoader.GetTransfImgY()
        
        self.heatImgX = self.interfaceLoader.GetHeatImgX()
        self.heatImgY = self.interfaceLoader.GetHeatImgY()
        
        self.nextPullTime = time() + self.pullInterval
        
        return

    """*************************************************************************
                                handle_events Method 
    
    Received the event vector and checks if it has any event from interface items
    *************************************************************************"""
    def handle_events(self,retVal):
        """handle all events."""
        for event in retVal:
            
            #VERIFY IF THE EVENT CAME FROM GUI BUTTONS
            for btn in self.buttons:
                if 'click' in btn.handleEvent(event):
                    btnName = btn._propGetName()
                    
                    if btnName == "Up":
                        self.listPosition = self.listPosition - 1
                    elif btnName == "Down":
                        self.listPosition = self.listPosition + 1
                    elif btnName == "BTF":
                        #clear whole screen
                        self.screen.fill(pygame.Color(255,255,255))
                        self.fileList = ['Please Wait','Loading...']
                        self.update()
                        self.draw()
                        # update screen
                        pygame.display.update()
                        
                        self.listPosition = 0
                        self.LoadFileList("BTF")
                        self.selectedRoot = btnName
                        self.pickerStateChanged = True
                    elif btnName == "USB":
                        self.LoadFileList("USB")
                        self.usbOpened = False
                        self.loadUSBDevices = True
                        self.selectedFolderName = ""
                        #Verify if there is onlu one USB drive
                        if(len(self.fileList) == 1):
                            self.LoadFileList(self.usbPaths[0])
                            self.selectedFolderName = self.usbPaths[0]
                            self.usbOpened = True
                        
                        self.selectedGCode = False
                        self.selectedRoot = btnName
                        
                    elif btnName == "Next":
                        self.selectedFileIdx = (2+self.listPosition) % len(self.fileList)
                        self.selectedFileName = self.fileList[self.selectedFileIdx]
                        if self.selectedFileName.endswith(".stl"):
                            self.interfaceState = self.interfaceState + 1
                        elif self.selectedFileName.endswith(".gcode"):
                            self.interfaceState = self.interfaceState + 3
                            self.initTransfer = True
                            if(self.selectedRoot == "USB"):
                                self.transferFile(self.selectedFileName)
                            elif(self.selectedRoot == "BTF"):
                                pass
                        
                        print("Selected: ",self.selectedFileName)
                    elif btnName == "ResLow":
                        self.selectedRes = btnName
                        print('Click')
                    elif btnName == "ResMed":
                        self.selectedRes = btnName
                    elif btnName == "ResHigh":
                        self.selectedRes = btnName
                    elif btnName == "FillLow":
                        self.selectedFill = btnName
                    elif btnName == "FillMed":
                        self.selectedFill = btnName
                    elif btnName == "FillHigh":
                        self.selectedFill = btnName
                    elif btnName == "Slice":
                        print("Start Slicing with ", self.selectedRes, " and ", self.selectedFill)
                        self.interfaceState = self.interfaceState + 1
                        self.nextPullTime = time() + self.pullInterval
                        self.ready2Print = False
                        
                    elif btnName == "Cancel":
                        self.cancelTransfer = True
                        self.interfaceState = 0
                    elif btnName == "Print":
                        self.interfaceState = 3
                        
                    """
                    Load new buttons and labels from interfaceLoader
                    """
                    self.lblTopFont = None
                    self.lblTopFontColor = None
                    self.lblTopText = None
                    
                    self.lblFont = None
                    self.lblFontColor = None
                    self.lblText = None
                    
                    self.buttons = None
                    
                    self.lblTopFont = self.interfaceLoader.GetTopLblFont(self.interfaceState)
                    self.lblTopFontColor = self.interfaceLoader.GetTopLblFontColor(self.interfaceState)
                    self.lblTopText = self.interfaceLoader.GetToplblText(self.interfaceState)
                    
                    self.lblFont = self.interfaceLoader.GetlblFont(self.interfaceState)
                    self.lblFontColor = self.interfaceLoader.GetlblFontColor(self.interfaceState)
                    self.lblText = self.interfaceLoader.GetlblText(self.interfaceState)
                    
                    self.buttons = self.interfaceLoader.GetButtonsList(self.interfaceState)
            
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                #VERIFY IF THE USER SELECTED A FOLDE OR FILE
                #IF A FILE IS SELECTED UPDATE THE LIST LABELS POSITION
                #IF A FOLSER IS SELECTED UPDATE FILE LIST
                if(self.GetPickerSelectedFolder(event)):
                    self.GetSelectedIdx(event)
                self.pickerStateChanged = True
                        
            event = None
        
        return

    """*************************************************************************
                                update Method 
    
    Updates screen components
    *************************************************************************"""
    def update(self):
        
        #UPDATE TOP LABEL TEXT
        self.lblTop = self.lblTopFont.render(self.lblTopText, 1, self.lblTopFontColor)
        
        #UPDARE LABELS TEXT
        self.lbl = []
        for i in range(0,len(self.lblText)):
            self.lbl.append(self.lblFont[i].render(self.lblText[i], 1, self.lblFontColor[i]))
        
        #UPDATE BUTTONS
        for btn in self.buttons:
            #FILE BROWSER INTERFACE
            if self.interfaceState == 0:
                if(self.selectedRoot == "USB"):
                    if(btn._propGetName() == "Next"):
                        btn.visible = self.selectedGCode
                else:
                    btn.visible = True
            elif self.interfaceState == 2:
                if btn._propGetName() == "Print":
                    btn.visible = self.ready2Print
                else:
                    btn.visible = True
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
        for i in range(0,len(self.lblText)):
            self.screen.blit(self.lbl[i], (self.interfaceLoader.GetlblTopXPos(self.interfaceState)[i],
                                            self.interfaceLoader.GetlblTopYPos(self.interfaceState)[i]))
        #DRAW BUTTONS
        for btn in self.buttons:
            btn.draw(self.screen)
            btnName = btn._propGetName()
            if (btnName == self.selectedRoot) or (btnName == self.selectedRes) or (btnName == self.selectedFill):
                pygame.draw.rect(self.screen, btn._propGetFgColor(), btn._propGetRect(), 3)
        
        """        
            FILE PICKER INTERFACE
        """
        self.pickerLabels = []
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
            
            #CHECK IF THERE ARE MORE FILES THAN AVAILABLE PICKER LINES
            listRange = len(self.fileList)
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
                idx = pos % len(self.fileList)
                
                #IF FILE NAME TOO LONG TRUNCATE
                fileName = self.fileList[idx]
                lblStr = ""
                if(self.selectedFolderName == "" and self.selectedRoot == "USB"):
                    lblStr = "USB:"

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
                    #Update selected label
                    self.selPickerName = fileName
                    #Verify if a picker change occurred
                    if(self.pickerStateChanged):
                        self.isGcodeFile(self.selPickerName)
                        self.pickerStateChanged = False
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
                self.pickerLabels.append(fileName)

                #DRAW LINES SEPARATING ENTRIES IF ENOUGH LINES
                if (i>0 and i<listRange and self.interfaceLoader.GetPickerRowCount() > 3):
                    pygame.draw.line(self.screen, pickerColor, (x, y+((-2+i)*height)),
                                (x+width, y+((-2+i)*height)), int(0.05*height))
                    
                
            #DRAW CENTER FOCUS RECT
            self.pickFileRect = pygame.draw.rect(self.screen, pickerColor, (x,y,width,height), 3)
            
            
        
        #SLICE INTERFACE
        elif self.interfaceState == 2:
            # Draw Image
            self.screen.blit(self.slicingImg,(self.slicingImgX,self.slicingImgY))
        
        #TRANSFERING INTERFACE
        elif self.interfaceState == 3:
            # Draw Image
            self.screen.blit(self.transfImg,(self.transfImgX,self.transfImgY))
            # Draw Progress Bar
            self.progressBar.DrawRect(self.screen)
            
            self.screen.blit(self.progressBar.GetSurface(self.blocksTransfered,self.nBlocks),
                                self.progressBar.GetPos())
        #HEATING
        elif self.interfaceState == 4:
            # Draw Image
            self.screen.blit(self.heatImg,(self.heatImgX,self.heatImgY))
            # Draw Progress Bar
            self.progressBar.DrawRect(self.screen)
            self.screen.blit(self.progressBar.GetSurface(self.nozzleTemperature,self.targetTemperature),
                                self.progressBar.GetPos())
        
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
        
        self.interfaceState = None
        self.lblTopText = None
        self.lblTop = None
        self.lblTopFont = None
        self.lblTopFontColor = None
        self.lblText = None
        self.lbl = None
        self.lblFont = None
        self.lblFontColor = None
        self.buttons = None
        self.selectedRoot = None
        self.selctedRootRect = None
        self.fileList = None
        self.pickFileRect = None
        self.listPosition = None
        self.selectedFileIdx = None
        self.pickerStrLen = None
        self.usbDev = None
        self.usbPaths = None
        self.usbNames = None
        self.selectedFileName = None
        self.ready2Print = None
        self.selectedRes = None
        self.selectedFill = None
        self.pullInterval = None
        self.nextPullTime = None
        self.slicingImgPath = None
        self.transfImgPath = None
        self.heatImgPath = None
        self.slicingImgX = None
        self.slicingImgY = None
        self.transfImgX = None
        self.transfImgY = None
        self.heatImgX = None
        self.heatImgY = None
        
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
        
        t = time()
        if t > self.nextPullTime:
            #self.ready2Print = True
            
            if(self.interfaceState == 4):
                self.nozzleTemperature = self.beeCmd.GetNozzleTemperature()
                if(self.nozzleTemperature >= self.targetTemperature):
                    self.nozzleTemperature = self.targetTemperature
                    if(self.startPrint == True):
                        self.startPrint = False
                        self.beeCmd.home()
                        self.beeCmd.startSDPrint();
                    
            
            self.nextPullTime = time() + self.pullInterval
            
        if(self.interfaceState == 3):
            if(self.initTransfer == True):
                self.blocksTransfered = 0
                self.nBlocks = 0
                return "Transfer"
                #self.transferFile(self.selectedFileName)
            
        return 
    
    """*************************************************************************
                                GetSelectedIdx Method 
    
    Identifies which color the user chose by clicking the list
    *************************************************************************""" 
    def GetSelectedIdx(self, event):        
        
        if self.interfaceState ==0:
            pos = pygame.mouse.get_pos()
            posX = pos[0]
            posY = pos[1]
            
            width = self.interfaceLoader.GetPickerWidth()
            height = self.interfaceLoader.GetPickerHeight()
            pickerXMin = self.interfaceLoader.GetPickerX()
            pickerXMax = pickerXMin + width
            pickerYMin = self.interfaceLoader.GetPickerY() - (2 * height)
            pickerYMax = pickerYMin + (5 * height)
            
            if (posX>pickerXMin) and (posX<pickerXMax) and (posY>pickerYMin) and (posY<pickerYMax):
                relY = posY - pickerYMin
                idxChange = -2 + int(relY/height)
                self.listPosition += idxChange
        
        return 
    
    """*************************************************************************
                                LoadFileList Method 
    
    Loads the file list in the directory with the selected fileType
    *************************************************************************""" 
    def LoadFileList(self, directory):
        
        self.fileList = []
        
        if(directory == "BTF"):
            print("loading BTF files")
            self.fileList = self.beeCmd.getFileList()
        elif(directory == "USB"):
            self.fileList = self.FindUSBDrives()
        else:
            self.fileList = [file for file in os.listdir(directory) if file.endswith('.gcode')]
                            
        return

    """*************************************************************************
                                FindUSBDrives Method 
    
    
    *************************************************************************"""
    def FindUSBDrives(self):
        self.usbDev = []
        self.usbPaths = []
        self.usbNames = []
        
        partitionsFile = open("/proc/partitions")
        lines = partitionsFile.readlines()[2:]#Skips the header lines
        
        #SEARCH PARTITIONS FOR USB DRIVES
        for line in lines:
            
            words = [x.strip() for x in line.split()]
            minorNumber = int(words[1])
            deviceName = words[3]
            
            #USB DRIVES ALLWAYS HAVE MINOR MULTIPLE OF 16
            if minorNumber % 16 == 0:
                path = "/sys/class/block/" + deviceName
                if os.path.islink(path):
                    
                    #VERIFY IF DEVICE IS CONNECTED THROUGH USB
                    if os.path.realpath(path).find("/usb") > 0:
                        devName = "/dev/%s" % deviceName
                        self.usbDev.append(devName)
                        
                        #GET CORRESPONDING PATH
                        mountsFile = open("/proc/mounts")
                        linesMount = mountsFile.readlines()
                        for l in linesMount:
                            wordsMounts = [y.strip() for y in l.split()]
                            if(devName in wordsMounts[0]):
                                self.usbPaths.append(wordsMounts[1])
                        
                                #GET CORRESPONDING NAME
                                blkid = subprocess.check_output("blkid", universal_newlines=True)
                                blkidLines = blkid.split('\n')
                                for b in blkidLines:
                                    bWords = [z.strip() for z in b.split()]
                                    if(len(bWords) > 0):
                                        if(devName in bWords[0]):
                                            leftSplit = b.split('LABEL="')
                                            rightSplit = leftSplit[1].split('" UUID')
                                            self.usbNames.append(rightSplit[0] + "/")
                                            break
                                if(len(self.usbNames) != len(self.usbPaths)):
                                    folderName = wordsMounts[1].split('/')
                                    self.usbNames.append(folderName[len(folderName)-1] + "/")
                                break
                                
            
            
        return self.usbNames

    """*************************************************************************
                                transferFile Method 
    
    Transfers Gcode file to R2C2
    *************************************************************************""" 
    def transferFile(self, filename):
        
        selectedFilePath = self.selectedFolderName + "/" + filename
        
        self.initTransfer = False
        self.startPrint = False
        
        #check if file exists
        if(os.path.isfile(selectedFilePath) == False):
            print("File does not exist")
            return
        
        #Load File
        print("   :","Loading File")
        #f = open(selectedFilePath, 'rb')
        fSize = os.path.getsize(selectedFilePath)
        print("   :","File Size: ", fSize, "bytes")
        
        blockBytes = self.beeCmd.MESSAGE_SIZE * self.beeCmd.BLOCK_SIZE
        self.nBlocks = math.ceil(fSize/blockBytes)
        print("   :","Number of Blocks: ", self.nBlocks)
        
        
        
        #TODO SEND M31 WITH ESTIMATED TIME
        
        fnSplit = filename.split(".")
        sdFN = fnSplit[0]
        
        #CREATE SD FILE
        resp = self.beeCmd.CraeteFile(sdFN)
        if(not resp):
            return
        
        #Start transfer
        self.blocksTransfered = 0
        totalBytes = 0
        
        startTime = time()
        
        #Load local file
        with open(selectedFilePath, 'rb') as f:

            self.beeCmd.transmisstionErrors = 0

            while(self.blocksTransfered < self.nBlocks):
                
                startPos = totalBytes
                #endPos = totalBytes + blockBytes
                
                #bytes2write = endPos - startPos
                
                #if(self.blocksTransfered == self.nBlocks -1):
                #    endPos = fSize
                    
                blockTransfered = False
                while(blockTransfered == False):
                    blockTransfered = self.beeCmd.sendBlock(startPos,f)
                    if(blockTransfered is None):
                        print("Transfer aborted")
                        return False

                    #print(resp)
                    totalBytes += self.beeCmd.MESSAGE_SIZE
                
                self.blocksTransfered += 1
                retVal = pygame.event.get()
                self.handle_events(retVal)
                self.Pull()
                self.draw()
                self.update()
                
                print("   :","Transfered ", str(self.blocksTransfered), "/", str(self.nBlocks), " blocks ", totalBytes, "/", fSize, " bytes")
            
        print("   :","Transfer completed")
        
        elapsedTime = time()- startTime
        avgSpeed = fSize//elapsedTime
        print("Elapsed time: ",elapsedTime)
        print("Average Transfer Speed: ", avgSpeed)
        
        #OPEN SD FILE
        resp = self.beeCmd.OpenFile(sdFN)
        if(not resp):
            return
        
        print("Heating")
        #Heat Nozzle
        self.beeCmd.SetNozzleTemperature(self.targetTemperature)
        self.startPrint = True
        
        print("Start printing")
        
        self.interfaceState = 4
        
        return
    
    """*************************************************************************
                                GetPickerSelectedEntry Method 
    
    
    *************************************************************************""" 
    def GetPickerSelectedFolder(self, event):
        
        
        #VERIFY IF THE GUI IS SHOWING THE FILE PICKER
        if self.interfaceState == 0:
            
            pos = pygame.mouse.get_pos()
            posX = pos[0]
            posY = pos[1]
            
            width = self.interfaceLoader.GetPickerWidth()
            height = self.interfaceLoader.GetPickerHeight()
            pickerXMin = self.interfaceLoader.GetPickerX()
            pickerXMax = pickerXMin + width
            pickerYMin = self.interfaceLoader.GetPickerY() - (2 * height)
            pickerYMax = pickerYMin + (5 * height)
            
            
            if (posX>pickerXMin) and (posX<pickerXMax) and (posY>pickerYMin) and (posY<pickerYMax):
                relY = posY - pickerYMin
                pickerPos = 1 - relY//height
                
                #IF WE'RE BROWSING THE USB (!BTF) THE INITIAL ROOT == USB 
                if(self.selectedRoot != "BTF" and self.selectedRoot == "USB" and self.usbOpened == False):
                    
                    if(len(self.usbNames) <=1 ):
                        #self.LoadFileList(self.usbPaths[0])
                        return
                    #Get initial path for selected drive
                    try:
                        selPath = self.GetUSBDrivePath(self.pickerLabels[pickerPos][:-1])
                        self.selectedFolderName = selPath
                        #RELOAD FILE LIST
                        self.LoadFileList(self.selectedFolderName)
                    except:
                        self.LoadFileList("USB")
                    
                    return True
            
            
        return True
    
    """*************************************************************************
                                GetUSBDrivePath Method 
    
    
    *************************************************************************""" 
    def GetUSBDrivePath(self, dName):
        
        for i in range(len(self.usbNames)):
            if(dName in self.usbNames[i]):
                return self.usbPaths[i]
            
        return None
    
    """*************************************************************************
                                isGcodeFile Method 
    
    
    *************************************************************************""" 
    def isGcodeFile(self, fName):
        
        #IF SEARCHING BTF FILES IGNORE AND EXIT
        if(self.selectedRoot == "BTF"):
            self.selectedGCode = False
            return True
        
        #IF THERE IS NO DRIVE SEELCTED, DISABLE PRINT AND EXIT
        if(self.selectedFolderName == ""):
            self.selectedGCode = False
            return False
        
        try:
            selectedFilePath = self.selectedFolderName + "/" + self.selPickerName
        except:
            selectedFilePath = ""
        
        #VERIFY IF FILE EXISTS
        if(not os.path.isfile(selectedFilePath)):
            print("File does not exist: ", selectedFilePath)
            self.selectedGCode = False
            return False
        
        print("isGcode: ", selectedFilePath)
        self.selectedGCode = True
        
        return True
    
    
    