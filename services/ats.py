from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def calculate_ats_score(
    resume_text,
    job_description
):

    corpus = [resume_text, job_description]

    vectorizer = TfidfVectorizer(
        stop_words='english'
    )

    vectors = vectorizer.fit_transform(corpus)

    similarity = cosine_similarity(
        vectors[0:1],
        vectors[1:2]
    )[0][0]

    return round(similarity * 100, 2)