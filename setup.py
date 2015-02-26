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

from distutils.core import setup
import shutil
import os
import platform
import getpass
#import BeeConnect
#import Loaders

setup(
      name='BeePanel',
      description='Python BeeTheFirst Panel',
      author='BVC Electronic Systems',
      author_email='mgomes@beeverycreative.com',
      license = '',
      url='https://github.com/beeverycreative/BeePanel',
      packages=['BeeConnect', 'Loaders', 'estimator'],
      )

"""
Directories definitions
"""
pMachine = platform.machine()
user = getpass.getuser()

homeDir = os.path.expanduser("~")

if(pMachine == 'armv6l'):       #assume we're using a raspberri pi
    homeDir = "/home/pi"


installationDir = homeDir + "/BeePanel"
sourceDir = os.getcwd()
installationJsonDir = installationDir + "/Json"
installationLoadersDir = installationDir + "/Loaders"
installationBeeConnectDir = installationDir + "/BeeConnect"
installatonFontsDir = installationDir + "/Fonts"
installationImgDir = installationDir + "/Images"
installationEstimatorDir = installationDir + "/estimator"
installationFirmwareDir = installationDir + "/Firmware"
installationFTPDir = installationDir + "/FTP"
dirMatch = False

if(installationDir == sourceDir):
    print('Source and Installation Dir Match')
    dirMatch = True

#IF INSTALLATION DIR DIFFERENT FROM WORKING DIR, COPY FILES
if(not dirMatch):
    """
    Check/create dirs
    """
    if(not os.path.isdir(installationDir)):
        print("Creating new BeePanel directory")
        os.makedirs(installationDir)
    
    if(not os.path.isdir(installationJsonDir)):
        print("Creating json directory")
        os.makedirs(installationJsonDir)
        
    if(not os.path.isdir(installationLoadersDir)):
        print("Creating loaders directory")
        os.makedirs(installationLoadersDir)
    
    if(not os.path.isdir(installationBeeConnectDir)):
        print("Creating BeeConnect directory")
        os.makedirs(installationBeeConnectDir)
    
    if(not os.path.isdir(installatonFontsDir)):
        print("Creating Fonts directory")
        os.makedirs(installatonFontsDir)
    
    if(not os.path.isdir(installationImgDir)):
        print("Creating Images directory")
        os.makedirs(installationImgDir)
    
    if(not os.path.isdir(installationEstimatorDir)):
        print("Creating estimator directory")
        os.makedirs(installationEstimatorDir)
        
    if(not os.path.isdir(installationFirmwareDir)):
        print("Creating Firmware directory")
        os.makedirs(installationFirmwareDir)
        
    if(not os.path.isdir(installationFTPDir)):
        print("Creating FTP directory")
        os.makedirs(installationFTPDir)
                
    """
    Get file list
    """
    srcList = [file for file in os.listdir(sourceDir) if file.endswith('.py')]
    jsonList = [file for file in os.listdir(sourceDir + "/Json") if file.endswith('.json')]
    loadersList = [file for file in os.listdir(sourceDir + "/Loaders") if file.endswith('.py')]
    beeConList = [file for file in os.listdir(sourceDir + "/BeeConnect") if file.endswith('.py')]
    fontsList = [file for file in os.listdir(sourceDir + "/Fonts") if file.endswith('.ttf')]
    imgList = [file for file in os.listdir(sourceDir + "/Images")]
    estimatorList = [file for file in os.listdir(sourceDir + "/estimator")]
    firmwareList = [file for file in os.listdir(sourceDir + "/Firmware")]
    ftpList = [file for file in os.listdir(sourceDir + "/FTP")]
    
    """
    Copy files to BeePanel dir
    """
    for src in srcList:
        shutil.copyfile(sourceDir + "/" + str(src), installationDir + "/" + str(src))
    
    for json in jsonList:
        shutil.copyfile(sourceDir + "/Json/" + str(json), installationJsonDir + "/" + str(json))
    
    for loader in loadersList:
        shutil.copyfile(sourceDir + "/Loaders/" + str(loader), installationLoadersDir + "/" + str(loader))
        
    for con in beeConList:
        shutil.copyfile(sourceDir + "/BeeConnect/" + str(con), installationBeeConnectDir + "/" + str(con))
    
    for font in fontsList:
        shutil.copyfile(sourceDir + "/Fonts/" + str(font), installatonFontsDir + "/" + str(font))
        
    for img in imgList:
        shutil.copyfile(sourceDir + "/Images/" + str(img), installationImgDir + "/" + str(img))
    
    for est in estimatorList:
        if(os.path.isfile(sourceDir + "/estimator/" + str(est))):
            shutil.copyfile(sourceDir + "/estimator/" + str(est), installationEstimatorDir + "/" + str(est))
    
    for firm in firmwareList:
        shutil.copyfile(sourceDir + "/Firmware/" + str(firm), installationFirmwareDir + "/" + str(firm))
        
    for ftp in ftpList:
        shutil.copyfile(sourceDir + "/FTP/" + str(ftp), installationFTPDir + "/" + str(ftp))
        