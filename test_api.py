from services.job_api import fetch_jobs

df = fetch_jobs("Python Developer")

print(df.head())