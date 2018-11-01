from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC  
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.common.exceptions import TimeoutException
import time
import sys
import os, errno
import datetime
import getpass
import logging
import urllib.request
from urllib.parse import quote_plus
from tqdm import tqdm
linksTaggedPic = []
linksPersonalPic = []
now = datetime.datetime.now()
LOG_FILE = './log.txt'
logging.basicConfig(filename=LOG_FILE, format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s', datefmt='%H:%M:%S', level=logging.DEBUG)

#user data
username = input('Your complete name on Facebook: ')
password = getpass.getpass('Your password: ')
savePath = input('Path were you want to save your pictures (please use double backspace -> \\\): ')

def loadPic():
	while True:
		numPic = len(driver.find_elements_by_class_name("uiMediaThumb"))
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		time.sleep(3)
		loadedPic = len(driver.find_elements_by_class_name("uiMediaThumb"))
		print('\n')
		print('Found ' + str(loadedPic) + ' pictures.')
		sys.stdout.flush()
		if numPic == loadedPic:
			break
		numPic = loadedPic

def downloadPic(arr,path):
	print('\n')
	print('Downloading pictures...')
	sys.stdout.flush()
	i = 1
	#for link in tqdm(arr):
	for link in arr:
		try:
			time.sleep(2)
			driver.get(link)
			wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'spotlight')))
			#time.sleep(5)
			print('Get picture ' + str(i) + ' of ' + str(len(arr)) +'...')
			sys.stdout.flush()
			src = driver.find_element_by_class_name("spotlight").get_attribute("src")
			size = round((urllib.request.urlopen(src).length / 1024),2)
			print ("Size: " + str(size) + " Kb")
			sys.stdout.flush()
			while True:
				if size < 1:
					print('Wrong pic, is too little, try again...')
					sys.stdout.flush()
					driver.get(link)
					wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'spotlight')))
					newSrc = driver.find_element_by_class_name("spotlight").get_attribute("src")
					newSize = round((urllib.request.urlopen(newSrc).length / 1024),2)
					size = newSize
					src = newSrc
				else:
					print(str(size) + 'KB ok, downloading...')
					print('\n')
					sys.stdout.flush()
					urllib.request.urlretrieve(src, path + 'pic_' + str(i) + '.jpg')
					break
		except TimeoutException:
			raise
		i = i+1

def saveLinks(arr):
	print('\n')
	print('Saving links...')
	sys.stdout.flush()
	links = driver.find_elements_by_class_name("uiMediaThumb")
	for x in tqdm(links):
		arr.append(x.get_attribute("href"))

try:
	#start browser
	_browser_profile = webdriver.FirefoxProfile()
	_browser_profile.set_preference("dom.webnotifications.enabled", False)
	binary = FirefoxBinary("C:\\Program Files\\Mozilla Firefox\\firefox.exe")
	driver = webdriver.Firefox(firefox_profile=_browser_profile, executable_path=r'geckodriver.exe')
	driver.set_window_position(-2000, 0)
	wait = WebDriverWait(driver, 10)

	#login
	print('Creating folders...')
	os.makedirs(savePath + '/FacebookBackup_' + str(now.day) + '_' + str(now.month) + '_' + str(now.year) + '_' + str(now.hour) + '_' + str(now.minute) + '/taggedPhotos')
	taggedPhotosPath = savePath + '/FacebookBackup_'  + str(now.day) + '_' + str(now.month) + '_' + str(now.year) + '_' + str(now.hour) + '_' + str(now.minute) + '/taggedPhotos/'
	os.makedirs(savePath + '/FacebookBackup_' + str(now.day) + '_' + str(now.month) + '_' + str(now.year) + '_' + str(now.hour) + '_' + str(now.minute) + '/personalPhotos')
	personalPhotosPath = savePath + '/FacebookBackup_' + str(now.day) + '_' + str(now.month) + '_' + str(now.year) + '_' + str(now.hour) + '_' + str(now.minute) + '/personalPhotos/'
	print("Login...")
	print('\n')
	sys.stdout.flush()
	driver.get("http://www.facebook.com")
	time.sleep(1)
	driver.find_element_by_id("email").send_keys(username)
	time.sleep(1)
	driver.find_element_by_id("pass").send_keys(password)
	time.sleep(1)
	driver.find_element_by_xpath("//input[@type='submit']").send_keys(Keys.RETURN)
	time.sleep(3)
	#open user photo page and load all pictures where the user is tagged
	try:
		driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[1]/div/div/div/div[2]/div[1]/div[1]/div/a").click()
		print("Login done.")
		print('\n')
		sys.stdout.flush()
	except:
		print("Username or password wrong!")
		sys.stdout.flush()
		time.sleep(1)
		print("Exiting...")
		sys.stdout.flush()
		time.sleep(3)
		driver.quit()
		sys.exit()
	driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[1]/div/div/div/div[2]/div[1]/div[1]/div/a").click()
	time.sleep(2)
	profileUrl = driver.current_url

	#get all download links of tagged pictures
	driver.find_element_by_xpath("//*[@data-tab-key='photos']").click()
	time.sleep(2)
	print('Loading pictures where you are tagged...')
	loadPic()
	saveLinks(linksTaggedPic)

	#get all download links of personal pictures
	driver.get(profileUrl + '/photos_all')
	time.sleep(2)
	print('Loading all your pictures...')
	loadPic()
	saveLinks(linksPersonalPic)

	downloadPic(linksTaggedPic,taggedPhotosPath)
	downloadPic(linksPersonalPic,personalPhotosPath)
	#'C:\\Users\\spina\\Desktop\\fb\\taggedPhotos\\'
	#'C:\\Users\\spina\\Desktop\\fb\\personalPhotos\\'
	driver.quit()
except:
	print('ops... an error occurred. Please open an issue on GitHub (https://github.com/daaanny90/Facebook-Photo-Backup-CLI/issues) with the content of the last error in the log file.')
	sys.stdout.flush()
	logging.exception('Error')
	time.sleep(3)
	driver.quit()
	sys.exit()
	
