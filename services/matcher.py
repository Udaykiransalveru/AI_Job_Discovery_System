from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def match_jobs(resume_text, jobs_df):

    descriptions = jobs_df["Description"].fillna("").tolist()

    corpus = [resume_text] + descriptions

    vectorizer = TfidfVectorizer(stop_words="english")

    vectors = vectorizer.fit_transform(corpus)

    resume_vector = vectors[0]
    job_vectors = vectors[1:]

    similarity = cosine_similarity(
        resume_vector,
        job_vectors
    ).flatten()

    jobs_df["Match_Score"] = similarity

    jobs_df = jobs_df.sort_values(
        by="Match_Score",
        ascending=False
    )

    return jobs_df.head(20)