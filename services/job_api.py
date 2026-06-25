import requests
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

APP_ID = os.getenv("APP_ID")
APP_KEY = os.getenv("APP_KEY")
COUNTRY = os.getenv("COUNTRY", "in")


def fetch_jobs(query, location="India", pages=1):

    all_jobs = []

    for page in range(1, pages + 1):

        url = f"https://api.adzuna.com/v1/api/jobs/{COUNTRY}/search/{page}"

        params = {
            "app_id": APP_ID,
            "app_key": APP_KEY,
            "results_per_page": 20,
            "what": query,
            "where": location,
            "content-type": "application/json"
        }

        response = requests.get(
            url,
            params=params
        )

        data = response.json()

        for job in data.get("results", []):

            all_jobs.append({

                "Title": job.get("title"),

                "Company": job.get(
                    "company",
                    {}
                ).get("display_name"),

                "Location": job.get(
                    "location",
                    {}
                ).get("display_name"),

                "Description": job.get(
                    "description"
                ),

                "Salary": job.get(
                    "salary_min"
                ),

                "Redirect_URL": job.get(
                    "redirect_url"
                ),

                "Category": query
            })

    return pd.DataFrame(all_jobs)