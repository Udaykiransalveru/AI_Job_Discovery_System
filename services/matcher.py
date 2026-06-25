from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer(
    'all-MiniLM-L6-v2'
)


def match_jobs(
    resume_text,
    jobs_df
):

    descriptions = jobs_df[
        "Description"
    ].fillna("").tolist()

    resume_embedding = model.encode(
        [resume_text]
    )

    job_embeddings = model.encode(
        descriptions
    )

    similarity = cosine_similarity(
        resume_embedding,
        job_embeddings
    ).flatten()

    jobs_df["Match_Score"] = similarity

    jobs_df = jobs_df.sort_values(
        by="Match_Score",
        ascending=False
    )

    return jobs_df.head(20)