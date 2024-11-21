from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

root_url = 'https://lkml.org/lkml'
year_urls = []
month_urls = []
day_urls = []
changelog_urls = []
driver = webdriver.Chrome() # to open the browser 
wait = WebDriverWait(driver, 10)

keywords = ['desktop', 'Desktop', 'DESKTOP', ' pc ', ' Pc ', ' PC ']
filePath = "daysMentioned.txt"


def get_year_urls():
  years = driver.find_elements(By.TAG_NAME, "a")

  for i in range(len(years)):
    url = years[i].get_attribute("href")

    if url is None or url == "":
      continue
    
    elif ("lkml/" in url and (len(year_urls) == 0 or url != year_urls[-1]))\
        and url != 'https://lkml.org/lkml/last100':
      year_urls.append(url)


def get_month_urls(year_url):
  driver.get(year_url)
  year = year_url[-4:] + '/'
  
  months = driver.find_elements(By.TAG_NAME, "a")

  for i in range(len(months)):
    url = months[i].get_attribute("href")
    if year in url and (len(month_urls) == 0 or url != month_urls[-1])\
      and url != 'https://lkml.org/lkml/last100':
      month_urls.append(url)


def get_day_urls(month_url):
  driver.get(month_url)
  year = month_url[-7:-3]
  month = month_url[-3:]
  text = year + month + '/'
  
  days = driver.find_elements(By.TAG_NAME, "a")

  for i in range(len(days)):
    url = days[i].get_attribute("href")
    if text in url and (len(day_urls) == 0 or url != day_urls[-1])\
      and url != 'https://lkml.org/lkml/last100':
      day_urls.append(url)


def get_changelog_urls(day_url):
  driver.get(day_url)
  text = day_url[-8:] + '/'

  changelogs = driver.find_elements(By.TAG_NAME, "a")

  for i in range(len(changelogs)):
    url = changelogs[i].get_attribute("href")
    if text in url and (len(day_urls) == 0 or url != day_urls[-1])\
      and url != 'https://lkml.org/lkml/last100':
      changelog_urls.append(url)


def search_urls(file, changelog_url):
  driver.get(changelog_url)

  textboxes = driver.find_elements(By.TAG_NAME, "pre")

  for i in range(len(textboxes)):
    for word in keywords:
      if textboxes[i].find_elements(By.XPATH, f"//*[contains(text(), '{word}')]"):
        date = changelog_url[-12:]
        file.write(f"{date} - {word}")
        file.write('\n')

# Start of program

driver.get(root_url) 
get_year_urls()
for year_url in year_urls:
  get_month_urls(year_url)

for month_url in month_urls:
  get_day_urls(month_url)

for day_url in day_urls:
  get_changelog_urls(day_url)
  
# test code
# for i in range(3):
#   get_day_urls(month_urls[i])
# for i in range(1):
#   get_changelog_urls(day_urls[i])

file = open(filePath, 'w')
for changelog_url in changelog_urls:
  search_urls(file, changelog_url)

file.close()