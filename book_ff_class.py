#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 15:12:50 2019

@author: yeejie.tang
"""

import time
import pause
from selenium.webdriver import Chrome
from credentials import ff_web_login, ff_valerie_login
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed

class ffchrome(Chrome):

    executable_path = '/usr/local/bin/chromedriver' 
    # Tells driver to implicitly wait for elements for 5 seconds before timing out
    time_to_wait = 7 
    ff_website = 'https://clients.mindbodyonline.com/LoginLaunch?studioid=741470'
    gym_selector = 'a.selectBox.bf-filter.selectBox-dropdown' 
    drivers = [] # registrar 
    
    def __init__(self, gym, login, password):
        self.drivers.append(self) 
        Chrome.__init__(self, self.executable_path) 
        Chrome.implicitly_wait(self, self.time_to_wait) 
        Chrome.get(self, self.ff_website) 
        # Expand gym location dropdown
        Chrome.find_element_by_css_selector(self, self.gym_selector).click() 
        # Choose gym
        Chrome.find_element_by_link_text(self, gym).click() 
        # Login
        Chrome.find_element_by_id(self, 'requiredtxtUserName').send_keys(login) 
        Chrome.find_element_by_id(self, 'requiredtxtPassword').send_keys(password) 
        Chrome.find_element_by_id(self, 'btnLogin').click() 
        
    def book_class(self, class_button):
        Chrome.find_element_by_name(self, class_button).click() 
        
    @classmethod
    def refresh_all(cls):
        for driver in cls.drivers:
            driver.refresh()
            
    @classmethod
    def click_book_button(cls):
        for driver in cls.drivers:
            driver.find_element_by_xpath("//input[@value='Make a single reservation']").click() 
        
    @classmethod
    def quit_all(cls):
        for driver in cls.drivers:
            driver.quit()

def refresh_and_book_class(driver, class_button):
    driver.refresh()
    driver.find_element_by_name(class_button).click()
    driver.find_element_by_xpath("//input[@value='Make a single reservation']").click() 
    time.sleep(2)
    driver.quit()

# Check which day are we running this script 
# dow = Monday is 0, Sunday is 6
dow = datetime.today().weekday()

# List of classes I'd be interested in booking (but often run out quick)
# GRIT STRENGTH, Wednesday 1:00pm, MBFC (Yeoh)                  but820
# GRIT STRENGTH, Wednesday 7:10pm, MBFC (Nelson)                but2700
# GRIT STRENGTH, Thursday 6:50pm, MBFC (Yeoh)                   but902
# Circuit, Thursday 7:25pm, MBFC (Yeoh)                         but906
# BODYPUMP, Friday , MarketStreet (Gavin)                       but6370
# BODYPUMP, Saturday 9:15am, Paragon (Bertram)                  but7197
# GRIT STRENGTH, Saturday 2:35pm, Metropolis (Yeoh)             but2705
# Circuit, Satuday 3:10pm, Metropolis (Yeoh)                    but1467
# BODYPUMP, Sunday 4:55pm, Paragon (Bertram)                    but7223
# Circuit, Monday 6:40pm, Paragon (Yeoh)                        but7284

# Get credentials
yj_login = ff_web_login['login']
yj_pwd = ff_web_login['password']
val_login = ff_valerie_login['login']
val_pwd = ff_valerie_login['password']

# Initialize browser sessions
if dow == 0:
    driver1 = ffchrome('MBFC', yj_login, yj_pwd)
    driver2 = ffchrome('MBFC', yj_login, yj_pwd)
elif dow == 1:
    driver1 = ffchrome('MBFC', yj_login, yj_pwd)
    driver2 = ffchrome('MBFC', yj_login, yj_pwd)
    driver3 = ffchrome('MBFC', val_login, val_pwd)
    driver4 = ffchrome('MBFC', val_login, val_pwd)
# elif dow == 2:
#     driver1 = ffchrome('MarketStreet')
# elif dow == 3:
#     driver1 = ffchrome('Paragon')
#     driver2 = ffchrome('Metropolis')
#     driver3 = ffchrome('Metropolis')
# elif (dow == 4 or dow == 5):
#     driver1 = ffchrome('Paragon')
else:
    exit()

# Wait 2 seconds before all other actions
time.sleep(2)

# Decide when to run the rest of the code
dt = datetime.now()
y, m, d = dt.year, dt.month, dt.day
pause.until(datetime(y, m, d, 8))

# Start timer
# start = time.time()

# Refresh
# ffchrome.refresh_all()

# Book gym classes
with ThreadPoolExecutor(max_workers=None) as executor:
    if dow == 0:
        futures = [ executor.submit(refresh_and_book_class, driver1, 'but820'), 
                    executor.submit(refresh_and_book_class, driver2, 'but2700') ] 
    elif dow == 1:
        futures = [ executor.submit(refresh_and_book_class, driver1, 'but902'), 
                    executor.submit(refresh_and_book_class, driver2, 'but906'),
                    executor.submit(refresh_and_book_class, driver1, 'but902'), 
                    executor.submit(refresh_and_book_class, driver2, 'but906') ] 

# Click all book buttons
# ffchrome.click_book_button()

# End timer
# end = time.time()
# print("Time Taken: {:.6f}s".format(end-start))

# Wait 2 seconds before quitting drivers
# time.sleep(2)
# ffchrome.quit_all()