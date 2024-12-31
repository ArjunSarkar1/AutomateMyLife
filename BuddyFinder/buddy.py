from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from time import sleep
from dotenv import load_dotenv
import os

MAX_TIME = 30

load_dotenv()

class BuddyBot():
    def __init__(self):
        self.driver = webdriver.Chrome()

    
    def open_bumble(self):
        try:
            self.driver.get("https://bumble.com/")
            sleep(2)

            sign_in = self.driver.find_element(By.XPATH ,"/html/body/div/main/section[1]/div/div[2]/div/div[2]/div/div[3]/a")
            sign_in.click()
            
            sleep(2)

            self.fb_login()
        except Exception as e:
            print(f"An error occurred while opening Bumble:\n{e}")
            raise


    def fb_login(self):
        try:
            facebook_option = self.driver.find_element(By.XPATH, "/html/body/div/div/div[1]/div[2]/main/div/div[3]/form/div[1]/div/div[2]/button/span/span[2]/span")
            facebook_option.click()

            sleep(4)

            # Switching Windows 
            main_window = self.driver.current_window_handle
            for handle in self.driver.window_handles:
                if handle != main_window:
                    self.driver.switch_to.window(handle)

            fb_email = self.driver.find_element("xpath", "/html/body/div/div[2]/div[1]/form/div/div[1]/div/input")
            fb_email.click()
            fb_email.send_keys(os.getenv('FB_EMAIL'))
            
            sleep(2)

            fb_pass = self.driver.find_element("xpath", "/html/body/div/div[2]/div[1]/form/div/div[2]/div/input")
            fb_pass.click()
            fb_pass.send_keys(os.getenv('FB_PASS'))
            
            sleep(1)
            
            login_button = self.driver.find_element("xpath", "/html/body/div/div[2]/div[1]/form/div/div[3]/label[2]/input")
            login_button.click()
            
            sleep(6)

            continue_btn = self.driver.find_element("xpath", "/html/body/div[1]/div/div/div/div/div/div/div[1]/div[3]/div/div/div/div/div/div/div[2]/div/div/div[1]/div/div/div/div[1]/div/div/div/div/div/div[1]/div/span/span")
            continue_btn.click()

            #sleep(MAX_TIME)
            # I am in this stage where I have to drag an drop image from directory inside the current directory
            # Drag and drop those picture on the window
            
            # Switching back to Main Window
            self.driver.switch_to.window(main_window)
        
            ######################################
            # Giving Time to drop your pictures.....
            ######################################
            sleep(MAX_TIME/5)

            # continue_btn2 = self.driver.find_element("xpath","/html/body/div/div/div[1]/div[2]/main/div/div[4]/form/div[3]/button")
            # continue_btn2.click()

            # sleep(MAX_TIME/4.0)

            ####################################
            
            # enable_location = self.driver.find_element("xpath","/html/body/div/div/div[1]/div[2]/main/div/div[5]/form/div/button")
            # enable_location.click()

            # sleep(MAX_TIME/4.0)

            # continue_btn3 = self.driver.find_element("xpath","/html/body/div/div/div[1]/div[1]/main/div/div[8]/button")
            # continue_btn3.click()

            # sleep(4.0)
            
            # continue_btn4 = self.driver.find_element("xpath","/html/body/div/div/div[1]/div[1]/main/section/div/div[3]/button")
            # continue_btn4.click()

            # sleep(4.0)

            # ###########
            # female_choice = self.driver.find_element("xpath","/html/body/div/div/div[1]/main/div[2]/div/div/span/div/section/div/div[2]/div/div/div[2]/button")
            # female_choice.click()
            # ###########

            # sleep(4.0)

            # continue_btn5 = self.driver.find_element("xpath","/html/body/div/div/div[1]/main/div[2]/div/div/span/div/section/div/div[3]/button")
            # continue_btn5.click()
            ##########################
            for i in range(10):
                like_button = self.driver.find_element("xpath","/html/body/div/div/div[1]/main/div[2]/div/div/span/div[2]/div/div[2]/div/div[2]/div/div[1]/span")
                like_button.click()
                sleep(2)

            sleep(2)

            self.quit_browser()

        except Exception as e:
            print(f"An error occurred during Facebook Login:\n{e}")
            raise
    
    def quit_browser(self):
        try:
            self.driver.quit()
        except Exception as e:
            print(f"Error while quitting the Web Browser:\n{e}")

myBot = BuddyBot()
try:
    myBot.open_bumble()
except Exception as e:
    print(f"Script encountered an error:\n{e}")
finally:
    myBot.quit_browser()