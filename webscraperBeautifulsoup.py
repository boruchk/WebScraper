from time import sleep
import re
import requests
from bs4 import BeautifulSoup


ROOTURL = 'https://lkml.org/lkml'
KEYWORDS = ['desktop', ' pc ']
YEARFILEPATH = "urls\yearUrls.txt"
MONTHFILEPATH = "urls\monthUrls.txt"
DAYFILEPATH = "urls\dayUrls.txt"
CHANGELOGFILEPATH = "urls\changelogurls.txt"
MENTIONFILEPATH = "daysMentioned.txt"



def fetch_url_with_backoff(url, retryCount=4, backOffFactor=1):
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
  fetchedHtml = fetch_url_with_backoff(ROOTURL)
  if fetchedHtml is None:
    print("Failed to fetch content from the URL.")
    return
  
  soup = BeautifulSoup(fetchedHtml.text, features="xml")
  for child in soup.findAll('a', class_="nb"):
    if len(child.text) == 4:
      file.write(f"https://lkml.org{child.get('href')}\n")

  file.close()


def get_month_urls(monthFile, year_url):
  fetchedHtml = fetch_url_with_backoff(year_url)
  if fetchedHtml is None:
    print("Failed to fetch content from the URL.")
    return
  
  soup = BeautifulSoup(fetchedHtml.text, features="xml")
  for child in soup.findAll('a', class_="nb"):
    if len(child.text) == 8:
      monthFile.write(f"https://lkml.org{child.get('href')}\n")


def get_day_urls(dayFile, month_url):
  fetchedHtml = fetch_url_with_backoff(month_url)
  if fetchedHtml is None:
    print("Failed to fetch content from the URL.")
    return
  
  soup = BeautifulSoup(fetchedHtml.text, features="xml")
  for child in soup.findAll('a', class_="nb"):
    if len(child.text) >= 10 and len(child.text) <= 11:
      dayFile.write(f"https://lkml.org{child.get('href')}\n")


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


def search_urls(mentionFile, changelog_url):
  fetchedHtml = fetch_url_with_backoff(changelog_url)
  if fetchedHtml is None:
    print("Failed to fetch content from the URL.")
    return

  soup = BeautifulSoup(fetchedHtml.text, features="xml")
  result = soup.get_text().lower()
  pattern = r"/lkml/(\d{4})"  # Captures the year of the changelog
  year = re.search(pattern, changelog_url).group(1)[-4:]
  for word in KEYWORDS:
    if word in result:
      mentionFile.write(f"{year} - {word} - {changelog_url}\n")

        

# Start of program

# get_year_urls()

# yearFile = open(YEARFILEPATH, 'r')
# monthFile = open(MONTHFILEPATH, 'r')
# for year_url in yearFile:
#   get_month_urls(monthFile, year_url.strip('\n'))
# yearFile.close()
# monthFile.close()

# monthFile = open(MONTHFILEPATH, 'r')
# dayFile = open(DAYFILEPATH, 'r')
# for month_url in monthFile:
#   get_day_urls(dayFile, month_url.strip('\n'))
# monthFile.close()
# dayFile.close()

# dayFile = open(DAYFILEPATH, 'r')
# changelogFile = open(CHANGELOGFILEPATH, 'a')
# for day_url in dayFile:
#   get_changelog_urls(changelogFile, day_url.strip('\n'))
# dayFile.close()
# changelogFile.close()

urlFile = open(CHANGELOGFILEPATH, 'r')
mentionFile = open(MENTIONFILEPATH, 'a')
for changelog_url in urlFile:
  search_urls(mentionFile, changelog_url.strip('\n'))
  urlFile.readline()

urlFile.close()
mentionFile.close()