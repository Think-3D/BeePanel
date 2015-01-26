#!/usr/bin/env python


import os
import shutil
from shutil import copyfile

"""
Directories definitions
"""
homeDir = os.path.expanduser("~")
installationDir = homeDir + "/BeePanel"
sourceDir = os.getcwd() + "/src"
installationJsonDir = installationDir + "/json"
installationLoadersDir = installationDir + "/loaders"
installationBeeConnectDir = installationDir + "/BeeConnect"
installatonFontsDir = installationDir + "/Fonts"
installationImgDir = installationDir + "/Images"

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
            
"""
Get file list
"""
srcList = [file for file in os.listdir(path=sourceDir) if file.endswith('.py')]
jsonList = [file for file in os.listdir(path=sourceDir + "/json") if file.endswith('.json')]
loadersList = [file for file in os.listdir(path=sourceDir + "/loaders") if file.endswith('.py')]
beeConList = [file for file in os.listdir(path=sourceDir + "/BeeConnect") if file.endswith('.py')]
fontsList = [file for file in os.listdir(path=sourceDir + "/Fonts") if file.endswith('.ttf')]
imgList = [file for file in os.listdir(path=sourceDir + "/Images")]

"""
Copy files to BeePanel dir
"""
for src in srcList:
    copyfile(sourceDir + "/" + str(src), installationDir + "/" + str(src))

for json in jsonList:
    copyfile(sourceDir + "/json/" + str(json), installationJsonDir + "/" + str(json))

for loader in loadersList:
    copyfile(sourceDir + "/loaders/" + str(loader), installationLoadersDir + "/" + str(loader))
    
for con in beeConList:
    copyfile(sourceDir + "/BeeConnect/" + str(con), installationBeeConnectDir + "/" + str(con))

for font in fontsList:
    copyfile(sourceDir + "/Fonts/" + str(font), installatonFontsDir + "/" + str(font))
    
for img in imgList:
    copyfile(sourceDir + "/Images/" + str(img), installationImgDir + "/" + str(img))