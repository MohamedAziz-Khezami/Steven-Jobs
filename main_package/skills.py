

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







#Extracting skills from all job descriptions
def get_skills(df: pd.DataFrame) -> pd.DataFrame:
    
    
    #Getting job skills from linkedin jobs using gemini
    def skills_extraction(job_desc):
        prompt_empy = '{"key_words":[]}'

        prompt = '''
        Read the following job description and return key words of all the skills required for this job.
        I need all the skills required for this job.
        
        
        
        if the job description is empty don't return anything
        
        if the job description contain a list of job descriptions return all the skills required for all the jobs even if they are in different jobs
        
        if the job descriptions doesn't have any content don't return anything

        No explanations, uniques keywords only for skills, no duplicates, Be breif.
        '''
        
        genai.configure(api_key="AIzaSyAX5hRxjQ64IqZxqNcdj7ONpALMWxnIHb0")

        model = genai.GenerativeModel('gemini-1.5-flash')
        
        if job_desc == "":
            prompt_id = prompt_empy
        else:
            prompt_id = prompt + job_desc
        output = model.generate_content(prompt_id)

        
        return output.candidates[0].content.parts[0].text.strip().replace("-","").split('\n')



    
    
    
    
    description = df.job_description
    
    batch_size = len(description) // 2
    
    batches = np.array_split(description, batch_size)

    # Access individual batches
    batchs = [batches[0], batches[1], batches[2] ]
    
    
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
