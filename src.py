from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

root_url = 'https://lkml.org/lkml'
year_urls = []
month_urls = []
day_urls = []
driver = webdriver.Chrome() # to open the browser 
wait = WebDriverWait(driver, 10)


def get_month_urls(url):
  driver.get(url)
  year = url[-4:]
  
  months = driver.find_elements(By.TAG_NAME, "a")

  for i in range(len(months)):
    if '{year}/' in url and (len(month_urls) == 0 or url != month_urls[-1])\
      and url != 'https://lkml.org/lkml/last100':
      month_urls.append(url)

def get_day_urls(url):
  driver.get(url)
  year = url[-7:-3]
  month = url[-3:]
  
  days = driver.find_elements(By.TAG_NAME, "a")

  for i in range(len(days)):
    if '{year}/{month}/' in url and (len(day_urls) == 0 or url != day_urls[-1])\
      and url != 'https://lkml.org/lkml/last100':
      day_urls.append(url)


driver.get(root_url) 
years = driver.find_elements(By.TAG_NAME, "a")

for i in range(len(years)):
  url = years[i].get_attribute("href")

  if url is None or url == "":
    continue
  
  elif ("lkml/" in url and (len(year_urls) == 0 or url != year_urls[-1]))\
      and url != 'https://lkml.org/lkml/last100':
    year_urls.append(url)


for i in range(len(year_urls)):
  # 'https://lkml.org/lkml/{year}/{nonth}/'
  url = year_urls[i].get_attribute("href")

  if url is None or url == "":
    continue

  get_month_urls(url)

for i in range(len(month_urls)):
  url = month_urls[i].get_attribute("href")

  if url is None or url == "":
    continue

  get_day_urls(url)

for i in range(day_urls):
  url = day_urls[i].get_attribute("href")

  if url is None or url == "":
    continue

  driver.get(url)
  



two_four_home = 'https://lkml.org/lkml/2024'
driver.get(two_four_home) 
two_four = driver.find_elements(By.TAG_NAME, "a")
two_four_months = []
two_four_urls = []

for i in range(len(two_four)):
  url = two_four[i].get_attribute("href")

  if url is None or url == "":
    continue
  
  elif "2024/" in url and (len(two_four_months) == 0 or url != two_four_months[-1]):
    two_four_months.append(url)


for i in range(len(two_four_months)):
  driver.get(two_four_months[i])
  jan_days = driver.find_elements(By.TAG_NAME, "a")

  for i in range(len(jan_days)):
    url = jan_days[i].get_attribute("href")

    if url is None or url == "":
      continue
    
    elif (("/1/" in url or "/2/" in url or "/3/" in url or "/4/" in url\
        or "/5/" in url or "/6/" in url or "/7/" in url or "/8/" in url\
        or "/9/" in url or "/10/" in url or "/11/" in url or "/12/" in url)\
        and (len(two_four_urls) == 0 or url != two_four_urls[-1])):
      two_four_urls.append(url)


# with open("driverWordCount.txt", "r+") as file:
#   for url in two_four_urls:
#     file.write(str(url))
#     file.write('\n')