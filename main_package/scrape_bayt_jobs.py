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
def scrape_bayt_jobs_description(df: pd.DataFrame) -> pd.DataFrame:
    # Changing date format
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

    storage = pd.DataFrame(
        columns=["post_date", "job_title", "job_description", "company", "location"]
    )

    for u in tqdm.tqdm(df.links, desc="Scraping jobs"):
        headers = {"User-Agent": user.random}

        url = u

        try:
            request = requests.get(url, timeout=3600, headers=headers)

        except Exception as e:
            print(e)
            continue

        if request.status_code != 200:
            continue

        soup = BeautifulSoup(request.text, "html.parser")
        time.sleep(2)

        post_date = soup.find("div", {"class": "t-small t-mute m10b"})

        job_title = soup.find("h1", {"class": "h3 t-break"})

        job_description = soup.find("div", {"class": "t-break"})

        company = soup.find("a", {"class": "is-black t-bold"})

        location = soup.find("span", {"class": "t-mute"})

        criteria = soup.find_all("dl", {"class": "dlist is-spaced is-fitted t-small"})

        a = pd.DataFrame(
            {
                "post_date": (
                    convert_relative_date(post_date.text.strip().split("\n")[0])
                    if post_date
                    else "2024-01"
                ),
                "job_title": job_title.text.strip() if job_title else "None",
                "job_description": (
                    job_description.text.strip() if job_description else "None"
                ),
                "company": company.text.strip() if company else "None",
                "location": location.text.strip() if location else "None",
                "industry": (
                    criteria[0].text.strip().split("\n")[5] if criteria else "None"
                ),
            },
            index=[0],
        )

        storage = pd.concat([storage, a], axis=0)
    try:
        storage.post_date = pd.to_datetime(storage.post_date, format="%Y-%m")
    except:
        pass

    return storage
