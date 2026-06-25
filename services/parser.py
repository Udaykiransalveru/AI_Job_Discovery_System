import fitz
import re

# ---------------------------------------------------
# SKILLS DATABASE
# ---------------------------------------------------

COMMON_SKILLS = [

    # Programming

    "python",
    "java",
    "c++",
    "javascript",

    # Databases

    "sql",
    "mongodb",
    "postgresql",

    # Backend

    "django",
    "flask",
    "fastapi",
    "spring boot",

    # Frontend

    "react",
    "angular",
    "vue",
    "html",
    "css",

    # Cloud / DevOps

    "aws",
    "docker",
    "kubernetes",

    # AI / ML

    "machine learning",
    "deep learning",
    "tensorflow",
    "pytorch",

    # Other Domains

    "digital marketing",
    "seo",
    "sales",
    "hr"
]

# ---------------------------------------------------
# EXTRACT TEXT FROM PDF
# ---------------------------------------------------


def extract_text_from_pdf(pdf_path):

    text = ""

    try:

        doc = fitz.open(pdf_path)

        for page in doc:

            text += page.get_text()

    except Exception as e:

        print(
            f"PDF Extraction Error: {e}"
        )

    return text


# ---------------------------------------------------
# EXTRACT SKILLS
# ---------------------------------------------------


def extract_skills(text):

    text = text.lower()

    found_skills = []

    for skill in COMMON_SKILLS:

        pattern = r"\\b" + re.escape(skill) + r"\\b"

        if re.search(pattern, text):

            found_skills.append(skill)

    return list(set(found_skills))


# ---------------------------------------------------
# EMAIL DETECTION
# ---------------------------------------------------


def extract_email(text):

    pattern = r'\\S+@\\S+'

    match = re.search(pattern, text)

    if match:

        return match.group()

    return None


# ---------------------------------------------------
# PHONE DETECTION
# ---------------------------------------------------


def extract_phone(text):

    pattern = r'\\b\\d{10}\\b'

    match = re.search(pattern, text)

    if match:

        return match.group()

    return None


# ---------------------------------------------------
# VALIDATE RESUME
# ---------------------------------------------------


def is_valid_resume(text):

    text = text.lower()

    # ----------------------------------------
    # CHECK MINIMUM LENGTH
    # ----------------------------------------

    if len(text.strip()) < 100:

        return False

    # ----------------------------------------
    # RESUME KEYWORDS
    # ----------------------------------------

    resume_keywords = [

        "education",

        "skills",

        "projects",

        "experience",

        "internship",

        "certifications",

        "developer",

        "engineer",

        "student",

        "objective",

        "resume",

        "profile"
    ]

    keyword_count = 0

    for keyword in resume_keywords:

        if keyword in text:

            keyword_count += 1

    # ----------------------------------------
    # CHECK EMAIL
    # ----------------------------------------

    email_found = extract_email(text)

    # ----------------------------------------
    # CHECK PHONE
    # ----------------------------------------

    phone_found = extract_phone(text)

    # ----------------------------------------
    # FINAL VALIDATION
    # ----------------------------------------

    if (

        keyword_count >= 3

        and email_found is not None

        and phone_found is not None
    ):

        return True

    return False