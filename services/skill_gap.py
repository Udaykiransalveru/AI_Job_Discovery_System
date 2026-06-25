import re

COMMON_SKILLS = [

    "python",
    "sql",
    "django",
    "aws",
    "docker",
    "fastapi",
    "react",
    "machine learning",
    "tensorflow",
    "mongodb"
]


def extract_required_skills(
    job_description
):

    job_description = job_description.lower()

    required = []

    for skill in COMMON_SKILLS:

        pattern = r"\\b" + re.escape(skill) + r"\\b"

        if re.search(pattern, job_description):

            required.append(skill)

    return required


def find_missing_skills(
    resume_skills,
    required_skills
):

    return list(
        set(required_skills)
        - set(resume_skills)
    )