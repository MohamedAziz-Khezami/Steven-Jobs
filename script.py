
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

from main_package import *

import pyodbc



def main():
    #Database connection
    con_string = "Driver={ODBC Driver 18 for SQL Server};Server=tcp:prepa-insights.database.windows.net,1433;Database=stevenjobs;Uid=aziz_admin;Pwd=Insightsprepa12;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=7000;"

    conn = pyodbc.connect(con_string)

    conn.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-8')
    conn.setencoding(encoding='utf-8')

    conn.autocommit = True
    
    
    
    

    #Scraping links
    ln_links = scrape_linkedin_links()
    print(ln_links.head(3))
    print(ln_links.shape)

    bayt_links = scrape_bayt_links()
    print(bayt_links.head(3))
    print(bayt_links.shape)
    
    
    #Scraping jobs
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
    
    
    #Extracting skills
    print('Extracting skills form linkedin and bayt jobs')
    ln_skills = get_skills(ln_jobs)
    
    print('waiting for 1 min')
    time.sleep(65)
    
    bayt_skills = get_skills(bayt_jobs)
  
    total_skills = pd.concat([ln_skills, bayt_skills])
    
    print(total_skills.head(3))



    #Translating
    print('Translating skills...')
    Translator = pipeline("translation", model="Helsinki-NLP/opus-mt-mul-en", max_length=500000000)
    
    print('Translating skills...')
    
    total_skills_english = total_skills.skills.apply(lambda x: Translator(x, max_length=500000000)[0]['translation_text'])
    
    total_skills_english = pd.DataFrame(total_skills_english, columns=['skills'])
    
    print(total_skills_english)
    
    print('Translating job titles...')
    
    ln_jobs.job_title = ln_jobs.job_title.apply(lambda x: Translator(x, max_length=500000000)[0]['translation_text'])
    
    bayt_jobs.job_title = bayt_jobs.job_title.apply(lambda x: Translator(x, max_length=500000000)[0]['translation_text'])
    
    
    #local saving
    ln_jobs.to_csv('lntest27072024.csv',index=False)
    
    bayt_jobs.to_csv('bayttest27072024.csv',index=False)
    
    total_skills_english.to_csv('total_skills_test27072024.csv',index=False)
    
    
    #Inserting to DB
    print('Inserting data to DB:')
    
    insert_data_from_linkedin(conn, 'linkedin_jobs' ,ln_jobs)
    
    insert_data_from_bayt(conn,'bayt_jobs',bayt_jobs)
    
    insert_skills(conn, 'skills', total_skills_english)




if __name__ == '__main__':
    main()