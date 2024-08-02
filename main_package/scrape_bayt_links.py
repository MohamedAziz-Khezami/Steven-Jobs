# Libraries
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


# Scraping bayt job links
def scrape_bayt_links() -> pd.DataFrame:

    url = "https://www.bayt.com/en/tunisia/jobs/?page=1"

    driver = webdriver.Chrome()

    page = 1

    df = []

    while True:

        driver.get(url)
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

        link = driver.find_elements(By.CSS_SELECTOR, ".col.u-stretch.t-large.m0")

        for l in link:
            df.append(l.find_element(By.TAG_NAME, "a").get_attribute("href"))

        page += 1

        url = f"https://www.bayt.com/en/tunisia/jobs/?page={page}"

        if page == 17:
            break

    dff = pd.DataFrame(df, columns=["links"])

    return dff
