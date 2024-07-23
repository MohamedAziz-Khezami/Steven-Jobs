import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import csv
import time



url = "https://www.linkedin.com/jobs/search?location=Tunisia&geoId=102134353&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&currentJobId=3796559592"
service = Service(ChromeDriverManager().install())  # Download and configure ChromeDriver
webdriver = webdriver.Chrome(service=service)
webdriver.get(url)
time.sleep(10)

links = webdriver.find_elements(By.CSS_SELECTOR,".base-card__full-link.absolute.top-0.right-0.bottom-0.left-0.p-0")

for link in links:
    print(link.get_attribute('href'))


'''
while True:
    webdriver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

    
    if len(links) >= 300:
        break
        
'''