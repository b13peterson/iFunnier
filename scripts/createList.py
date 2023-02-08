
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import datetime
import urllib.request
import csv
import time
import json

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scroll_down():
	"""A method for scrolling the page."""

	# Get scroll height.
	last_height = driver.execute_script("return document.body.scrollHeight")
	scrollCount = 0
	print(f'beginning scroll with {scrollCount} scrolls.')
	while True:
		# Scroll down to the bottom.
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

		# Wait to load the page.
		time.sleep(1)
		scrollCount += 1
		if scrollCount % 60 == 0:
			print(f'scrollCount = {scrollCount}')

		# Calculate new scroll height and compare with last scroll height.
		new_height = driver.execute_script("return document.body.scrollHeight")

		if new_height == last_height:

			break

		last_height = new_height


opt = webdriver.ChromeOptions()
opt.add_argument("--start-maximized")
prefs = {"profile.managed_default_content_settings.images":2}
opt.add_experimental_option("prefs", prefs)


with open("config.json") as configuration:
	driver = webdriver.Chrome(configuration.drivers.chrome, options=opt)

driver.implicitly_wait(10)
driver.get("https://ifunny.co/")

# Login stuff
driver.find_element_by_xpath("//a[@data-test='login-link']").click()
email = driver.find_element_by_xpath("//input[@type='text' and @name='email']")
password = driver.find_element_by_xpath("//input[@type='password' and @name='password']")
#email.send_keys()
#password.send_keys()
time.sleep(30)

userNavXPath = "//img[@class='navigation__user-avatar']"


#driver.get("https://ifunny.co/account/smiles")

ignored_exceptions=(NoSuchElementException,StaleElementReferenceException,)
try:
	userNav = WebDriverWait(driver, 10,ignored_exceptions=ignored_exceptions).until(
	EC.presence_of_element_located((By.XPATH, userNavXPath)))
finally:
	userNav.click()

#driver.find_element_by_xpath("//img[@class='navigation__user-avatar']").click()
driver.find_element_by_xpath("//a[@data-test='user-menu-profile' and @class='user-menu__profile']").click()
driver.find_element_by_xpath("//a[@href='/account/smiles']").click()

scroll_down()

links = driver.find_elements_by_css_selector("a")
timestamp = datetime.datetime.now()
with open("config.json") as configuration:
	storage = json.load(configuration).storage
	csvName = f'{storage.folder}/{storage.list}{timestamp}.csv'

with open(csvName, 'w', newline='') as csvfile:
	writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	print('writing to csv log file')
	linkCount = 0
	for link in links:
		linkUrl = link.get_attribute("href")
		linkType = ""
		if '/picture/' in linkUrl:
			linkType = "P"
		elif '/video/' in linkUrl:
			linkType = "U"

		if linkType != "":
			linkCount += 1
			if linkCount % 100 == 0:
				print(f'csv at row ={linkCount}')
			writer.writerow([linkType, link.get_attribute("href")])

driver.close()