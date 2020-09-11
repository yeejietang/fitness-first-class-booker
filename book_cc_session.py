#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 15:12:50 2019

@author: yeejie.tang
"""

import time
import pause
from selenium.webdriver import Chrome
from credentials import cc_login
from datetime import datetime

class gymchrome(Chrome):

    executable_path = '/usr/local/bin/chromedriver' 
    # Tells driver to implicitly wait for elements for 10 seconds before timing out
    time_to_wait = 10     
    ccf_website = 'https://app.rockgympro.com/b/?&bo=7f3e222bae344639836173664e9772ea'
    ccsh_website = 'https://app.rockgympro.com/b/?&bo=7c9070dab3f64c9f8350a0e19b236405'
    ccn_website = 'https://app.rockgympro.com/b/?&bo=0f37da39e8fb43d4967d679ad7b5059b'
    
    def __init__(self, gym):
        Chrome.__init__(self, self.executable_path) 
        Chrome.implicitly_wait(self, self.time_to_wait) 
        
        if gym == 'ccf':
            Chrome.get(self, self.ccf_website) 
        elif gym == 'ccsh':
            Chrome.get(self, self.ccsh_website) 
        else:
            Chrome.get(self, self.ccn_website)
        
        Chrome.maximize_window(self) 
        Chrome.find_element_by_xpath(self, '//*[@id="profile-link-div"]/div/a').click() 
        login_modal = Chrome.find_element_by_id(self, 'rgp00-embedded-modal-frame')
        self.switch_to.frame(login_modal)
        Chrome.find_element_by_id(self, 'inputEmail').send_keys(cc_login['login']) 
        Chrome.find_element_by_id(self, 'inputPassword').send_keys(cc_login['password'])
        Chrome.find_element_by_xpath(self, '/html/body/div[1]/div/div/form/div[1]/label/input').click()
        # Click login
        Chrome.find_element_by_xpath(self, '/html/body/div[1]/div/div/form/a[2]').click()
        # Click done and exit
        Chrome.find_element_by_xpath(self, '/html/body/div[1]/div/div/div[1]/a').click()


# Check which day are we running this script 
# dow = Monday is 0, Sunday is 6
dow = datetime.today().weekday()

# Initialize browser sessions
driver1 = gymchrome('ccsh')

# Wait 2 seconds before all other actions
time.sleep(2)

# Decide when to run the rest of the code
dt = datetime.now()
y, m, d = dt.year, dt.month, dt.day
pause.until(datetime(y, m, d, 19))

# Start timer
start = time.time()

# Refresh at certain time
driver1.refresh()

# Click on 3 days from today
d_plus_3 = d + 3
driver1.find_element_by_partial_link_text(str(d_plus_3)).click()

# Two persons
driver1.find_element_by_xpath('//*[@id="theform"]/div[6]/div/fieldset[2]/table/tbody/tr[1]/td[1]/a[2]').click()
driver1.find_element_by_xpath('//*[@id="theform"]/div[6]/div/fieldset[2]/table/tbody/tr[1]/td[1]/a[2]').click()

# 5pm slot
#driver1.find_element_by_xpath('//*[@id="offering-page-select-events-table"]/tbody/tr[11]/td[4]/a').click()

# 7pm slot
driver1.find_element_by_xpath('//*[@id="offering-page-select-events-table"]/tbody/tr[14]/td[4]/a').click()

# Me first
driver1.find_element_by_id('pfirstname-pindex-1-1').send_keys('Yee Jie')
driver1.find_element_by_id('plastname-pindex-1-1').send_keys('Tang')

yj_month_xpath = '//select[@id="participant-birth-pindex-1month"]/option[text()="' + cc_login['yj_month'] + '"]'
yj_day_xpath = '//select[@id="participant-birth-pindex-1day"]/option[text()="' + cc_login['yj_day'] + '"]'
yj_year_xpath = '//select[@id="participant-birth-pindex-1year"]/option[text()="' + cc_login['yj_year'] + '"]'

driver1.find_element_by_xpath(yj_month_xpath).click()
driver1.find_element_by_xpath(yj_day_xpath).click()
driver1.find_element_by_xpath(yj_year_xpath).click()

# Val 2nd
driver1.find_element_by_id('pfirstname-pindex-1-2').send_keys('Valerie')
driver1.find_element_by_id('plastname-pindex-1-2').send_keys('Chang')

val_month_xpath = '//select[@id="participant-birth-pindex-2month"]/option[text()="' + cc_login['val_month'] + '"]'
val_day_xpath = '//select[@id="participant-birth-pindex-2day"]/option[text()="' + cc_login['val_day'] + '"]'
val_year_xpath = '//select[@id="participant-birth-pindex-2year"]/option[text()="' + cc_login['val_year'] + '"]'

driver1.find_element_by_xpath(val_month_xpath).click()
driver1.find_element_by_xpath(val_day_xpath).click()
driver1.find_element_by_xpath(val_year_xpath).click()

# Info correct
driver1.find_element_by_xpath('//*[@id="theform"]/fieldset[3]/div[2]/span/input').click()

# YJ phone
driver1.find_element_by_xpath('//*[@id="p143cb51f5af8844ef9ea240fe04ffcd57"]').send_keys(cc_login['yj_phone'])

# Val phone
driver1.find_element_by_xpath('//*[@id="p243cb51f5af8844ef9ea240fe04ffcd57"]').send_keys(cc_login['val_phone'])

# Next page
driver1.find_element_by_partial_link_text('CONTINUE').click()

# Wait 1 second for some stuff to prefill
time.sleep(1)

# Agree terms
driver1.find_element_by_xpath('//*[@id="theform"]/fieldset[5]/div[2]/input').click() 

# Complete booking
driver1.find_element_by_partial_link_text('Complete Booking').click()

# End timer
end = time.time()
print("Time Taken: {:.6f}s".format(end-start))

# Wait 2 seconds before quitting
time.sleep(2)
driver1.quit()








#ids = driver1.find_elements_by_xpath('//*[@id]')
#for i in ids:
#    print(i.get_attribute('id'))