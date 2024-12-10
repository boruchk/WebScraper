from time import sleep
import requests
import lxml as lxmlThing
from bs4 import BeautifulSoup

# exponential backoff
root_url = 'https://lkml.org/lkml'
year_urls = []
month_urls = []
day_urls = []
changelog_urls = []

keywords = ['return', 'port'] 
# keywords = ['desktop', 'Desktop', 'DESKTOP', ' pc ', ' Pc ', ' PC ']
urlFilePath = "changelogurls.txt"
mentionFilePath = "daysMentioned.txt"



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


def search_urls(file, changelog_url):
  fetchedHtml = fetch_url_with_backoff(changelog_url)
  if fetchedHtml is None:
    print("Failed to fetch content from the URL.")
    return

  soup = BeautifulSoup(fetchedHtml, "lxml")
  found = soup.findAll('pre', string=keywords)

  date = changelog_url[-12:]
  file.write(f"{date} - {found}")
  file.write('\n')

        

# Start of program

# response = requests.get('https://lkml.org/lkml/2020/5/5/7') 
urlFile = open(urlFilePath, 'r')
mentionFile = open(mentionFilePath, 'w')

search_urls(mentionFile, 'https://lkml.org/lkml/2020/5/5/7')
# get_year_urls()
# for year_url in year_urls:
#   get_month_urls(year_url)

# for month_url in month_urls:
#   get_day_urls(month_url)

# for day_url in day_urls:
#   get_changelog_urls(day_url)
  
# test code
# for i in range(3):
#   get_day_urls(month_urls[i])
# for i in range(1):
#   get_changelog_urls(day_urls[i])

# urlFile = open(urlFilePath, 'r')
# mentionFile = open(mentionFilePath, 'w')
# for changelog_url in changelog_urls:
#   search_urls(mentionFile, changelog_url)

urlFile.close()
mentionFile.close()