from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC  
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import time
import sys
import urllib.request
from urllib.parse import quote_plus
from tqdm import tqdm
linksTaggedPic = []
linksPersonalPic = []

#user login data
username = input('Your complete name on Facebook: ')
password = input('Your password: ')

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
		i = i+1

def saveLinks(arr):
	print('\n')
	print('Saving links...')
	sys.stdout.flush()
	links = driver.find_elements_by_class_name("uiMediaThumb")
	for x in tqdm(links):
		arr.append(x.get_attribute("href"))

#start browser
options = FirefoxOptions()
options.add_argument("--headless")
_browser_profile = webdriver.FirefoxProfile()
_browser_profile.set_preference("dom.webnotifications.enabled", False)
binary = FirefoxBinary("C:\\Program Files\\Mozilla Firefox\\firefox.exe")
driver = webdriver.Firefox(firefox_profile=_browser_profile, firefox_options=options, executable_path=r'geckodriver.exe')
wait = WebDriverWait(driver, 10)

#login
print("Login...")
print('\n')
sys.stdout.flush()
driver.get("http://www.facebook.com")
driver.find_element_by_id("email").send_keys(username)
driver.find_element_by_id("pass").send_keys(password)
driver.find_element_by_xpath("//input[@type='submit']").send_keys(Keys.RETURN)
time.sleep(3)
#open user photo page and load all pictures where the user is tagged
print("Login done.")
print('\n')
sys.stdout.flush()
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

downloadPic(linksTaggedPic,'C:\\Users\\spina\\Desktop\\fb\\taggedPhotos\\')
downloadPic(linksPersonalPic,'C:\\Users\\spina\\Desktop\\fb\\personalPhotos\\')

driver.quit()