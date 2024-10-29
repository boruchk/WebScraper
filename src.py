from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


driver = webdriver.Chrome() # to open the browser 
wait = WebDriverWait(driver, 10)


root_url = 'https://lkml.org/lkml'
driver.get(root_url) 
years = driver.find_elements(By.TAG_NAME, "a")
years_urls = []
months_urls = []


def get_months(driver, year):
  for i in range(len(5)):
    if '{year}/' in url and (len(months_urls) == 0 or url != months_urls[-1]):
      months_urls.append(url)

for i in range(len(years)):
  url = years[i].get_attribute("href")

  if url is None or url == "":
    continue
  
  elif ("lkml/" in url and (len(years_urls) == 0 or url != years_urls[-1]))\
      and url != 'https://lkml.org/lkml/last100':
    years_urls.append(url)


for i in range(len(years_urls)):
  'https://lkml.org/lkml/2024/1'
  url = years_urls[i]
  driver.get(url)

  year = years_urls[0][-4:]
  get_months(driver, year)

  months = driver.find_elements(By.TAG_NAME, "a")





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