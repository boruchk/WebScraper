from time import sleep
import re
import requests
from bs4 import BeautifulSoup

# exponential backoff
root_url = 'https://lkml.org/lkml'
year_urls = []
month_urls = []
day_urls = []
changelog_urls = []

keywords = ['desktop', 'Desktop', 'DESKTOP', ' pc ', ' Pc ', ' PC ']



def fetch_url_with_backoff(url, retryCount=5, backOffFactor=1):
  for attempt in range(retryCount):
    try:
      response = requests.get(url)
      response.raise_for_status()
      return response
    except requests.exceptions.HTTPError as e:
      if attempt < retryCount:
        waitTime = backOffFactor * (2 ** attempt)
        print(f"HTTPError: {e}. Retrying in {waitTime} seconds...")
        sleep(waitTime)
      else:
        print("Max retries reached. Could not fetch the URL.")
        return None
    except requests.exceptions.RequestException as e:
      print(f"An error occurred: {e}")
      return None


def get_year_urls():
  file = open("urls\yearUrls.txt", 'a')
  fetchedHtml = fetch_url_with_backoff(root_url)
  if fetchedHtml is None:
    print("Failed to fetch content from the URL.")
    return
  
  soup = BeautifulSoup(fetchedHtml.text, features="xml")
  for child in soup.findAll('a', class_="nb"):
    if len(child.text) == 4:
      file.write(f"https://lkml.org{child.get('href')}\n")

  file.close()


def get_month_urls(yearFile, year_url):
  fetchedHtml = fetch_url_with_backoff(year_url)
  if fetchedHtml is None:
    print("Failed to fetch content from the URL.")
    return
  
  soup = BeautifulSoup(fetchedHtml.text, features="xml")
  for child in soup.findAll('a', class_="nb"):
    if len(child.text) == 8:
      yearFile.write(f"https://lkml.org{child.get('href')}\n")


def get_day_urls(monthFile, month_url):
  fetchedHtml = fetch_url_with_backoff(month_url)
  if fetchedHtml is None:
    print("Failed to fetch content from the URL.")
    return
  
  soup = BeautifulSoup(fetchedHtml.text, features="xml")
  for child in soup.findAll('a', class_="nb"):
    if len(child.text) >= 10 and len(child.text) <= 11:
      monthFile.write(f"https://lkml.org{child.get('href')}\n")


def get_changelog_urls(changelogFile, day_url):
  fetchedHtml = fetch_url_with_backoff(day_url)
  if fetchedHtml is None:
    print("Failed to fetch content from the URL.")
    return
  
  soup = BeautifulSoup(fetchedHtml.text, features="xml")
  for child in soup.findAll('a', class_="nb"):
    text = child.get('href')
    if len(child.get('href')) >= 16 and len(child.get('href')) <= 21:
      changelogFile.write(f"https://lkml.org{child.get('href')}\n")


def search_urls(changelog_url):
  fetchedHtml = fetch_url_with_backoff(changelog_url)
  if fetchedHtml is None:
    print("Failed to fetch content from the URL.")
    return

  soup = BeautifulSoup(fetchedHtml.text, features="xml")
  result = soup.get_text()
  date = changelog_url[-10:]
  for word in keywords:
    if word in result:
      file.write(f"{date} - {word}")
      file.write('\n')    

        

# Start of program

# get_year_urls()

# yearFile = open("urls\yearUrls.txt", 'r')
# for year_url in file:
#   get_month_urls(yearFile, year_url.strip('\n'))
# yearFile.close()

# monthFile = open("urls\monthUrls.txt", 'r')
# for month_url in file:
#   get_day_urls(monthFile, month_url.strip('\n'))
# monthFile.close()

dayFile = open("urls\dayUrls.txt", 'r')
changelogFile = open("urls\changelogurls.txt", 'a')
for day_url in dayFile:
  get_changelog_urls(changelogFile, day_url.strip('\n'))
dayFile.close()
changelogFile.close()

urlFile = open(urlFilePath, 'r')
mentionFile = open(mentionFilePath, 'w')
for changelog_url in changelog_urls:
  search_urls(mentionFile, changelog_url)

# urlFile.close()
# mentionFile.close()