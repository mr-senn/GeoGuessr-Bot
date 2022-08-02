""" 
GeoGuessr Bot
Author: Sohom Sen
Current Version: 1.0 -beta
"""

#imports
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import *
import mysql.connector
import time
from os import environ

# Environment varible declarations
#GOOGLE_CHROME_PATH = environ['GOOGLE_CHROME_PATH']
USERNAME = environ['GEO_USERNAME']
PASSWORD = environ['GEO_PASSWORD']

db_host = environ['DB_HOST']
db_database = environ['DB_DATABASE']
db_user = environ['DB_USER']
db_password = environ['DB_PASSWORD']
db_port = environ['DB_PORT']

s = Service(ChromeDriverManager().install())


class GeoGuessorBot():
    def __init__(self):
        
        # Initializes Chrome driver and browser functions
        chrome_options = Options()
        #chrome_options.add_argument("--headless")
        #chrome_options.add_argument('--no-sandbox')      
        #chrome_options.add_argument('--disable-dev-shm-usage')
        #chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("log-level=3")
        self.driver = webdriver.Chrome(service = s, options = chrome_options)
        self.wait = WebDriverWait(self.driver,20)
        print("Bot Initialized")
        
    
    def login(self):
        # Function for logging in GeoGuessrPro account.
        self.driver.get("https://www.geoguessr.com/")
        alreadyButton = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='Already have an account?']")))
        alreadyButton.click()
        time.sleep(3)
        emailField = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='email']")))
        emailField.send_keys(USERNAME)
        passField = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='password']")))
        passField.send_keys(PASSWORD)
        enter = self.driver.find_element(by = By.XPATH, value = "//button[@type='submit']")
        enter.click()

        print("GeoGuessr login successful.")
        time.sleep(1)

    def close(self):
        self.driver.quit()

    def moveReset(self):
        try:
            self.driver.find_element(by = By.XPATH, value = "//img[@alt='Moving is allowed']")
        except NoSuchElementException:
            resetMove = self.wait.until(EC.element_to_be_clickable((By.XPATH,"//img[@alt='Moving is not allowed']")))
            resetMove.click()

    def panReset(self):
        try:
            self.driver.find_element(by = By.XPATH, value = "//img[@alt='Panning is allowed']")
        except NoSuchElementException:
            resetPan = self.wait.until(EC.element_to_be_clickable((By.XPATH,"//img[@alt='Panning is not allowed']")))
            resetPan.click()
    def zoomReset(self):
        try:
            self.driver.find_element(by = By.XPATH, value = "//img[@alt='Zooming is allowed']")
        except NoSuchElementException:
            resetZoom = self.wait.until(EC.element_to_be_clickable((By.XPATH,"//img[@alt='Zooming is not allowed']")))
            resetZoom.click()
    
    def default(self):
        # This function is called when the game setting is set to default by the user. 
        invite = self.wait.until(EC.element_to_be_clickable((By.XPATH,"//button[@type='button']//div[@class='button_wrapper__NkcHZ']")))
        invite.click()
        time.sleep(5)

    def no_move(self):
        # This function is called when the game setting is set to no move by the user.
        #pan zoom allowed

        GeoGuessorBot.moveReset(self)
        GeoGuessorBot.panReset(self)
        GeoGuessorBot.zoomReset(self)

        nmSelect = self.wait.until(EC.element_to_be_clickable((By.XPATH,"//img[@alt='Moving is allowed']")))
        nmSelect.click()
        time.sleep(1)
        invite = self.wait.until(EC.element_to_be_clickable((By.XPATH,"//button[@type='button']")))
        invite.click()
        time.sleep(2)    
    
    def no_zoom(self):
        # This function is called when the game setting is set to no zoom by the user.
        #move pan allowed

        GeoGuessorBot.moveReset(self)
        GeoGuessorBot.panReset(self)
        GeoGuessorBot.zoomReset(self)

        nzSelect = self.wait.until(EC.element_to_be_clickable((By.XPATH,"//img[@alt='Zooming is allowed']")))
        nzSelect.click()
        time.sleep(1)
        invite = self.wait.until(EC.element_to_be_clickable((By.XPATH,"//button[@type='button']")))
        invite.click()
        time.sleep(2) 

    def no_move_zoom(self):
        #pan allowed
        # This function is called when the game setting is set to no move, no zoom by the user.      
        GeoGuessorBot.moveReset(self)
        GeoGuessorBot.panReset(self)
        GeoGuessorBot.zoomReset(self)

        nzSelect = self.wait.until(EC.element_to_be_clickable((By.XPATH,"//img[@alt='Zooming is allowed']")))
        nzSelect.click()
        nmSelect = self.wait.until(EC.element_to_be_clickable((By.XPATH,"//img[@alt='Moving is allowed']")))
        nmSelect.click()
        time.sleep(1)
        invite = self.wait.until(EC.element_to_be_clickable((By.XPATH,"//button[@type='button']")))
        invite.click()
        time.sleep(2) 
    
    def no_move_zoom_pan(self):
        # none allowed
        # This function is called when the game setting is set to no move, no pan, no zoom by the user
        GeoGuessorBot.moveReset(self)
        GeoGuessorBot.panReset(self)
        GeoGuessorBot.zoomReset(self)

        nzSelect = self.wait.until(EC.element_to_be_clickable((By.XPATH,"//img[@alt='Zooming is allowed']")))
        nzSelect.click()
        nmSelect = self.wait.until(EC.element_to_be_clickable((By.XPATH,"//img[@alt='Moving is allowed']")))
        nmSelect.click()
        npSelect = self.wait.until(EC.element_to_be_clickable((By.XPATH,"//img[@alt='Panning is allowed']")))
        npSelect.click()
        time.sleep(1)
        invite = self.wait.until(EC.element_to_be_clickable((By.XPATH,"//button[@type='button']")))
        invite.click()
        time.sleep(2) 

    def time_slider(self,time_num):
        num = int(time_num)

        if num % 10 == 0:
            resetSlider = self.driver.find_element(by = By.XPATH, value = "//div[@class='styles_handle__zYRZ7']")
            ActionChains(self.driver).drag_and_drop_by_offset(resetSlider, -228, 0).perform()
            time.sleep(1)

            input = int(num / 10)
            list_num = int(input+1)
            range_num = []
            for i in range(list_num):
                range_num.append(round(i*3.6))
            pixel = 1 + int(range_num[input])
            print(pixel)
            
            timerSlider = self.driver.find_element(by = By.XPATH, value = "//div[@class='styles_handle__zYRZ7']")
            ActionChains(self.driver).drag_and_drop_by_offset(timerSlider, pixel , 0).perform()
            time.sleep(1)
        if num % 10 != 0:

            resetSlider = self.driver.find_element(by = By.XPATH, value = "//div[@class='styles_handle__zYRZ7']")
            ActionChains(self.driver).drag_and_drop_by_offset(resetSlider, -228, 0).perform()
            time.sleep(1)

            rounded_num = round(num/10)*10
            input = int(rounded_num / 10)
            list_num = int(input+1)
            range_num = []
            for i in range(list_num):
                range_num.append(round(i*3.6))
            pixel = 1 + int(range_num[input])
            print(pixel)
            
            timerSlider = self.driver.find_element(by = By.XPATH, value = "//div[@class='styles_handle__zYRZ7']")
            ActionChains(self.driver).drag_and_drop_by_offset(timerSlider, pixel , 0).perform()
            time.sleep(1)
        else:
            return False

    def game_setting(self):
        # Function for checking if the game rule menu is being displayed. Returns False if the element is not found.
        try:
            self.driver.find_element(by = By.CLASS_NAME, value = "game-options_optionGroup__qNKx1")
        except NoSuchElementException:
            return True
        return False
        
    def checkMap(map):
        connection = mysql.connector.connect(host= db_host,
                                         database= db_database,
                                         user= db_user,
                                         password = db_password,
                                         port = db_port)
        get_map_cursor = connection.cursor(prepared=True)

        get_map_query = """SELECT map, urlStub FROM geo WHERE map = %s"""
        try:
            map_check = (map,)
            get_map_cursor.execute(get_map_query,map_check)
            map_db = get_map_cursor.fetchone()
            if map_db:
                map_name = map_db[0]
                map_url = map_db[1]
                return [map_name, map_url]
            else:
                return False
        except mysql.connector.Error as error:
            print("Uh oh. Something went wrong. {}".format(error))
        finally:
            if connection.is_connected():
                get_map_cursor.close()
    
    def checkOptions(option):
        game_options = ["default", "nm", "nz", "nmz", "nmpz"]
        if option not in game_options:
            return False
        else:
            return option

    def map_generator(self, map, option, timer):
        map_check = GeoGuessorBot.checkMap(map)
        if map_check[0] == map:
            self.driver.get("https://www.geoguessr.com/maps/" + map_check[1] + "/play")
            challenge = self.wait.until(EC.element_to_be_clickable((By.XPATH,"//div[@class='radio-box_root__ka_9S']//div[@class='radio-box_illustration___Yw_M']")))
            challenge.click()
        if map_check == False:
            return False
        
        rule_check =  GeoGuessorBot.checkOptions(option)
        if rule_check == False:
            return False
        else:
            if rule_check == "default":
                if GeoGuessorBot.game_setting(self) == False:
                    defaultBtn = self.wait.until(EC.element_to_be_clickable((By.XPATH,"//div[@class='game-settings_default__DIBgs']//div//input[@type='checkbox']")))
                    defaultBtn.click()
                    GeoGuessorBot.default(self)
                else:
                    GeoGuessorBot.default(self)
                link = self.driver.find_element(by = By.XPATH, value = "//input[@name='copy-link']").get_attribute('value')
                return link
            elif rule_check == "nm":
                if GeoGuessorBot.game_setting(self):
                    noDefaultBtn = self.wait.until(EC.element_to_be_clickable((By.XPATH,"//div[@class='game-settings_default__DIBgs']//div//input[@type='checkbox']")))
                    noDefaultBtn.click()
                    GeoGuessorBot.time_slider(self, timer)
                    time.sleep(1)
                    GeoGuessorBot.no_move(self)
                else:
                    GeoGuessorBot.time_slider(self, timer)
                    time.sleep(1)
                    GeoGuessorBot.no_move(self)

                link = self.driver.find_element(by = By.XPATH, value = "//input[@name='copy-link']").get_attribute('value')
                return link
            elif rule_check == "nz":
                if GeoGuessorBot.game_setting(self):
                    noDefaultBtn = self.wait.until(EC.element_to_be_clickable((By.XPATH,"//div[@class='game-settings_default__DIBgs']//div//input[@type='checkbox']")))
                    noDefaultBtn.click()
                    GeoGuessorBot.time_slider(self, timer)
                    time.sleep(1)
                    GeoGuessorBot.no_zoom(self)
                else:
                    GeoGuessorBot.time_slider(self, timer)
                    time.sleep(1)
                    GeoGuessorBot.no_zoom(self)

                link = self.driver.find_element(by = By.XPATH, value = "//input[@name='copy-link']").get_attribute('value')
                return link
            elif rule_check == "nmz":
                if GeoGuessorBot.game_setting(self):
                    noDefaultBtn = self.wait.until(EC.element_to_be_clickable((By.XPATH,"//div[@class='game-settings_default__DIBgs']//div//input[@type='checkbox']")))
                    noDefaultBtn.click()
                    GeoGuessorBot.time_slider(self, timer)
                    time.sleep(1)
                    GeoGuessorBot.no_move_zoom(self)
                else:
                    GeoGuessorBot.time_slider(self, timer)
                    time.sleep(1)
                    GeoGuessorBot.no_move_zoom(self)

                link = self.driver.find_element(by = By.XPATH, value = "//input[@name='copy-link']").get_attribute('value')
                return link
            elif rule_check == "nmpz":
                if GeoGuessorBot.game_setting(self):
                    noDefaultBtn = self.wait.until(EC.element_to_be_clickable((By.XPATH,"//div[@class='game-settings_default__DIBgs']//div//input[@type='checkbox']")))
                    noDefaultBtn.click()
                    GeoGuessorBot.time_slider(self, timer)
                    time.sleep(1)
                    GeoGuessorBot.no_move_zoom_pan(self)
                else:
                    GeoGuessorBot.time_slider(self, timer)
                    time.sleep(1)
                    GeoGuessorBot.no_move_zoom_pan(self)

                link = self.driver.find_element(by = By.XPATH, value = "//input[@name='copy-link']").get_attribute('value')
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