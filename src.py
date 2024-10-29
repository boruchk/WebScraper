import time 
from selenium import webdriver 
from datetime import datetime 

driver = webdriver.Chrome() # to open the browser 

# url of google news website 
url = 'https://lkml.org/lkml'

# to open the url in the browser 
driver.get(url) 
# time.sleep(1)

all_links = driver.find_elements("xpath", "(//a)")
last_link_diff = 0
for link in all_links:
  last_link_diff += 1

print("last link diff = ", last_link_diff)
# while(True): 
#   now = datetime.now() 
    
#   current_time = now.strftime("%H:%M:%S") 
#   print(f'At time : {current_time} IST') 
#   c = 1

#   for link_diff in range(3, last_link_diff): 
#     curr_path = '' 
      
#     try: 
#       year_path = f'/html/body/table/tbody/tr[2]/td[3]/table/tbody/tr[{link_diff}]/td[2]/a'
#       # title = driver.find_elements("xpath", year_path) 
#       driver.get(year_path)
#       desktop_ct = driver.find_element('desktop')
#     except: 
#       print("exception", end='\n')
#       continue
    
#     print(f"Heading {c}: ") 
#     c += 1
#     for val in title:
#       print(val.text) 
      

#   for month_var in range(13):
#     month_path = f'/html/body/table/tbody/tr[2]/td[3]/table/tbody/tr[{month_var}]/td[1]/a'
        
#   # to stop the running of code for 10 mins 
#   time.sleep(600)  
