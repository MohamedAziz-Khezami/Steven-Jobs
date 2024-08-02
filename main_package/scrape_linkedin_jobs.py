

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






#Getting job description from linkedin jobs

def scrape_linkedin_jobs_description(df: pd.DataFrame) -> pd.DataFrame:
    
    
    
    
    #Changing date format
    def convert_relative_date(relative_date_str):
        """Converts a relative date string (e.g., "1 year ago", "2 months ago") to an actual date."""
        relative_date_str = relative_date_str.replace("+", "").strip()
        
        match = re.match(r"(\d+) (\w+) ago", relative_date_str)
        if not match:
            return None

        amount, unit = int(match.group(1)), match.group(2)

        now = datetime.datetime.now()

        if unit == "year" or unit == "years":
            delta = datetime.timedelta(days=amount * 365)
        elif unit == "month" or unit == "months":
            delta = datetime.timedelta(days=amount * 30)  # Approximation
        elif unit == "day" or unit == "days":
            delta = datetime.timedelta(days=amount)
        elif unit == "hour" or unit == "hours":
            delta = datetime.timedelta(hours=amount)
        elif unit == "minute" or unit == "minutes":
            delta = datetime.timedelta(minutes=amount)
        elif unit == "second" or unit == "seconds":
            delta = datetime.timedelta(seconds=amount)
        elif unit == "week" or unit == "weeks":
            delta = datetime.timedelta(weeks=amount)
        
        else:
            return None

        actual_date = now - delta
        return actual_date.strftime("%Y-%m")
    
    
    
    user = UserAgent()

    
    storage = []
    
    for u in tqdm.tqdm(df.links, desc="Scraping jobs"):
        headers =  {
            'User-Agent': user.random
        }

        url = u
        english_url = url.replace('tn.linkedin.com','www.linkedin.com') 
        
    
        try:
            request = requests.get(english_url, timeout=3600 , headers= headers)
        
        except Exception as e :
            print(e)
            continue
        
        if request.status_code != 200:
    

            continue
        
            
        soup = BeautifulSoup(request.text, 'html.parser')
        time.sleep(3)
        
        job_title = soup.find('h1', {'class': 'top-card-layout__title font-sans text-lg papabear:text-xl font-bold leading-open text-color-text mb-0 topcard__title'})
        job_description = soup.find('div', {'class': 'show-more-less-html__markup show-more-less-html__markup--clamp-after-5 relative overflow-hidden'})
        company = soup.find('a', {'class': 'topcard__org-name-link topcard__flavor--black-link'})
        location = soup.find('span', {'class': 'topcard__flavor topcard__flavor--bullet'})
        post_date = soup.find('span', {'class': 'posted-time-ago__text topcard__flavor--metadata'})


        
        criteria = soup.find_all('span', {'class': 'description__job-criteria-text description__job-criteria-text--criteria'})
    
    
        
        storage.append({'post_date': convert_relative_date(post_date.text.strip()) if post_date else "2024-01",
                        'job_title':job_title.text.strip() if job_title else "None", 
                        'job_description':job_description.text.strip() if job_description else "None", 
                        'company':company.text.strip() if company else "None",
                        'location':location.text.strip() if location else "None", 
                        'seniority': criteria[0].text.strip() if criteria and len(criteria) > 0 else "None",
                        'employement_type': criteria[1].text.strip() if criteria and len(criteria) > 1 else "None",
                        'job_functions': criteria[2].text.strip() if criteria and len(criteria) > 2 else "None",
                        'industry': criteria[3].text.strip() if criteria and len(criteria) > 3 else "None",
                        
                        })
    dff = pd.DataFrame(storage, columns=['post_date','job_title','job_description','company','location','seniority','employement_type','job_functions','industry'])
    
    try:
        dff.post_date = pd.to_datetime(dff.post_date, format="%Y-%m")
    except:
        pass
    
    return dff