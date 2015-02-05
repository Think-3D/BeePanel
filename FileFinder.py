#!/usr/bin/env python


r"""FileFinder - File hanfling Features.

This class exports some methods destined to find files and folder in the operating system

__init__()        Initializes current class
GetAbsPath() - a method that returns the absolute file path from the system.
LoadUSBFolders() - this methods locates USB devices and returns a list with them
FindLinuxUSBDevices() - this method locates and return the list of USB ass storage devices in linux environments
FindOSXUSBDevices() - this method locates and return the list of USB ass storage devices in OSX environments
"""


__author__ = "BEEVC - Electronic Systems"
__license__ = ""

import os
import platform
import subprocess

class FileFinder():
    
    absPath = None
    currentDir = None
    absDirPath = None
    
    homePath = None
    pSystem = None
    
    """*************************************************************************
    #                            Init Method 
    #
    #
    #************************************************************************"""
    def __init__(self):
        r"""
        FileFinder class initialization
        
        loads system folders path and platform type
        
        """
        pMachine = platform.machine()
        self.homePath = os.path.expanduser("~")

        if(pMachine == 'armv6l'):       #assume we're using a raspberri pi
            self.homePath = "/home/pi"
        
        self.currentDir = os.getcwd()
        
        self.pSystem = platform.system()
            
        return
    
    """*************************************************************************
    #                            GetAbsolutePath Method 
    #
    #
    #************************************************************************"""
    def GetAbsPath(self, relPath):
        r"""
        Get Absolute File path
        
        This method receives the name of the path to find
        
        and returns the absolute file path
        
        """
        
        path = self.homePath + "/BeePanel" + relPath
        
        return path
    
    """*************************************************************************
    #                            LoadUSBFolders Method 
    #
    #
    #************************************************************************"""
    def LoadUSBFolders(self):
        
        fileList = None
        
        pSystem = platform.system()
        
        if(pSystem == 'Darwin'):
            fileList = self.FindOSXUSBDevices()
        elif(pSystem == 'Linux'):
            fileList = self.FindLinuxUSBDevices()
        
        
        
        return fileList
    
    """*************************************************************************
    #                            FindOSXUSBDevices Method 
    #
    #
    #************************************************************************"""
    def FindOSXUSBDevices(self):
        
        fileList = {}
        
        folders = os.listdir('/Volumes/')
        
        fileList['FolderList'] = {}
        fileList['FolderList']['FileNames'] = []
        fileList['FolderList']['FilePaths'] = []
        for f in folders:
            folderName = f
            folderPath = '/Volumes/' + f
            fileList['FolderList']['FileNames'].append(folderName)
            fileList['FolderList']['FilePaths'].append(folderPath)
            folderFiles = [file for file in os.listdir(folderPath) if file.endswith('.gcode')]
            fileList[f] = {}
            fileList[f]['FileNames'] = []
            fileList[f]['FilePaths'] = []
            for folderFile in folderFiles:
                filePath = folderPath + '/' + folderFile
                fileList[f]['FileNames'].append(folderFile)
                fileList[f]['FilePaths'].append(filePath)
                #fileList[f].append([[folderPath],[folderFile,filePath]])
            
        
        return fileList
    
    """*************************************************************************
    #                            FindLinuxUSBDevices Method 
    #
    #
    #************************************************************************"""
    def FindLinuxUSBDevices(self):
        
        fileList = {}
        fileList['FolderList'] = {}
        fileList['FolderList']['FileNames'] = []
        fileList['FolderList']['FilePaths'] = []
        fileList['FolderList']['DevNames'] = []
        
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
                        fileList['FolderList']['DevNames'].append(devName)
                        fileList['FolderList']['FileNames'].append(devName)
                        #GET CORRESPONDING PATH
                        mountsFile = open("/proc/mounts")
                        linesMount = mountsFile.readlines()
                        for l in linesMount:
                            wordsMounts = [y.strip() for y in l.split()]
                            if(devName in wordsMounts[0]):
                                fileList['FolderList']['FilePaths'].append(wordsMounts[1])
        
        
        for i in range(len(fileList['FolderList']['FileNames'])):
            folderPath = fileList['FolderList']['FilePaths'][i]
            f = fileList['FolderList']['FileNames'][i]
            folderFiles = [file for file in os.listdir(folderPath) if file.endswith('.gcode')]
            fileList[f] = {}
            fileList[f]['FileNames'] = []
            fileList[f]['FilePaths'] = []
            for folderFile in folderFiles:
                filePath = folderPath + '/' + folderFile
                fileList[f]['FileNames'].append(folderFile)
                fileList[f]['FilePaths'].append(filePath)
        
        return fileList 