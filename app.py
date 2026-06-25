import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt

from services.parser import (
    extract_text_from_pdf,
    extract_skills,
    extract_email,
    extract_phone,
    is_valid_resume
)

from services.job_api import fetch_jobs

from services.matcher import match_jobs

from services.skill_gap import (
    extract_required_skills,
    find_missing_skills
)

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="AI Career Discovery Platform",
    layout="wide"
)

# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------

st.markdown(
    """
    <style>

    .main {
        background-color: #f5f7fa;
    }

    .title {
        font-size: 50px;
        font-weight: bold;
        color: #111827;
        text-align: center;
        margin-bottom: 10px;
    }

    .subtitle {
        text-align: center;
        color: gray;
        margin-bottom: 30px;
        font-size: 18px;
    }

    .skill-box {
        background-color: #2563eb;
        color: white;
        padding: 8px 14px;
        border-radius: 20px;
        display: inline-block;
        margin: 5px;
        font-size: 14px;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------
# HEADER
# ---------------------------------------------------

st.markdown(
    """
    <div class='title'>
        🚀 AI-Powered Career Discovery Platform
    </div>

    <div class='subtitle'>
        Semantic AI Job Matching + Salary Intelligence
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

st.sidebar.title("🔍 Search Filters")

username = st.sidebar.text_input(
    "Enter Your Name"
)

city = st.sidebar.text_input(
    "Preferred Location",
    "Hyderabad"
)

experience_level = st.sidebar.selectbox(

    "Experience Level",

    [
        "Fresher",
        "Experienced",
        "Both"
    ]
)

career_interests = st.sidebar.multiselect(

    "Career Interests",

    [

        "frontend developer",

        "backend developer",

        "full stack developer",

        "software engineer",

        "data analyst",

        "machine learning engineer",

        "cloud engineer",

        "digital marketing",

        "sales executive",

        "hr recruiter"
    ]
)

uploaded_file = st.sidebar.file_uploader(
    "Upload Resume",
    type=["pdf"]
)

# ---------------------------------------------------
# FIND JOBS BUTTON
# ---------------------------------------------------

if st.sidebar.button("Find Jobs"):

    if uploaded_file is not None:

        # ---------------------------------------------------
        # CREATE UPLOADS FOLDER
        # ---------------------------------------------------

        os.makedirs(
            "uploads",
            exist_ok=True
        )

        # ---------------------------------------------------
        # SAVE RESUME
        # ---------------------------------------------------

        path = os.path.join(
            "uploads",
            uploaded_file.name
        )

        with open(path, "wb") as f:

            f.write(
                uploaded_file.read()
            )

        # ---------------------------------------------------
        # EXTRACT RESUME TEXT
        # ---------------------------------------------------

        text = extract_text_from_pdf(path)

        # ---------------------------------------------------
        # VALIDATE RESUME
        # ---------------------------------------------------

        if not is_valid_resume(text):

            st.error(
                "❌ Uploaded file is not a valid resume."
            )

            st.stop()

        # ---------------------------------------------------
        # EXTRACT DETAILS
        # ---------------------------------------------------

        skills = extract_skills(text)

        email = extract_email(text)

        phone = extract_phone(text)

        # ---------------------------------------------------
        # SHOW USER DETAILS
        # ---------------------------------------------------

        st.subheader(
            "👤 Resume Information"
        )

        col1, col2 = st.columns(2)

        with col1:

            if email:

                st.write(
                    f"📧 Email: {email}"
                )

            else:

                st.warning(
                    "Email not detected."
                )

        with col2:

            if phone:

                st.write(
                    f"📱 Phone: {phone}"
                )

            else:

                st.warning(
                    "Phone number not detected."
                )

        # ---------------------------------------------------
        # SHOW SKILLS
        # ---------------------------------------------------

        st.subheader(
            "🧠 Extracted Skills"
        )

        if len(skills) > 0:

            skill_html = ""

            for skill in skills:

                skill_html += f"""
                <span class='skill-box'>
                    {skill}
                </span>
                """

            st.markdown(
                skill_html,
                unsafe_allow_html=True
            )

        else:

            st.warning(
                "No skills detected."
            )

        # ---------------------------------------------------
        # LOW SKILL WARNING
        # ---------------------------------------------------

        if len(skills) < 2:

            st.warning(
                "⚠️ Very few skills detected."
            )

        # ---------------------------------------------------
        # RESUME SUMMARY
        # ---------------------------------------------------

        st.subheader(
            "📄 Resume Summary"
        )

        st.write(
            text[:1000]
        )

        # ---------------------------------------------------
        # WORD COUNT
        # ---------------------------------------------------

        word_count = len(text.split())

        st.write(
            f"📝 Resume Word Count: {word_count}"
        )

        # ---------------------------------------------------
        # DEFAULT CAREER INTERESTS
        # ---------------------------------------------------

        if len(career_interests) == 0:

            if experience_level == "Fresher":

                career_interests = [

                    "fresher python developer",

                    "junior software engineer",

                    "graduate trainee",

                    "associate developer",

                    "software engineer intern",

                    "frontend intern",

                    "backend intern",

                    "data analyst fresher",

                    "machine learning intern",

                    "digital marketing intern"
                ]

            else:

                career_interests = [

                    "software engineer",

                    "frontend developer",

                    "backend developer",

                    "full stack developer",

                    "data analyst",

                    "machine learning engineer",

                    "cloud engineer",

                    "digital marketing",

                    "sales executive",

                    "hr recruiter"
                ]

        # ---------------------------------------------------
        # FETCH LIVE JOBS
        # ---------------------------------------------------

        all_jobs = pd.DataFrame()

        with st.spinner(
            "Fetching Live Jobs..."
        ):

            for query in career_interests:

                temp_jobs = fetch_jobs(

                    query=query,

                    location=city
                )

                all_jobs = pd.concat(

                    [all_jobs, temp_jobs],

                    ignore_index=True
                )

        # ---------------------------------------------------
        # REMOVE DUPLICATES
        # ---------------------------------------------------

        jobs = all_jobs.drop_duplicates(

            subset=[
                "Title",
                "Company",
                "Redirect_URL"
            ]
        )

        jobs = jobs[
            jobs["Redirect_URL"].notna()
        ]

        jobs = jobs[
            jobs["Company"].notna()
        ]

        # ---------------------------------------------------
        # EXPERIENCE FILTER
        # ---------------------------------------------------

        if experience_level == "Fresher":

            fresher_keywords = [

                "fresher",

                "junior",

                "intern",

                "trainee",

                "associate",

                "0-1",

                "0 to 1"
            ]

            jobs = jobs[

                jobs["Description"]

                .fillna("")

                .str.lower()

                .apply(

                    lambda x: any(
                        keyword in x
                        for keyword in fresher_keywords
                    )
                )
            ]

        elif experience_level == "Experienced":

            experienced_keywords = [

                "senior",

                "manager",

                "lead",

                "3+ years",

                "5+ years"
            ]

            jobs = jobs[

                jobs["Description"]

                .fillna("")

                .str.lower()

                .apply(

                    lambda x: any(
                        keyword in x
                        for keyword in experienced_keywords
                    )
                )
            ]

        # ---------------------------------------------------
        # CHECK JOBS
        # ---------------------------------------------------

        if jobs.empty:

            st.error(
                "No jobs found."
            )

        else:

            # ---------------------------------------------------
            # SEMANTIC MATCHING
            # ---------------------------------------------------

            matched_jobs = match_jobs(
                text,
                jobs
            )

            # ---------------------------------------------------
            # MARKET INSIGHTS
            # ---------------------------------------------------

            st.subheader(
                "📊 Market Insights"
            )

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Jobs Found",
                len(matched_jobs)
            )

            avg_salary = int(

                matched_jobs[
                    "Salary"
                ].fillna(0).mean()
            )

            col2.metric(
                "Average Salary",
                f"₹ {avg_salary:,}"
            )

            top_score = round(

                matched_jobs[
                    "Match_Score"
                ].max() * 100,
                2
            )

            col3.metric(
                "Top Match Score",
                f"{top_score}%"
            )

            # ---------------------------------------------------
            # TABS
            # ---------------------------------------------------

            tab1, tab2, tab3 = st.tabs([

                "🎯 Recommended Jobs",

                "🌎 Explore Careers",

                "📈 Salary Analysis"
            ])

            # ---------------------------------------------------
            # RECOMMENDED JOBS
            # ---------------------------------------------------

            with tab1:

                for _, row in matched_jobs.iterrows():

                    st.markdown("---")

                    st.subheader(
                        row["Title"]
                    )

                    st.write(
                        f"🏢 Company: {row['Company']}"
                    )

                    st.write(
                        f"📍 Location: {row['Location']}"
                    )

                    salary = row["Salary"]

                    if pd.isna(salary):

                        salary = 0

                    st.write(
                        f"💰 Salary: ₹ {int(salary):,}"
                    )

                    match_score = round(
                        row["Match_Score"] * 100,
                        2
                    )

                    st.write(
                        f"🎯 Match Score: {match_score}%"
                    )

                    # ---------------------------------------------------
                    # SKILL GAP ANALYSIS
                    # ---------------------------------------------------

                    required_skills = extract_required_skills(
                        row["Description"]
                    )

                    missing = find_missing_skills(
                        skills,
                        required_skills
                    )

                    if missing:

                        st.warning(
                            f"Missing Skills: {', '.join(missing)}"
                        )

                    # ---------------------------------------------------
                    # APPLY BUTTON
                    # ---------------------------------------------------

                    if row["Redirect_URL"]:

                        st.link_button(
                            "Apply Now",
                            row["Redirect_URL"]
                        )

            # ---------------------------------------------------
            # EXPLORE CAREERS
            # ---------------------------------------------------

            with tab2:

                explore_jobs = jobs.sample(

                    min(10, len(jobs))
                )

                for _, row in explore_jobs.iterrows():

                    st.markdown("---")

                    st.write(
                        f"💼 {row['Title']}"
                    )

                    st.write(
                        f"🏢 {row['Company']}"
                    )

                    st.write(
                        f"📍 {row['Location']}"
                    )

                    st.write(
                        f"📂 {row['Category']}"
                    )

                    if row["Redirect_URL"]:

                        st.link_button(
                            "Explore Job",
                            row["Redirect_URL"]
                        )

            # ---------------------------------------------------
            # SALARY ANALYSIS
            # ---------------------------------------------------

            with tab3:

                salary_df = matched_jobs.dropna(
                    subset=["Salary"]
                )

                salary_df = salary_df.head(10)

                if not salary_df.empty:

                    fig, ax = plt.subplots(
                        figsize=(10, 5)
                    )

                    ax.bar(

                        salary_df["Title"],

                        salary_df["Salary"]
                    )

                    plt.xticks(rotation=45)

                    plt.title(
                        "Top Salary Jobs"
                    )

                    st.pyplot(fig)

                else:

                    st.warning(
                        "Salary data unavailable."
                    )

    else:

        st.error(
            "Please upload a resume PDF."
        )