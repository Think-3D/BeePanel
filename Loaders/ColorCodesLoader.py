#!/usr/bin/env python

r"""

ColorCodeLoader Class

This class is responsible for loading the interface components configuration 
from the .json configuration file.

This class exports the following methods:

__init__()            Initializes current class
GetColorNameList()    returns color names list
GetColorCodeList()    returns color code list
GetColorList()        returns color list
GetColorName()        returns color name for a given color code
"""


__author__ = "BVC Electronic Solutions"
__license__ = ""

import pygame
import json
import FileFinder

class ColorCodes():
    
    jsonPath = "/Json/ColorCodes.json"
    
    colors = None
    
    colorNameList = []
    colorCodeList = []
    colorRGBList = []
    
    """*************************************************************************
                                Init Method 
    
    
    *************************************************************************"""
    def __init__(self):
        r"""
        __init__ method
        
        Initialization method. Loads configurations from the json file
        """
        
        ff = FileFinder.FileFinder()
        
        f = open(ff.GetAbsPath(self.jsonPath),'r')                     #load json as text file
        jsonData = json.load(f)                         #parse the json file
        self.colors = jsonData.get('ColorCodes')      #get the color codes list from json file
        f.close()   
        
        for code in self.colors:
            self.colorNameList.append(code['ColorName'])
            self.colorCodeList.append(code['ColorCode'])
            
            rgbColor = code['RGBColor']
            rgbSplit = rgbColor.split(",")
            self.colorRGBList.append(pygame.Color(
                                                int(rgbSplit[0]),
                                                int(rgbSplit[1]),
                                                int(rgbSplit[2])))
            
        
        return
    
    """*************************************************************************
                                GetColorNameList Method 
    
    
    *************************************************************************"""
    def GetColorNameList(self):
        r"""
        GetColorNameList method
        
        returns color name list
        """
        return self.colorNameList
    
    """*************************************************************************
                                GetColorCodeList Method 
    
    
    *************************************************************************"""
    def GetColorCodeList(self):
        r"""
        GetColorCodeList method
        
        returns color code list
        """
        return self.colorCodeList
    
    """*************************************************************************
                                GetColorList Method 
    
    
    *************************************************************************"""
    def GetColorList(self):
        r"""
        GetColorList method
        
        returns color  list
        """
        return self.colorRGBList
    
    """*************************************************************************
                                GetColorName Method 
    
    
    *************************************************************************"""
    def GetColorName(self, code):
        r"""
        GetColorName method
        
        returns color name for a given color code
        
        arguments:
            code - string with color code
            
        returns:
            string with color name
            "unknown" string if color not found 
        """
        
        for c in self.colors:
            if(c['ColorCode'] == code):
                return c['ColorName']
            
        return "Unknoown"