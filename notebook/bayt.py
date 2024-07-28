

from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
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













url = "https://www.bayt.com/en/tunisia/jobs/?page=1"


page = 1

df = []

while True:
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.by import By
    from webdriver_manager.chrome import ChromeDriverManager


    webdriver = webdriver.Firefox()
    webdriver.get(url)
    time.sleep(2)
    webdriver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)

    link = webdriver.find_elements(By.CSS_SELECTOR,".col.u-stretch.t-large.m0")
    
    l = [i.find_element(By.TAG_NAME,"a").get_attribute('href') for i in link]
    
    df.append(l)

    
    page += 1
    
    url = f"https://www.bayt.com/en/tunisia/jobs/?page={page}"
    
    if len(df) >= 2000:
        break


print(df)