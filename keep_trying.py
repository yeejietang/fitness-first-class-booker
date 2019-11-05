#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 24 10:54:50 2019

@author: yeejie.tang
"""

import time
import requests
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from credentials import ff_web_login, ff_valerie_login
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
from bs4 import BeautifulSoup

class ffchrome(Chrome):

    executable_path = '/usr/local/bin/chromedriver'
    time_to_wait = 5 # Implicit wait seconds
    ff_website = 'https://clients.mindbodyonline.com/LoginLaunch?studioid=741470'
    gym_selector = 'a.selectBox.bf-filter.selectBox-dropdown' 
    options = Options()
    # options.headless = True
    # options.add_argument("--no-startup-window")
    
    def __init__(self, gym, login, password):
        Chrome.__init__(self, self.executable_path, options=self.options) 
        Chrome.implicitly_wait(self, self.time_to_wait) 
        Chrome.get(self, self.ff_website) 
        Chrome.find_element_by_css_selector(self, self.gym_selector).click() # Expand gym location dropdown
        Chrome.find_element_by_link_text(self, gym).click() # Choose gym
        Chrome.find_element_by_id(self, 'requiredtxtUserName').send_keys(login) 
        Chrome.find_element_by_id(self, 'requiredtxtPassword').send_keys(password) 
        Chrome.find_element_by_id(self, 'btnLogin').click() # Login

def book_class(driver, class_button):
    time.sleep(2)
    driver.quit()

# Get credentials
yj_login = ff_web_login['login']
yj_pwd = ff_web_login['password']
val_login = ff_valerie_login['login']
val_pwd = ff_valerie_login['password']




# soup = BeautifulSoup(requests.get('https://clients.mindbodyonline.com/LoginLaunch?studioid=741470').text, 'html.parser')
# print(soup.prettify())




# Initialize
driver1 = ffchrome('MBFC', yj_login, yj_pwd)
# driver2 = ffchrome('MBFC', val_login, val_pwd)

# Wait to load
time.sleep(2)

element = driver1.find_element_by_name('but2700')
print(element.get_attribute('value'))


# Click through to classes
# driver1.find_element_by_name('but2700').click()

# driver1.quit()

# Try to book:
# try:
#     element = WebDriverWait(driver1, 5).until(
#         EC.presence_of_element_located((By.XPATH, "//input[@value='Make a single reservation']"))
#         )
#     driver1.find_element_by_xpath("//input[@value='Make a single reservation']").click() 
# finally:
#     driver1.quit()

# try:
#     element = WebDriverWait(driver2, 5).until(
#         EC.presence_of_element_located((By.XPATH, "//input[@value='Make a single reservation']"))
#         )
# finally:
#     driver2.quit()

