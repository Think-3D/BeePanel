#!/usr/local/bin/python3
#from Onboard.OnboardGtk import app


r"""
BeePanel - Main class

This file exports:

BeePanel Class:
    Class called to handle the interface and application activity

restart_app() method to start the application within the application

"""

__author__ = "Marcos Gomes"
__license__ = ""

import os
import sys
import pygame
import math
import time


import BeePanel_Button
import WaitForConnection

import About
import Calibration
import FilamentChange
import FileBrowser
import Jog
import PrinterInfo
import Printing
import Settings

import BeeConnect.Command
import BeeConnect.Connection

import Loaders.BeePanelJsonLoader as BeePanelJsonLoader

os.environ["SDL_FBDEV"] = "/dev/fb1"
os.environ["SDL_MOUSEDEV"] = "/dev/input/touchscreen"
os.environ["SDL_MOUSEDRV"] = "TSLIB"

"""
Main Class Interfaces
"""
class BeePanel():
    r"""
    BeePanel Class
    
    This class exports:
    
    __init__()            method to initialize the application variables and connection
    start()               method with the application infinite loop
    handle_events()       method handles the pygame events
    update()              method updates interface components
    draw()                method draws components on the screen
    UpdateLeftButtons()   method updates left buttons components
    GetBEEStatus()        method gets the current status of the BTF printer
    LoadCurrentScreen()   method loads current screen json config to current screen
    transferFile()        method transfers local gcode file to BTF memory 
    """
    
    """
    State vars
    """
    restart = False
    exitApp = False
    done = False
    cancelTransfer = False
    BeeState = "Disconnected"
    
    """
    BEEConnect vars
    """
    beeCon = None
    beeCmd = None
    
    """
    Loaders variables
    """
    jsonLoader = None
    
    """
    Left Menu
    """
    leftMenuButtons = None
    interfaceButtons = None
    
    leftMenuLoader = None
    carouselButtons = None
    visibleButtons = None
    currentIdx = None
    carouselItems = None
    carouselX = None
    carouselY = None
    carouselWidth = None
    carouselHeight = None
    carouselButtonHeight = None
    buttonNames = None
    buttonTitles = None
    carouselBgR = None
    carouselBgG = None
    carouselBgB = None
    carouselFR = None
    carouselFG = None
    carouselFB = None
    carouselFontType = None
    carouselFontSize = None
    
    """
    Interfaces
    """
    currentScreenName = None
    currentScreen = None
    printerInfoScreenLoader = None
    jogScreenLoader = None
    calibrationScreenLoader = None
    filamentScreenLoader = None
    settingsScreenLoader = None
    browserScreenLoader = None
    aboutScreenLoader = None
    printingScreenLoader = None

    """*************************************************************************
                                Init Method 
        
    *************************************************************************"""
    def __init__(self):
        """
        inits the BeePanel Components
        
        
        """
        
        
        """
        State variables Initialization
        """
        self.done = False
        self.restart = False
        self.exitApp = False
        self.cancelTransfer = False
        self.BeeState = "Disconnected"
        
        """
        JSON Loading
        """
        self.jsonLoader = BeePanelJsonLoader.jsonLoader()
        
        print("Using display: ",self.jsonLoader.displayObject.displayType)
        print("Display Resolution: ", 
                self.jsonLoader.displayObject.displayWidth, 
                "x", self.jsonLoader.displayObject.displayHeight)
        
        self.BEEDisplay = self.jsonLoader.displayObject
        
        
        """
        Left Menu Loader
        """
        self.leftMenuLoader = self.jsonLoader.GetLeftMenuLoader()
        
        self.carouselButtons = self.leftMenuLoader.GetCarouselButtons()
        
        self.currentIdx = 0
        self.carouselItems = self.leftMenuLoader.GetCarouselItems()
        self.carouselX = self.leftMenuLoader.GetCarouselX()
        self.carouselY = self.leftMenuLoader.GetCarouselY()
        self.carouselWidth = self.leftMenuLoader.GetCarouselWidth()
        self.carouselHeight = self.leftMenuLoader.GetCarouselHeight()
        self.carouselButtonHeight = self.leftMenuLoader.GetCarouselButtonHeight()
        
        self.buttonNames = self.leftMenuLoader.GetCarouselButtonNames()
        self.buttonTitles = self.leftMenuLoader.GetCarouselButtonTitles()
        
        self.carouselBgR = self.leftMenuLoader.GetBgR()
        self.carouselBgG = self.leftMenuLoader.GetBgG()
        self.carouselBgB = self.leftMenuLoader.GetBgB()
        self.carouselFR = self.leftMenuLoader.GetFR()
        self.carouselFG = self.leftMenuLoader.GetFG()
        self.carouselFB = self.leftMenuLoader.GetFB()
        
        self.carouselFontType = self.leftMenuLoader.GetCarouselFontType()
        self.carouselFontSize = self.leftMenuLoader.GetCarouselFontSize()
        
        self.UpdateLeftButtons()
        
        """
        Screen Loaders
        """
        self.printerInfoScreenLoader = self.jsonLoader.GetPrinterInfoInterface()
        self.jogLoader = self.jsonLoader.GetJogInterface()
        self.calibrationLoader = self.jsonLoader.GetCalibrationInterface()
        self.filamentChangeLoader = self.jsonLoader.GetFilamentChangeInterface()
        self.settingsLoader = self.jsonLoader.GetSettingsInterface()
        self.fileBrowserLoader = self.jsonLoader.GetFileBrowserInterface()
        self.aboutLoader = self.jsonLoader.GetAboutInterface()
        
        self.printingScreenLoader = self.jsonLoader.GetPrintingInterface()
        
        self.currentScreenName = self.jsonLoader.GetDefaultScreen()
        
        """
        Init pygame
        """
        print("Drawing Interfaces")
        pygame.init()
        pygame.mouse.set_visible(False)
        
        self.screen = self.BEEDisplay.GetBEEScreen()
        self.screen.fill(self.BEEDisplay.GetbgColor())
        
        """
        Wait For Connection
        """
        
        
        waitScreen = WaitForConnection.WaitScreen(self.screen)
        #If the user closes the windows without a connection
        if not waitScreen.connected:
            self.done = True
            
        self.beeCon = waitScreen.beeCon
        self.beeCmd = BeeConnect.Command.Cmd(self.beeCon)
        
        waitScreen.KillAll()
        waitScreen = None
        
        

        
        return
        
    """*************************************************************************
                                Start Method 
    
    *************************************************************************"""
    def start(self):
        """
        BeePanel Infinite Loop
        
        
        """
        
        self.GetBEEStatus()
        
        """
        Print interface screen
        """
        if(self.BeeState == "SD_Print"):
            #init print screen in Printing state
            self.LoadCurrentScreen("Print", 0)
        elif( self.BeeState == "Ready"):
            """
            Init Interfaces Screens
            """
            self.beeCmd.home()
            self.LoadCurrentScreen(self.currentScreenName)
        else:
            print("COULD NOT GET STATUS, Connection Wait happened???")
            #self.currentScreenName = self.jsonLoader.GetDefaultScreen()
            #self.LoadCurrentScreen(self.currentScreenName)
            
            return None
        
        print("Starting BeePanel")
        
        #CLEAR EXISTING EVENTS
        retVal = pygame.event.get()
        retVal = None
        
        self.exitApp = False
        self.restart = False
        
        while not self.done:
            
            # Handle events
            self.handle_events()
            if(self.exitApp):
                break
            
            # Update buttons visibility, text, graphs etc
            self.update()

            # Draw everything
            self.draw()
            
            #Pull variables
            pullRes = self.currentScreen.Pull()
            
            #check for gobal actions
            
            if(pullRes is not None):
                print(pullRes)
                if(pullRes == "Printing"):
                    self.restart = True
                    """
                    self.restart = True
                    self.currentScreen.KillAll()
                    self.currentScreen = None
                    self.beeCmd = None
                    self.beeCon.close()
                    self.beeCon = None
                    self.done = True
                    time.sleep(1)
                    """
                    break
            
            
            # Check for interface CallBack
            if((self.currentScreen.ExitCallBack() is not None)):
                if(self.currentScreen.exitCallBackResp == "Restart"):
                    self.restart = True
                    self.currentScreenName = self.jsonLoader.GetDefaultScreen()
                """
                self.currentScreen.KillAll()
                self.currentScreen = None
                self.beeCmd.homeZ()
                self.beeCmd = None
                self.beeCon.close()
                self.beeCon = None
                self.done = True
                """
                break
            
        #pygame.quit()
        
        return
        
        
        
    """*************************************************************************
                                handle_events Method 
    
    Retrieves the event vector and sends it to the individual interface methods
    *************************************************************************"""
    def handle_events(self):
        
        retVal = pygame.event.get()
        """handle all events."""
        buttonEvent = False
        
        self.currentScreen.handle_events(retVal)
        
        for event in retVal:
            eventName =  pygame.event.event_name(event.type)
            #if(eventName in ['ActiveEvent','MouseMotion']):        #MOUSE MOOVEMENT
            #    break
            
            
            """
            CARROUSEL MENU UP/DOWN BUTTONS
            """
            for btn in self.carouselButtons:
                if 'click' in btn.handleEvent(event):
                    btnName = btn._propGetName()
                    if btnName == "MenuUp":
                        self.currentIdx = self.currentIdx - 1
                        buttonEvent = True
                    elif btnName == "MenuDown":
                        self.currentIdx = self.currentIdx + 1
                        buttonEvent = True
                    self.UpdateLeftButtons()
            
            if(buttonEvent == True):
                break
            
            
            """
            CARROUSEL INTERFACE SELECTION BUTTONS
            """
            setScreen = None
            for btn in self.leftMenuButtons:
                btnName = btn._propGetName()
                if 'click' in btn.handleEvent(event):
                    if btnName == "Printer Info":
                        setScreen = "PrinterInfo"
                        buttonEvent = True
                    elif btnName == "Jog":
                        setScreen = "Jog"
                        buttonEvent = True
                    elif btnName == "Calibration":
                        setScreen = "Calibration"
                        buttonEvent = True
                    elif btnName == "Filament":
                        setScreen = "FilamentChange"
                        buttonEvent = True
                    elif btnName == "Settings":
                        setScreen = "Settings"
                        buttonEvent = True
                    elif btnName == "Browser":
                        setScreen = "FileBrowser"
                        buttonEvent = True
                    elif btnName == "About":
                        setScreen = "About"
                        buttonEvent = True
                    
            
            if (not (setScreen is None)) and (not setScreen==self.currentScreen.GetCurrentScreenName()):
                if(self.currentScreen.exitNeedsHoming):
                    self.beeCmd.home()
                self.LoadCurrentScreen(setScreen)
                
        if(buttonEvent == True):
            return
        
        return
        
        
        
    """*************************************************************************
                                update Method 
    
    Calls all the individual update methods
    *************************************************************************"""
    def update(self):
        
        if(self.BeeState == "SD_Print" or self.BeeState == "Transfer"):
            pass
        else:
            #set left buttons visible
            for btn in self.jsonLoader.leftMenuButtons:
                btn.visible = True

            #set carouselbuttons visible
            for btn in self.carouselButtons:
                btn.visible = True
                pass

        self.currentScreen.update()
        
        return
            
    """*************************************************************************
                                draw Method 
    
    Draws current screen and calls all the individual draw methods
    *************************************************************************"""   
    def draw(self):
        
        #clear whole screen
        self.screen.fill(self.BEEDisplay.GetbgColor())
        
        if(self.BeeState == "SD_Print" or self.BeeState == "Transfer"):
            pass
        else:
            #draw split line
            self.BEEDisplay.DrawLine(self.screen)

            for btn in self.carouselButtons:
                btn.draw(self.screen)

            for btn in self.leftMenuButtons:
                btn.draw(self.screen)
                if btn._propGetName() == self.currentScreen.GetCurrentScreenName():
                    pygame.draw.rect(self.screen, btn._propGetFgColor(), btn._propGetRect(), 3)

        #draw screen elements
        self.currentScreen.draw()
        
        # update screen
        pygame.display.update()
        
        return
        
        return
    
    """*************************************************************************
                                UpdateLeftButtons Method 
    
    Updates Left Menu buttons to show
    *************************************************************************"""  
    def UpdateLeftButtons(self):
        
        self.leftMenuButtons = []
        for i in range(0,self.carouselItems):
            
            pos = i + self.currentIdx
            idx = pos % len(self.buttonNames)
                
            x = self.carouselX
            y = self.carouselY + i*self.carouselHeight
            width = self.carouselWidth
            height = self.carouselButtonHeight
            
            beeBtn = BeePanel_Button.Button(x,y,width,height,
                                            self.buttonNames[idx],
                                            self.carouselBgR,self.carouselBgR,self.carouselBgR,
                                            self.carouselFR,self.carouselFG,self.carouselFB,
                                            self.carouselFontType,self.carouselFontSize,
                                            None,None,None,self.buttonTitles[idx])
            
            self.leftMenuButtons.append(beeBtn.GetTextButton())
        
        return
    
    """*************************************************************************
                                GetBEEStatus Method 
    
    Gets the printer status
    *************************************************************************"""  
    def GetBEEStatus(self):
        
        self.BeeState = self.beeCmd.getStatus()
        
        print("Printer Status: ",self.BeeState)
        
        return
    
    """*************************************************************************
                                LoadCurrentScreen Method 
    
    Updates slected screen
    *************************************************************************"""  
    def LoadCurrentScreen(self, setScreen, state = 0):
        
        if(self.currentScreen is not None):
            print("New Screen")
            self.currentScreen.KillAll()
            self.currentScreen = None
            
        if(setScreen == "Print"):
            self.currentScreen = Printing.PrintScreen(self.screen,self.printingScreenLoader,self.beeCmd, state)
        else:
            if setScreen == "PrinterInfo":
                self.currentScreen = PrinterInfo.PrinterInfoScreen(self.screen,self.printerInfoScreenLoader,self.beeCmd)
            elif setScreen == "Jog":
                self.currentScreen = Jog.JogScreen(self.screen,self.jogLoader,self.beeCmd)
            elif setScreen == "Calibration":
                self.currentScreen = Calibration.CalibrationScreen(self.screen,self.calibrationLoader,self.beeCmd)
            elif setScreen == "FilamentChange":
                self.currentScreen = FilamentChange.FilamentChangeScreen(self.screen,self.filamentChangeLoader,self.beeCmd)
            elif setScreen == "Settings":
                self.currentScreen = Settings.SettingsScreen(self.screen,self.settingsLoader,self.beeCmd)
            elif setScreen == "FileBrowser":
                self.currentScreen = FileBrowser.FileBrowserScreen(self.screen,self.fileBrowserLoader,self.beeCmd)
            elif setScreen == "About":
                self.currentScreen = About.AboutScreen(self.screen,self.aboutLoader,self.beeCmd)

            self.currentScreenName = self.currentScreen.GetCurrentScreenName()
        
        
        return
    
    """*************************************************************************
                                transferFile Method 
    
    Transfers gcode file to R2C2
    *************************************************************************"""  
    def transferFile(self, fileName):
        
        
        return


"""*************************************************************************
                                restart_app Method 
    
    restarts application
*************************************************************************"""  
def restart_app():
    python = sys.executable
    os.execl(python, python, * sys.argv)

"""*************************************************************************
                                main Method 
    
    restarts application
*************************************************************************"""  
if __name__ == '__main__':
    app = BeePanel()
    while(app.exitApp == False):
        try:
            app.start()
        except ValueError:
            app = BeePanel()
            print('Application error occurred')
    
    pygame.quit()
    """
    if(app.restart == True):
        app = None
        restart_app()
    """