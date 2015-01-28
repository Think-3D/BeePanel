#!/usr/bin/env python


r"""FileFinder - File hanfling Features.

This module exports:

GetAbsPath() - a function that returns the absolute file path from the system.
"""


__author__ = "BEEVC - Electronic Systems"
__license__ = ""

import os
import platform

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
        
        self.currentDir = os.getcwd()
        
        self.homePath = os.path.expanduser("~")
        
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