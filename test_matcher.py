from services.job_api import fetch_jobs
from services.matcher import match_jobs

resume_text = "Python Django SQL Machine Learning"

jobs = fetch_jobs("Python Developer")

matched = match_jobs(
    resume_text,
    jobs
)

print(
    matched[
        ["Title", "Match_Score"]
    ]
)