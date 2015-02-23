Copyright (c) 2015 BEEVC - Electronic Systems This file is part of BEESOFT
software: you can redistribute it and/or modify it under the terms of the GNU
General Public License as published by the Free Software Foundation, either
version 3 of the License, or (at your option) any later version. BEESOFT is
distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details. You
should have received a copy of the GNU General Public License along with
BEESOFT. If not, see <http://www.gnu.org/licenses/>.

## BeePanel Beta ##

Beepanel creates a small interface to control you BeeTheFirst 3D Printer. <br/>
BeePanel grants you access to mantainance operations directly on the touch screen. <br/>
BeePanel allows you to run custom gcodes on your BTF Printer, using USB Mass storage devices to transfer the code directly to the pritner. <br/>

https://github.com/beeverycreative/BeePanel


## Setup ##

### Requirements ###

* Raspberry Pi running Raspbian
* LCD Touch Dispaly with STMPE610 + ILI9341 controllers (e.g. Adafruit PiTFT (http://adafru.it/1601))
* Python 3.4
* PyGame


### Adafruit PiTFT Setup ###


### Reccommended Install ###
We recommend you to install BeePanel by burning the Available Image into a SD card. <br/>
To burn the image follow these steps: <br/>

*   Download the .img file. <br/>
*   Insert a 4GB+ SD card in your SD card reader. <br/>
*   Follow isntructions on how to burn the .img. (http://www.raspberrypi.org/documentation/installation/installing-images/) <br/>

However if you wish to install it on an existing raspbian image read section "Installing BeePanel in an existing Raspbian Image" and follow the instructions. <br/>



### Installing BeePanel in an existing Raspbian Image ###

cd ~
git clone https://github.com/beeverycreative/BeePanel.git
cd BeePanel
sudo python3 setup.py install
