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

from transformers import pipeline

import google.generativeai as genai

from main_package import *
import os
import pyodbc


def main():
    # Database connection
    con_string = os.environ('CONNECTION_STRING')

    conn = pyodbc.connect(con_string)

    conn.setdecoding(pyodbc.SQL_WCHAR, encoding="utf-8")
    conn.setencoding(encoding="utf-8")

    conn.autocommit = True

    # Scraping links
    ln_links = scrape_linkedin_links()
    print(ln_links.head(3))
    print(ln_links.shape)

    bayt_links = scrape_bayt_links()
    print(bayt_links.head(3))
    print(bayt_links.shape)

    # Scraping jobs
    print("Starting jobs scraping in 5 sec, please turn on proxy switcher")
    time.sleep(5)

    print("Scraping jobs from linkedin:")
    ln_jobs = scrape_linkedin_jobs_description(ln_links)
    print(ln_jobs.head(3))
    print(ln_jobs.shape)

    print("Scraping jobs from bayt:")
    bayt_jobs = scrape_bayt_jobs_description(bayt_links)
    print(bayt_jobs.head(3))
    print(bayt_jobs.shape)

    total_jobs = pd.concat([ln_jobs, bayt_jobs], axis=0)

    total_jobs.to_csv("total_jobs.csv", index=False)

    # Extracting skills
    print("Extracting skills form linkedin and bayt jobs")
    total_skills = get_skills(total_jobs)
    print(total_skills.head(3))
    total_skills.to_csv("total_skills_test.csv", index=False)

    print("Transforming job titles...")
    total_jobs.job_title = total_jobs.job_title.apply(lambda x: job_titles(x))

    total_jobs.to_csv("total_jobs.csv", index=False)

    # Inserting to DB
    print("Inserting data to DB:")

    insert_data_from_linkedin(conn, "linkedin_jobs", total_jobs)

    # insert_data_from_bayt(conn,'bayt_jobs',bayt_jobs)

    insert_skills(conn, "skills", total_skills)


if __name__ == "__main__":
    main()
