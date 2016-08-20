# Copyright (c) 2016, Emmanuel Reubanraj Isaac
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#  * Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#
#  * Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation and/or
# other materials provided with the distribution.
# 
#   * Neither the name of Emmanuel Reubanraj Isaac nor the names of its contributors may be used to
# endorse or promote products derived from this software without specific prior
# written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
# IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# TRAVIAN FARM LIST RAID LAUNCH AUTOMATOR 1.0.0
#

import sys
import time
from splinter import Browser

# VARIABLES
homeURL = 'http://ts6.travian.com/'
farmListURL = 'http://ts6.travian.com/build.php?tt=99&id=39'
username = ''
password = ''#'sys.argv[2]'
raidListMarkAll = 'raidListMarkAll'
loadingMessage = 'Please wait while page is loading'
executionSuccessMessage = 'Successfully Launched Raids'
missingParametersMessage = 'You need to call the script with both username and password'

# ELEMENTS
USERNAME_TEXT_NAME = 'name'
PASSWORD_TEXT_NAME = 'password'
SUBMIT_BUTTON_ID = 's1'
VILLAGE_MAP_ID = 'village_map'
RAID_LIST_ID = 'raidList'
LIST_ENTRY_CLASS = '.listEntry'
OPEN_SWITCH_WRAPPER_CLASS = '.openedClosedSwitch.switchOpened'
CLOSED_SWITCH_WRAPPER_CLASS = '.openedClosedSwitch.switchClosed'
GREEN_CLASS = '.green'
START_RAID_BUTTON_VALUE = 'Start raid'

# GLOBAL VARIABLES
COUNTER = 0
LIST_COUNT = 0

# QUIT BROWSER
def timeToSleep():
    browser.quit()

# ITERATE THROUGH FARM LISTS AND START EXECUTING
def commandTroopAttacks():
    global COUNTER
    # If all farm lists raids are started then stop execution 
    if (COUNTER == LIST_COUNT):
        print(executionSuccessMessage)
        timeToSleep()
    # Else start farm list raids
    else:
        # Get the farm list
        divs = browser.find_by_css(LIST_ENTRY_CLASS)
        if (divs):
            # Get the nth farm list based on counter
            div = divs[COUNTER]
            # Trim the farm list ID to get only the number
            listID = div['id'][4:]

            # Since by default the first farm list is expanded skip this step
            if (COUNTER != 0):
                browser.execute_script('Travian.Game.RaidList.toggleList(' + listID + ');')

            # Select all items in expanded farm list
            div.find_by_id(raidListMarkAll + listID).click()

            # Get the buttons in the expanded farm list 
            buttons = div.find_by_css(GREEN_CLASS)
            for button in buttons:
                # Identify if the button is Start Raid
                if (button.value == START_RAID_BUTTON_VALUE):
                    # Get the button ID
                    buttonID = button['id']
                    # Start the raid by clicking the button
                    div.find_by_id(buttonID).click()
                    # Increase the counter
                    COUNTER += 1

            # Wait till page loads
            while(browser.is_element_not_present_by_id(RAID_LIST_ID, 0.1) == True):
                print(loadingMessage)
            # Adding a sleep timer just in case 
            time.sleep(0.5)
            # Recursive function call until counter is equal to number of farm list items
            commandTroopAttacks()
                
# OPEN THE RALLY POINT
def routeToRallyPoint():
    # Open rally point farm list tab
    browser.visit(farmListURL)
    while(browser.is_element_not_present_by_id(RAID_LIST_ID, 0.1) == True):
        print(loadingMessage)
    # Set the number of farm lists into global variable
    global LIST_COUNT
    LIST_COUNT = len(browser.find_by_css(LIST_ENTRY_CLASS))
    commandTroopAttacks()

# LOGIN TO TRAVIAN SERVER
def loginToServer():
    # Complete login form
    browser.fill(USERNAME_TEXT_NAME, username)
    browser.fill(PASSWORD_TEXT_NAME, password)
    browser.find_by_id(SUBMIT_BUTTON_ID).click()
    while(browser.is_element_not_present_by_id(VILLAGE_MAP_ID, 0.1) == True):
        print(loadingMessage)
    routeToRallyPoint()

# START RAIDING SCRIPT
def startRaiding():
    # Open Travian TS6 Login page
    browser.visit(homeURL)
    loginToServer()


# Create a browser instance
browser = Browser()
if(len(sys.argv) == 3):
    username = sys.argv[1]
    password = sys.argv[2]
    startRaiding()
else:
    timeToSleep()
    print(missingParametersMessage)