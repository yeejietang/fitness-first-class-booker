import time
import pause
from datetime import datetime 
from selenium import webdriver 

# Path for chromedriver
# /usr/local/bin/chromedriver

def open_page_and_login(driver, website, gym, login, pwd):
	# Tells driver to implicitly wait for elements for 15 seconds before timing out
	driver.implicitly_wait(15) 
	# Open website
	driver.get(website) 
	# Expand gym location dropdown
	driver.find_element_by_css_selector('a.selectBox.bf-filter.selectBox-dropdown').click() 
	# Choose gym
	driver.find_element_by_link_text(gym).click() 
	# Login
	driver.find_element_by_id('requiredtxtUserName').send_keys(login) 
	driver.find_element_by_id('requiredtxtPassword').send_keys(pwd) 
	driver.find_element_by_id('btnLogin').click() 
	return 

def refresh_and_book(driver, classbut):
	driver.refresh()
	driver.find_element_by_name(classbut).click()
	driver.find_element_by_xpath("//input[@value='Make a single reservation']").click()

def main():
	# Set variables
	ff_website = 'https://clients.mindbodyonline.com/LoginLaunch?studioid=741470' 
	yj_login = #
	yj_pwd = #

	# Gym List 
	mbfc = 'MBFC' 
	tanjong = '100AM (Tanjong Pag...' 
	bugis = 'Bugis Junction' 
	captow = 'Capital Tower' 
	mktst = 'MarketStreet' 
	orq = 'One Raffles Quay' 
	paragon = 'Paragon' 
	metro = 'Metropolis' 

	

	# Check which day are we running this script 
	# dow = Monday is 0, Sunday is 6
	dow = datetime.today().weekday()

	# Open webpages and login
	if (dow == 0 or dow == 1):
		driver1, driver2 = webdriver.Chrome(), webdriver.Chrome() 
		open_page_and_login(driver1, ff_website, mbfc, yj_login, yj_pwd) 
		open_page_and_login(driver2, ff_website, mbfc, yj_login, yj_pwd) 
	elif dow == 3:
		driver1, driver2, driver3 = webdriver.Chrome(), webdriver.Chrome(), webdriver.Chrome() 
		open_page_and_login(driver1, ff_website, paragon, yj_login, yj_pwd) 
		open_page_and_login(driver2, ff_website, metro, yj_login, yj_pwd) 
		open_page_and_login(driver3, ff_website, metro, yj_login, yj_pwd) 
	# On other days don't run
	else: 
		return 

	# Only run the following codes AT 8AM PRECISELY 
	dt = datetime.now() 
	y, m, d = dt.year, dt.month, dt.day 
	pause.until(datetime(y, m, d, 8)) 

	# Refreshes
	driver1.refresh() 
	# Refresh additional browsers if needed
	if (dow == 0 or dow == 1 or dow == 3): 
		driver2.refresh() 
		if dow == 3:
			driver3.refresh() 

	# Book relevant classes
	# Monday (Wednesday Classes)
	if dow == 0:
		driver1.find_element_by_name('but820').click() 
		driver2.find_element_by_name('but2700').click() 
	# Tuesday (Thursday Classes)
	if dow == 1:
		driver1.find_element_by_name('but902').click() 
		driver2.find_element_by_name('but906').click() 
	# 
	if dow == 3:
		driver1.find_element_by_name('but7197').click() 
		driver2.find_element_by_name('but2705').click() 
		driver3.find_element_by_name('but1467').click() 

	# Click on book button
	driver1.find_element_by_xpath("//input[@value='Make a single reservation']").click() 
	# Click on additional book buttons
	if (dow == 0 or dow == 1 or dow == 3): 
		driver2.find_element_by_xpath("//input[@value='Make a single reservation']").click() 
		if dow == 3:
			driver3.find_element_by_xpath("//input[@value='Make a single reservation']").click() 

	# Close browsers
	time.sleep(2)
	driver1.close()
	# Close additional browsers 
	if (dow == 0 or dow == 1 or dow == 3): 
		driver2.close() 
		if dow == 3:
			driver3.close() 

	# OLD Signup for classes you're interested in
	# driver.find_element_by_xpath("//*[contains(@onclick, 'GRIT STRENGTH at 6:50 pm  on Thursday')]").click()
	# driver2.find_element_by_xpath("//*[contains(@onclick, 'Circuit at 7:25 pm  on Thursday')]").click()

	# OLD Login After Choosing Class
	# driver.find_element_by_id('su1UserName').send_keys(yj_login)
	# driver2.find_element_by_id('su1UserName').send_keys(yj_login)
	# driver.find_element_by_id('su1Password').send_keys(yj_pwd)
	# driver2.find_element_by_id('su1Password').send_keys(yj_pwd)
	# driver.find_element_by_id('btnSu1Login').click()
	# driver2.find_element_by_id('btnSu1Login').click()

	return 

if __name__ == '__main__':
	main()