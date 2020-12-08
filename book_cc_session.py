#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 15:12:50 2019

@author: yeejie.tang
"""

# Import statements
import time
import pause
import calendar
from selenium.webdriver import Chrome
from credentials import cc_login
from datetime import datetime
from datetime import timedelta 

# Change these variables
gym_to_book = 'ccf' #('ccsh', 'ccf', 'ccn') 
hour_to_book = 18
minute_to_book = 30
days_later = 3
running_test = False
persons_to_book = ['yj', 'val'] #['yj', 'val', 'kyle']. 'yj' is always in

# Main Script
class gymchrome(Chrome):

    executable_path = '/usr/local/bin/chromedriver' 
    time_to_wait = 10 # Tells driver to implicitly wait for elements for 10 seconds before timing out
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
        Chrome.find_element_by_xpath(self, '/html/body/div[1]/div/div/form/a[2]').click() # Click login
        Chrome.find_element_by_xpath(self, '/html/body/div[1]/div/div/div[1]/a').click() # Click done and exit

# Page 1
driver1 = gymchrome(gym_to_book) # Initialize browser sessions
time.sleep(2) # Wait 2 seconds before all other actions
dt = datetime.now()
y, m, d = dt.year, dt.month, dt.day
if not running_test: # If running test, don't want to pause
    pause.until(datetime(y, m, d, 12, 0)) # Pause until booking is open
start = time.time() # Start timer
driver1.refresh() # Refresh at certain time
day_to_book = dt + timedelta(days=days_later) # Find date for 3 (or other amount) days later
month_dict = {v: k for k,v in enumerate(calendar.month_name)}
ui_month = driver1.find_element_by_class_name('ui-datepicker-month').text
if day_to_book.month - m == 1 and month_dict[ui_month] != day_to_book.month: # If need be, click cross month
    driver1.find_element_by_partial_link_text('Next').click() 
driver1.find_element_by_partial_link_text(str(day_to_book.day)).click() 
driver1.find_element_by_xpath('//*[@id="theform"]/div[6]/div/fieldset[2]/table/tbody/tr[1]/td[1]/a[2]').click()
if 'val' in persons_to_book:
    driver1.find_element_by_xpath('//*[@id="theform"]/div[6]/div/fieldset[2]/table/tbody/tr[1]/td[1]/a[2]').click()
if 'kyle' in persons_to_book:
    driver1.find_element_by_xpath('//*[@id="theform"]/div[6]/div/fieldset[2]/table/tbody/tr[2]/td[1]/a[2]').click()

# weekday_dict = {
#     '110': '1',
#     '1130': '2',
#     '120': '3',
#     '1230': '4',
#     '1330': '5',
#     '140': '6',
#     '1430': '7',
#     '150': '8',
#     '160': '9',
#     '1630': '10',
#     '170': '11',
#     '1730': '12',
#     '1830': '13',
#     '190': '14',
#     '1930': '15',
#     '200': '16',
#     '2050': '17'
# }

weekday_dict = {
    '100': '1',
    '110': '2',
    '1230': '3',
    '1330': '4',
    '150': '5',
    '160': '6',
    '1730': '7',
    '1830': '8',
    '200': '9',
    '2050': '10'
}

# weekend_dict = {
#     '90': '1',
#     '930': '2',
#     '100': '3',
#     '1030': '4',
#     '1130': '5',
#     '120': '6',
#     '1230': '7',
#     '130': '8',
#     '140': '9',
#     '1430': '10',
#     '150': '11',
#     '1530': '12',
#     '1630': '13',
#     '170': '14',
#     '1730': '15',
#     '180': '16',
#     '1850': '17'
# }

weekend_dict = {
    '90': '1',
    '100': '2',
    '1130': '3',
    '1230': '4',
    '140': '5',
    '150': '6',
    '1630': '7',
    '1730': '8',
    '1850': '9'
}

if day_to_book.weekday()<5: # Weekday
    slot = weekday_dict[str(hour_to_book)+str(minute_to_book)]
else: # Weekend
    slot = weekend_dict[str(hour_to_book)+str(minute_to_book)] 
xpath_for_date = '//*[@id="offering-page-select-events-table"]/tbody/tr[' + str(slot) + "]/td[4]/a"
driver1.find_element_by_xpath(xpath_for_date).click() # click on correct timeslot to book

# Page 2
driver1.find_element_by_id('pfirstname-pindex-1-1').send_keys('Yee Jie') # Fill in details
driver1.find_element_by_id('plastname-pindex-1-1').send_keys('Tang')
yj_month_xpath = '//select[@id="participant-birth-pindex-1month"]/option[text()="' + cc_login['yj_month'] + '"]'
yj_day_xpath = '//select[@id="participant-birth-pindex-1day"]/option[text()="' + cc_login['yj_day'] + '"]'
yj_year_xpath = '//select[@id="participant-birth-pindex-1year"]/option[text()="' + cc_login['yj_year'] + '"]'
driver1.find_element_by_xpath(yj_month_xpath).click()
driver1.find_element_by_xpath(yj_day_xpath).click()
driver1.find_element_by_xpath(yj_year_xpath).click()
if 'val' in persons_to_book:
    driver1.find_element_by_id('pfirstname-pindex-1-2').send_keys('Valerie')
    driver1.find_element_by_id('plastname-pindex-1-2').send_keys('Chang')
    p2_month_xpath = '//select[@id="participant-birth-pindex-2month"]/option[text()="' + cc_login['val_month'] + '"]'
    p2_day_xpath = '//select[@id="participant-birth-pindex-2day"]/option[text()="' + cc_login['val_day'] + '"]'
    p2_year_xpath = '//select[@id="participant-birth-pindex-2year"]/option[text()="' + cc_login['val_year'] + '"]'
    driver1.find_element_by_xpath(p2_month_xpath).click()
    driver1.find_element_by_xpath(p2_day_xpath).click()
    driver1.find_element_by_xpath(p2_year_xpath).click()
    if 'kyle' in persons_to_book:
        driver1.find_element_by_id('pfirstname-pindex-1-3').send_keys('Kyle')
        driver1.find_element_by_id('plastname-pindex-1-3').send_keys('Malinda-White')
        p3_month_xpath = '//select[@id="participant-birth-pindex-3month"]/option[text()="' + cc_login['kyle_month'] + '"]'
        p3_day_xpath = '//select[@id="participant-birth-pindex-3day"]/option[text()="' + cc_login['kyle_day'] + '"]'
        p3_year_xpath = '//select[@id="participant-birth-pindex-3year"]/option[text()="' + cc_login['kyle_year'] + '"]'
        driver1.find_element_by_xpath(p3_month_xpath).click()
        driver1.find_element_by_xpath(p3_day_xpath).click()
        driver1.find_element_by_xpath(p3_year_xpath).click()
elif len(persons_to_book) == 2 and 'kyle' in persons_to_book:
    driver1.find_element_by_id('pfirstname-pindex-1-2').send_keys('Kyle')
    driver1.find_element_by_id('plastname-pindex-1-2').send_keys('Malinda-White')
    p2_month_xpath = '//select[@id="participant-birth-pindex-2month"]/option[text()="' + cc_login['kyle_month'] + '"]'
    p2_day_xpath = '//select[@id="participant-birth-pindex-2day"]/option[text()="' + cc_login['kyle_day'] + '"]'
    p2_year_xpath = '//select[@id="participant-birth-pindex-2year"]/option[text()="' + cc_login['kyle_year'] + '"]'
    driver1.find_element_by_xpath(p2_month_xpath).click()
    driver1.find_element_by_xpath(p2_day_xpath).click()
    driver1.find_element_by_xpath(p2_year_xpath).click()
    
driver1.find_element_by_xpath('//*[@id="theform"]/fieldset[3]/div[2]/span/input').click() # Info correct

if gym_to_book == 'ccsh':
    xpath_for_yj_phone = '//*[@id="p143cb51f5af8844ef9ea240fe04ffcd57"]'
    xpath_for_p2_phone = '//*[@id="p243cb51f5af8844ef9ea240fe04ffcd57"]'
    xpath_for_p3_phone = '//*[@id="p343cb51f5af8844ef9ea240fe04ffcd57"]'
elif gym_to_book == 'ccf':
    xpath_for_yj_phone = '//*[@id="p1e3b93e774a2c44d4ab04966274738d2f"]'
    xpath_for_p2_phone = '//*[@id="p2e3b93e774a2c44d4ab04966274738d2f"]'
    xpath_for_p3_phone = '//*[@id="p3e3b93e774a2c44d4ab04966274738d2f"]'
else:
    xpath_for_yj_phone = '//*[@id="p1176490489e1d4072b70770d637208e84"]'
    xpath_for_p2_phone = '//*[@id="p2176490489e1d4072b70770d637208e84"]'
    xpath_for_p3_phone = '//*[@id="p3176490489e1d4072b70770d637208e84"]'

driver1.find_element_by_xpath(xpath_for_yj_phone).send_keys(cc_login['yj_phone'])
if 'val' in persons_to_book:
    driver1.find_element_by_xpath(xpath_for_p2_phone).send_keys(cc_login['val_phone'])
    if 'kyle' in persons_to_book:
        driver1.find_element_by_xpath(xpath_for_p3_phone).send_keys(cc_login['kyle_phone'])
elif len(persons_to_book) == 2 and 'kyle' in persons_to_book:
    driver1.find_element_by_xpath(xpath_for_p2_phone).send_keys(cc_login['kyle_phone'])
driver1.find_element_by_partial_link_text('CONTINUE').click()


# Page 3
time.sleep(1) # Wait 1 second for some stuff to prefill
driver1.find_element_by_xpath('//*[@id="theform"]/fieldset[5]/div[2]/input').click() # Agree terms
if not running_test: # If running test, don't want to book
    driver1.find_element_by_partial_link_text('Complete Booking').click() # Complete booking


# End
end = time.time()
print("Time Taken: {:.6f}s".format(end-start))
# time.sleep(2) # Wait 2 seconds before quitting
# if not running_test: # If running test, don't want to quit
#     driver1.quit()