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

r"""

BeePanelJsonLoadder Class

This class is responsible for loading the interface loaders with the correct
json configuration file

This class exports the following methods:

__init__()            Initializes current class
GetLeftMenuLoader()     returns LeftMenuInterface Object
GetPrinterInfoLoader()     returns PrinterInfoInterface Object
GetJogLoader()         returns JogInterface Object
GetCalibrationLoader()     returns CalibrationInterface Object
GetSettingsLoader()     returns SettingsInterface Object
GetFileBrowserLoader()     returns FileBrowserInterface Object
GetAboutLoader()     returns AboutInterface Object
GetPrintingLoader()     returns PrintingInterface Object

GetDefaultScreen()        returns default start screen Name
"""


__author__ = "BVC Electronic Solutions"
__license__ = ""


import json
import BeePanelDisplay
import FileFinder

import Loaders.AboutLoader as AboutLoader
import Loaders.CalibrationLoader as CalibrationLoader
import Loaders.FilamentChangeLoader as FilamentChangeLoader
import Loaders.FileBrowserLoader as FileBrowserLoader
import Loaders.JogLoader as JogLoader
import Loaders.LeftMenuLoader as LeftMenuLoader
import Loaders.PrinterInfoLoader as PrinterInfoLoader
import Loaders.PrintingLoader as PrintingLoader
import Loaders.SettingsLoader as SettingsLoader


class jsonLoader():
    
    """
    Json vars
    """
    
    displayJsonPath = "/Json/DisplayConfig.json"
    leftMenuJsonPath = "/Json/LeftMenuButtonsConfiguration.json"
    printerInfoJsonPath = "/Json/PrinterInfoConfiguration.json"
    jogJsonPath = "/Json/JogConfiguration.json"
    calibrationJsonPath = "/Json/CalibrationConfiguration.json"
    filamentChangeJsonPath = "/Json/FilamentChangeConfiguration.json"
    settingsJsonPath = "/Json/SettingsConfiguration.json"
    fileBrowserJsonPath = "/Json/FileBrowserConfiguration.json"
    aboutJsonPath = "/Json/AboutConfiguration.json"
    printingJsonPath = "/Json/PrintingConfiguration.json"
    
    """
    Display Configuration class
    """
    displayData = None
    display = None
    displayObject = None
    
    """
    Left Menu Configuration
    """
    leftMenu = []
    leftMenuButtons = []
    defaultScreen = ""
    leftMenuLoader = None
    
    """
    Interface Configuration
    """
    printerInfoInterface = None
    jogInterface = None
    calibrationInterface = None
    filamentChangeInterface = None
    settingsInterface = None
    fileBrowserInterface = None
    aboutInterface = None
    
    printingInterface = None
    
    """*************************************************************************
                                Init Method 
    
    *************************************************************************"""
    def __init__(self):
        r"""
        __init__ method
        
        This method loads every interface loader and its interfaces objects
        """
    
        ff = FileFinder.FileFinder()
        
        """
        Get Display Configuration
        """
        f = open(ff.GetAbsPath(self.displayJsonPath),'r')                      #load json as text file
        displayData = json.load(f)                              #parse the json file
        self.display = displayData.get('display')               #get the display list from json file
        displayJson = json.loads(json.dumps(self.display[0]))
        self.defaultScreen = displayJson['DefaultScreen']
        self.displayObject = BeePanelDisplay.Display(
                displayJson['Name'],
                int(displayJson['Width']),
                int(displayJson['Height']),
                displayJson['bgColor'],
                int(displayJson['SplitLinePos']),
                displayJson['SplitLineColor'],
                int(displayJson['SplitLineThickness']))
        
        f.close()                                                   #close the file
        
        """
        Get Left Menu Buttons Configuration
        """
        f = open(ff.GetAbsPath(self.leftMenuJsonPath),'r')                          #load json as text file
        menuData = json.load(f)                                     #parse the json file
        self.leftMenuLoader = LeftMenuLoader.LeftMenuLoader(menuData)
        f.close()                                                   #close the file
            
        """
        Get Printer Info Interface Configuration
        """
        f = open(ff.GetAbsPath(self.printerInfoJsonPath),'r')                          #load json as text file
        printerInfoData = json.load(f)                              #parse the json file
        printerInfo = printerInfoData['PrinterInfo']                #Get Printer Info
        printerInfoJson = json.loads(json.dumps(printerInfo[0]))    #Convert text to json
        self.printerInfoInterface = PrinterInfoLoader.PrinterInfoLoader(printerInfoJson)    #create interface
        f.close()                                                   #close the file
        
        """
        Get Jog Interface Configuration
        """
        f = open(ff.GetAbsPath(self.jogJsonPath),'r')                          #load json as text file
        jogData = json.load(f)                                     #parse the json file
        jog = jogData['Jog']                #Get Jog configuration text
        jogJson = json.loads(json.dumps(jog[0]))    #Convert text to json
        self.jogInterface = JogLoader.JogLoader(jogJson)    #create interface
        f.close()                                            #close the file
        
        """
        Get Calibration Interface Configuration
        """
        f = open(ff.GetAbsPath(self.calibrationJsonPath),'r')                          #load json as text file
        calibrationData = json.load(f)                                     #parse the json file
        calibration = calibrationData['Calibration']                #Get Calibration configuration text
        calibrationJson = json.loads(json.dumps(calibration[0]))    #Convert text to json
        self.calibrationInterface = CalibrationLoader.CalibrationLoader(calibrationJson)    #create interface
        f.close()                                            #close the file
        
        """
        Get Filament Change Interface Configuration
        """
        f = open(ff.GetAbsPath(self.filamentChangeJsonPath),'r')                          #load json as text file
        filamentChangeData = json.load(f)                                     #parse the json file
        filamentChange = filamentChangeData['FilamentChange']                #Get Filament Chnage configuration text
        filamentChangeJson = json.loads(json.dumps(filamentChange[0]))    #Convert text to json
        self.filamentChangeInterface = FilamentChangeLoader.FilamentChangeLoader(filamentChangeJson)    #create interface
        f.close()                                            #close the file
        
        """
        Get Settings Interface Configuration
        """
        f = open(ff.GetAbsPath(self.settingsJsonPath),'r')                            #load json as text file
        settingsData = json.load(f)                                    #parse the json file
        settings = settingsData['Settings']                                  #Get Settings configuration text
        settingsJson = json.loads(json.dumps(settings[0]))                #Convert text to json
        self.settingsInterface = SettingsLoader.SettingsLoader(settingsJson)    #create interface
        f.close()                                                   #close the file
        
        """
        Get File Browser Interface Configuration
        """
        f = open(ff.GetAbsPath(self.fileBrowserJsonPath),'r')                          #load json as text file
        fileBrowserData = json.load(f)                                     #parse the json file
        fileBrowser = fileBrowserData['FileBrowser']                #Get File Browser configuration text
        fileBrowserJson = json.loads(json.dumps(fileBrowser[0]))    #Convert text to json
        self.fileBrowserInterface = FileBrowserLoader.FileBrowserLoader(fileBrowserJson)    #create interface
        f.close()                                            #close the file
        
        """
        Get About Interface Configuration
        """
        f = open(ff.GetAbsPath(self.aboutJsonPath),'r')                            #load json as text file
        aboutData = json.load(f)                                    #parse the json file
        about = aboutData['About']                                  #Get About configuration text
        aboutJson = json.loads(json.dumps(about[0]))                #Convert text to json
        self.aboutInterface = AboutLoader.AboutLoader(aboutJson)    #create interface
        f.close()                                                   #close the file
        
        """
        Get About Interface Configuration
        """
        f = open(ff.GetAbsPath(self.printingJsonPath),'r')                            #load json as text file
        printingData = json.load(f)                                    #parse the json file
        printing = printingData['Printing']                                  #Get About configuration text
        printingJson = json.loads(json.dumps(printing[0]))                #Convert text to json
        self.printingInterface = PrintingLoader.PrintingLoader(printingJson)    #create interface
        f.close()                                                   #close the file
        
        return
    
    """*************************************************************************
                                GetLeftMenuLoader Method 
    
    *************************************************************************"""
    def GetLeftMenuLoader(self):
        r"""
        GetLeftMenuLoader method
        
        returns LeftMenuLoader Object
        """
        
        return self.leftMenuLoader
    
    """*************************************************************************
                                GetPrinterInfoInterface Method 
    
    *************************************************************************"""
    def GetPrinterInfoInterface(self):
        r"""
        GetPrinterInfoInterface method
        
        returns PrinterInfo Interface object
        """
        return self.printerInfoInterface
    
    """*************************************************************************
                                GetJogInterface Method 
    
    *************************************************************************"""
    def GetJogInterface(self):
        r"""
        GetJogInterface method
        
        returns Jog Interface Object
        """
        
        return self.jogInterface
    
    """*************************************************************************
                                GetCalibrationInterface Method 
    
    *************************************************************************"""
    def GetCalibrationInterface(self):
        r"""
        GetCalibrationInterface method
        
        returns Calibration Interface Object
        """
        
        return self.calibrationInterface
    
    """*************************************************************************
                                GetFilamentChangeInterface Method 
    
    *************************************************************************"""
    def GetFilamentChangeInterface(self):
        r"""
        GetFilamentChangeInterface method
        
        returns FilamentChange Interface Object
        """
        
        return self.filamentChangeInterface
    
    """*************************************************************************
                                GetSettingsInterface Method 
    
    *************************************************************************"""
    def GetSettingsInterface(self):
        r"""
        GetSettingsInterface method
        
        returns Settings Interface Object
        """
        
        return self.settingsInterface
    
    """*************************************************************************
                                GetFileBrowserInterface Method 
    
    *************************************************************************"""
    def GetFileBrowserInterface(self):
        r"""
        GetFileBrowserInterface method
        
        returns FileBrowser Interface Object
        """
        
        return self.fileBrowserInterface
    
    """*************************************************************************
                                GetAboutInterface Method 
    
    *************************************************************************"""
    def GetAboutInterface(self):
        r"""
        GetAboutInterface method
        
        returns About Interface Object
        """
        
        return self.aboutInterface
    
    """*************************************************************************
                                GetPrintingInterface Method 
    
    *************************************************************************"""
    def GetPrintingInterface(self):
        r"""
        GetPrintingInterface method
        
        returns Printing Interface Object
        """
        
        return self.printingInterface
    
    
    """*************************************************************************
                                GetDefaultScreen Method 
    
    *************************************************************************"""
    def GetDefaultScreen(self):
        r"""
        GetDefaultScreen method
        
        returns string with default start interface name
        """
        
        return self.defaultScreen
