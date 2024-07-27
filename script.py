
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

from transformers import pipeline

import google.generativeai as genai

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

        if len(df) >= 400:
            driver.close()
            break
            
    return df


#Scraping bayt job links
def scrape_bayt_links() -> pd.DataFrame:

    url = "https://www.bayt.com/en/tunisia/jobs/?page=1"

    service = Service(ChromeDriverManager().install())  
    driver = webdriver.Chrome(service=service)

    page = 1

    df = []

    while True:


        driver.get(url)
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

        link = driver.find_elements(By.CSS_SELECTOR,".col.u-stretch.t-large.m0")
        
        for l in link:
            df.append(l.find_element(By.TAG_NAME,"a").get_attribute('href'))

    
        
        page += 1
        
        url = f"https://www.bayt.com/en/tunisia/jobs/?page={page}"
        
        if page == 15:
            break

    dff = pd.DataFrame(df, columns=['links'])
    
    return dff




        

#Getting job description from linkedin jobs
def scrape_linkedin_jobs_description(df: pd.DataFrame) -> pd.DataFrame:
    
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
    
    
        
        storage.append({'post_date': convert_relative_date(post_date.text.strip()) if post_date else None,
                        'job_title':job_title.text.strip() if job_title else None, 
                        'job_description':job_description.text.strip() if job_description else None, 
                        'company':company.text.strip() if company else None,
                        'location':location.text.strip() if location else None, 
                        'seniority': criteria[0].text.strip() if criteria and len(criteria) > 0 else None,
                        'employement_type': criteria[1].text.strip() if criteria and len(criteria) > 1 else None,
                        'job_functions': criteria[2].text.strip() if criteria and len(criteria) > 2 else None,
                        'industry': criteria[3].text.strip() if criteria and len(criteria) > 3 else None,
                        
                        })
    dff = pd.DataFrame(storage, columns=['post_date','job_title','job_description','company','location','seniority','employement_type','job_functions','industry'])
    
    return dff
    

#Scraping bayt job links
def scrape_bayt_jobs_description(df: pd.DataFrame) -> pd.DataFrame:
    user = UserAgent()


    storage = pd.DataFrame(columns=['post_date','job_title','job_description','company','location'])


    for u in tqdm.tqdm(df.links, desc="Scraping jobs"):
        headers =  {
            'User-Agent': user.random
        }

        url = u
        
    
        try:
            request = requests.get(url, timeout=3600 , headers= headers)
        
        except Exception as e :
            print(e)
            continue
        
        if request.status_code != 200:
            continue
        
            
        soup = BeautifulSoup(request.text, 'html.parser')
        time.sleep(2)
        
        post_date = soup.find('div', {'class': 't-small t-mute m10b'})
        
        job_title = soup.find('h1', {'class': 'h3 t-break'})

        job_description = soup.find('div', {'class': 't-break'})

        company = soup.find('a', {'class': 'is-black t-bold'})

        location = soup.find('span', {'class': 't-mute'})
        


        
        criteria = soup.find_all('dl', {'class': 'dlist is-spaced is-fitted t-small'})
        
        
        
    
    
    
        
        a = pd.DataFrame({'post_date':convert_relative_date(post_date.text.strip().split('\n')[0]) if post_date else None,
                        'job_title':job_title.text.strip() if job_title else None, 
                        'job_description':job_description.text.strip() if job_description else None, 
                        'company':company.text.strip() if company else None,
                        'location':location.text.strip() if location else None, 
                        'industry': criteria[0].text.strip().split('\n')[5] if criteria else None,
    
                        
                        } , index=[0])

        

        storage = pd.concat([storage,a] ,axis=0)

    return storage


        

#Getting job description from linkedin jobs using gemini
def skills_extraction(job_desc):
    prompt_empy = '{"key_words":[]}'

    prompt = '''
    Read the following job description and return key words of all the skills required for this job.

    No explanations, uniques keywords, no duplicates, Be breif.

    '''
    
    genai.configure(api_key="AIzaSyAX5hRxjQ64IqZxqNcdj7ONpALMWxnIHb0")

    model = genai.GenerativeModel('gemini-1.5-flash')
    
    if job_desc == "":
        prompt_id = prompt_empy
    else:
        prompt_id = prompt + job_desc
    output = model.generate_content(prompt_id)

    
    return output.candidates[0].content.parts[0].text.strip().replace("-","").split('\n')




#Extracting skills from all job descriptions
def get_skills(df: pd.DataFrame) -> pd.DataFrame:
    
    description = df.job_description
    
    batch_size = len(description) // 12
    
    batches = np.array_split(description, batch_size)

    # Access individual batches
    batchs = [batches[0], batches[1], batches[2], batches[3], batches[4] , batches[5], batches[6], batches[7], batches[8], batches[9], batches[10], batches[11]]
    
    
    bat = []                

    for i in batchs:
        b= ""
        for j in str(i):
            b = b + j
        bat.append(b)
    
    
    
    ln_skills = []

    for i in tqdm.tqdm(bat, desc="Extracting skills"):
        s = skills_extraction(i)
        ln_skills.append(s)
        
        
    ls = []
    for i in ln_skills:
        for j in i:
            ls.append(j)


    return pd.DataFrame(ls, columns=['skills'])









def main():
        
    ln_links = scrape_linkedin_links()
    print(ln_links.head(3))
    print(ln_links.shape)

    bayt_links = scrape_bayt_links()
    print(bayt_links.head(3))
    print(bayt_links.shape)
    
    print('Starting jobs scraping in 5 sec, please turn on proxy switcher')
    time.sleep(5)
    
    print('Scraping jobs from linkedin:')
    ln_jobs = scrape_linkedin_jobs_description(ln_links)
    print(ln_jobs.head(3))
    print(ln_jobs.shape)
    
    print('Scraping jobs from bayt:')
    bayt_jobs = scrape_bayt_jobs_description(bayt_links)
    print(bayt_jobs.head(3))
    print(bayt_jobs.shape)
    
    print('Extracting skills form linkedin and bayt jobs')
    ln_skills = get_skills(ln_jobs)
    
    print('waiting for 1 min')
    time.sleep(65)
    
    bayt_skills = get_skills(bayt_jobs)
  
    
    
    total_skills = pd.concat([ln_skills, bayt_skills])

    print('Translating skills...')
    Translator = pipeline("translation", model="Helsinki-NLP/opus-mt-mul-en")
    total_skills_english = total_skills.skills.apply(lambda x: Translator(x)[0]['translation_text'])
    
    ln_jobs.job_title = ln_jobs.job_title.apply(lambda x: Translator(x)[0]['translation_text'])
    
    bayt_jobs.job_title = bayt_jobs.job_title.apply(lambda x: Translator(x)[0]['translation_text'])
    
    
    
    ln_jobs.to_csv('lntest27072024.csv',index=False)
    
    bayt_jobs.to_csv('bayttest27072024.csv',index=False)
    
    total_skills_english.to_csv('total_skills_test27072024.csv',index=False)
    
    print('Done...')


    




if __name__ == '__main__':
    main()