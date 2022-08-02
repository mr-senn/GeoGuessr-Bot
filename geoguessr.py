""" 
GeoGuessr Bot
Author: Sohom Sen
Email: sohom416@hotmail.com
Current Version: 0.2-alpha
"""

#imports
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import *
from inputs import maps, options, checkCustom, checkMap, checkOptions
import time, sys
import os
from os import environ

# Environment varible declarations
GOOGLE_CHROME_PATH = environ['GOOGLE_CHROME_PATH']
CHROMEDRIVER_PATH = environ['CHROMEDRIVER_PATH']
USERNAME = environ['USERNAME']
PASSWORD = environ['PASSWORD']

class GeoGuessorBot():
    def __init__(self):
        # Initializes Chrome driver and browser functions
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--no-sandbox')      
        chrome_options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(CHROMEDRIVER_PATH, options = chrome_options)
        self.wait = WebDriverWait(self.driver,20)
        print("Bot Initialized")
    
    def login(self):
        # Function for logging in GeoGuessrPro account.
        self.driver.get("https://www.geoguessr.com/")
        loginButton = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='Log in']")))
        loginButton.click()
        emailField = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='email']")))
        emailField.send_keys(USERNAME)
        passField = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='password']")))
        passField.send_keys(PASSWORD)
        enter = self.driver.find_element_by_xpath("//button[@type='submit']")
        enter.click()

        print("GeoGuessr login successful.")
        time.sleep(1)
    
    def default(self):
        # This function is called when the game setting is set to default by the user. 
        invite = self.wait.until(EC.element_to_be_clickable((By.XPATH,"//button[@type='button']")))
        invite.click()
        time.sleep(5)

    def no_move(self):
        # This function is called when the game setting is set to no move by the user.
        nmSelect = self.wait.until(EC.element_to_be_clickable((By.XPATH,"//label[normalize-space()='No move']")))
        nmSelect.click()
        invite = self.wait.until(EC.element_to_be_clickable((By.XPATH,"//button[@type='button']")))
        invite.click()
        time.sleep(5)    
    
    def no_zoom(self):
        # This function is called when the game setting is set to no zoom by the user.
        nzSelect = self.wait.until(EC.element_to_be_clickable((By.XPATH,"//label[normalize-space()='No zoom']")))
        nzSelect.click()
        invite = self.wait.until(EC.element_to_be_clickable((By.XPATH,"//button[@type='button']")))
        invite.click()
        time.sleep(5)   

    def no_move_zoom(self):
        # This function is called when the game setting is set to no move, no zoom by the user.
        nzSelect = self.wait.until(EC.element_to_be_clickable((By.XPATH,"//label[normalize-space()='No move, no zoom']")))
        nzSelect.click()
        invite = self.wait.until(EC.element_to_be_clickable((By.XPATH,"//button[@type='button']")))
        invite.click()
        time.sleep(5)
    
    def no_move_zoom_pan(self):
        # This function is called when the game setting is set to no move, no pan, no zoom by the user.
        nzSelect = self.wait.until(EC.element_to_be_clickable((By.XPATH,"//label[normalize-space()='No move, no pan, no zoom']")))
        nzSelect.click()   
        invite = self.wait.until(EC.element_to_be_clickable((By.XPATH,"//button[@type='button']")))
        invite.click()
        time.sleep(5)

    def game_setting(self):
        # Function for checking if the game rule menu is being displayed. Returns False if the element is not found.
        try:
            self.driver.find_element_by_xpath("//div[@class='game-settings__detailed-settings']")
        except NoSuchElementException:
            return False
        return True

    
    def map_generator(self, map, option):
        # Function for generating GeoGuessr game links
        map_checked = checkMap(map) # checks for a valid map
        if map_checked in maps:
            map_final = checkCustom(map) # checks for custom GeoGuessr Maps (unofficial ones have unique hash values instead of strings)
            option = checkOptions(option) # checks for a valid rule option
            if option in options:
                pass
            elif option == False:
                return False
            self.driver.get("https://www.geoguessr.com/maps/" + map_final + "/play")
            challenge = self.wait.until(EC.element_to_be_clickable((By.XPATH,"//div[@class='radio-box']//div[@class='radio-box__illustration']")))
            challenge.click()
        if map_checked == False:
            return False

        if option in options:
            if option == "default":
                # Generates game link with default settings.
                if GeoGuessorBot.game_setting(self) == True:
                    defaultBtn = self.wait.until(EC.element_to_be_clickable((By.XPATH,"//span[@class='checkbox__mark checkbox__mark--dark']")))
                    defaultBtn.click()
                    GeoGuessorBot.default(self)
                else:
                    GeoGuessorBot.default(self)
                link = self.driver.find_element_by_xpath("//input[@name='copy-link']").get_attribute('value')
                return link
            elif option == "nm":
                # Generates game link with the no move setting.
                if GeoGuessorBot.game_setting(self) == True:
                    GeoGuessorBot.no_move(self)
                else:
                    noDefault = self.wait.until(EC.element_to_be_clickable((By.XPATH,"//span[@class='checkbox__mark checkbox__mark--dark']")))
                    noDefault.click()
                    GeoGuessorBot.no_move(self)
                link = self.driver.find_element_by_xpath("//input[@name='copy-link']").get_attribute('value')
                return link
            elif option == "nz":
                # Generates game link with the no move zoom setting.
                if GeoGuessorBot.game_setting(self) == True:
                    GeoGuessorBot.no_zoom(self)
                else:
                    noDefault = self.wait.until(EC.element_to_be_clickable((By.XPATH,"//span[@class='checkbox__mark checkbox__mark--dark']")))
                    noDefault.click()
                    GeoGuessorBot.no_zoom(self)
                link = self.driver.find_element_by_xpath("//input[@name='copy-link']").get_attribute('value')
                return link
            elif option == "nmz":
                # Generates game link with the no move, no zoom setting.
                if GeoGuessorBot.game_setting(self) == True:
                    GeoGuessorBot.no_move_zoom(self)
                else:
                    noDefault = self.wait.until(EC.element_to_be_clickable((By.XPATH,"//span[@class='checkbox__mark checkbox__mark--dark']")))
                    noDefault.click()
                    GeoGuessorBot.no_move_zoom(self)
                link = self.driver.find_element_by_xpath("//input[@name='copy-link']").get_attribute('value')
                return link
            elif option == "nmpz":
                # Generates game link with the no move, no pan, no zoom setting.
                if GeoGuessorBot.game_setting(self) == True:
                    GeoGuessorBot.no_move_zoom_pan(self)
                else:
                    noDefault = self.wait.until(EC.element_to_be_clickable((By.XPATH,"//span[@class='checkbox__mark checkbox__mark--dark']")))
                    noDefault.click()
                    GeoGuessorBot.no_move_zoom_pan(self)
                link = self.driver.find_element_by_xpath("//input[@name='copy-link']").get_attribute('value')
                return link



def main():
    browser = GeoGuessorBot() #initiates GeoGuessrBotr
    browser.login()
    
    while True:
        map,option= input("Enter the Map you want and rule: ").split() 
        timer= input("Enter Time Limit: ")
        geoguessrlink = browser.map_generator(map,option,timer) # Generates link
        if geoguessrlink == False: # Checks if the game link was properly generated. If not, then error is sent to the user.
            print("Error Occured. Either the map or rule is incorrect. Please try again")
            return True
        else:
            print("Game link generated:") 
            print(geoguessrlink) #User receives the generated game link
            exitKey = input("Replay? y/n ").lower()
            print(exitKey)
            if exitKey == "y":
                pass
            if exitKey == "n":
                raise SystemExit
            

if __name__ == "__main__":
    main()