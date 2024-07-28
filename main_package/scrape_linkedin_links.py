
#Libraries
import pandas as pd
import numpy as np

from bs4 import BeautifulSoup
import requests
import pandas as pd
import tqdm
from requests_ip_rotator import ApiGateway

from fake_useragent import UserAgent
from itertools import cycle
import random 
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import csv
import time

import datetime
import re










#Scraping linkedin job links
def scrape_linkedin_links() -> pd.DataFrame:
    
    url = "https://www.linkedin.com/jobs/search?location=Tunisia&geoId=102134353&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&currentJobId=3796559592"
    service = Service(ChromeDriverManager().install())  
    driver = webdriver.Chrome(service=service)
    driver.get(url)
  



    df = pd.DataFrame(columns=['links'])

    while True:
        global links
        global df1
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        links = driver.find_elements(By.CSS_SELECTOR,".base-card__full-link.absolute.top-0.right-0.bottom-0.left-0.p-0")
        l = [link.get_attribute('href') for link in links]
        df1 = pd.DataFrame(l, columns=['links'])
       

            
        try:
            
            more = driver.find_element(By.CSS_SELECTOR,".infinite-scroller__show-more-button.infinite-scroller__show-more-button--visible")
        
            if more:
                time.sleep(2)
                more.click()
    


            
        except:
            continue
        
        if len(df1) == len(df):
            continue
        else:
            df = pd.concat([df,df1],axis=0,ignore_index=True)

        if len(df) >=3:
            driver.close()
            break
            
    return df
