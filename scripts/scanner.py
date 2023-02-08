
import unicodedata 
import re
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import urllib.request
import csv
import os

def slugify(value, allow_unicode=False):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')


def getPicture(urlSource, i):
	driver.get(urlSource)
	image = driver.find_element_by_xpath("//div[@class='media__preview']/img[1]")
	url = image.get_attribute("src")
	caption = image.get_attribute("alt")
	shortCaption = caption
	folder = int(i % 100)
	if folder != lastFolder:
		try:
			os.stat(f'{picPath}/{folder}')
		except:
			os.mkdir(f'{picPath}/{folder}')
			lastFolder = folder
	if len(caption) > 30:
		shortCaption = caption[:30]
	urllib.request.urlretrieve(url, f'./pics/{folder}/{slugify(shortCaption)}.jpg')
	print(f'Got picture from {urlSource}')

def getVideo(urlSource, i):
	driver.get(urlSource)
	video = driver.find_element_by_xpath("//video[@class='js-media-player media__player']")
	url = video.get_attribute("src")
	caption = urlSource.split('/video/',1)[1]
	shortCaption = caption
	folder = int(i % 100)
	if len(caption) > 30:
		shortCaption = caption[:30]
	urllib.request.urlretrieve(url, f'./vids/{folder}/{slugify(shortCaption)}.mp4')
	print(f'Got video from {urlSource}')
	
with open("config.json") as configuration:
	mainPath = configuration.storage.folder
	chromeDriver = configuration.drivers.chrome

vidPath = mainPath + '/vids'
picPath = mainPath + '/pics'

opt = webdriver.ChromeOptions()
opt.add_argument("--start-maximized")
#prefs = {"profile.managed_default_content_settings.images":2}
#opt.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(chromeDriver,options=opt)
driver.implicitly_wait(10)
listOfPicURLs = []
listOfVidURLs = []
# Setup tests
# with open(f'{mainPath}/scripts/smiles20210329015700.csv', newline='\r\n') as csvfile:
# 	reader = csv.reader(csvfile)
# 	i = 0
# 	for row in reader:
# 		print(row)
# 		i += 1
# 		if row[0] == "P":
# 			listOfPicURLs.append(row[1])
# 		elif row[0] == "U":
# 			listOfVidURLs.append(row[1])
	

print("Getting pictures....")
p = listOfPicURLs.count
# Loop through all URLs and save pictures or movies
while p > 6000:
	p -= 1
	getPicture(listOfPicURLs[p], p)

reverseVidList = []
for url in listOfVidURLs:
	reverseVidList.append(url)
time.sleep(5)
print("Getting videos.....")
v=0
for url in reverseVidList:
	v += 1
	getPicture(url, v)

driver.close()


