from nltk.corpus import stopwords
import pandas as pd
import re
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nltk.download("stopwords")
nltk.download("punkt")


def clean_text(text):
    if not isinstance(text, str):
        return ""

    text = text.lower()
    text = re.sub(r"[^a-z\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()

    stop_words = set(stopwords.words("english"))
    words = text.split()
    words = [word for word in words if word not in stop_words and len(word) > 2]

    return " ".join(words)


def build_recommendation_model(csv_path="movies_final.csv"):

    print("Data Loading...")
    df = pd.read_csv(csv_path)

    df = df.dropna(subset=["storyline"])
    df = df[df["storyline"].str.len() > 50]
    df = df.reset_index(drop=True)

    print(f"{len(df)} Movies Loaded!")

    print("Text Preprocessing...")
    df["cleaned_storyline"] = df["storyline"].apply(clean_text)

    print("TF-IDF Vectorization...")

    vectorizer = TfidfVectorizer(
        max_features=5000, ngram_range=(1, 2), min_df=2, max_df=0.95
    )

    tfidf_matrix = vectorizer.fit_transform(df["cleaned_storyline"])

    print(f"Matrix Shape: {tfidf_matrix.shape}")

    print("Cosine Similarity Calculating...")
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    print("Model Ready!")
    return df, vectorizer, tfidf_matrix, cosine_sim


def recommend_by_title(movie_name, df, cosine_sim, top_n=5):

    movie_name_lower = movie_name.lower()
    matches = df[df["movie_name"].str.lower().str.contains(movie_name_lower)]

    if matches.empty:
        return None, f"'{movie_name}' Database- not there"

    idx = matches.index[0]

    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1 : top_n + 1]

    results = []
    for movie_idx, score in sim_scores:
        results.append(
            {
                "rank": len(results) + 1,
                "movie_name": df.iloc[movie_idx]["movie_name"],
                "similarity_score": round(score * 100, 2),
                "storyline": df.iloc[movie_idx]["storyline"][:200] + "...",
            }
        )

    return results, None


def recommend_by_storyline(user_story, df, vectorizer, tfidf_matrix, top_n=5):
    cleaned = clean_text(user_story)

    if not cleaned:
        return None, "Storyline not detiled try again"

    user_vector = vectorizer.transform([cleaned])
    sim_scores = cosine_similarity(user_vector, tfidf_matrix).flatten()

    top_indices = sim_scores.argsort()[-top_n:][::-1]

    results = []
    for rank, idx in enumerate(top_indices, 1):
        results.append(
            {
                "rank": rank,
                "movie_name": df.iloc[idx]["movie_name"],
                "similarity_score": round(sim_scores[idx] * 100, 2),
                "storyline": df.iloc[idx]["storyline"][:200] + "...",
            }
        )

    return results, None


if __name__ == "__main__":
    df, vectorizer, tfidf_matrix, cosine_sim = build_recommendation_model(
        "movies_final.csv"
    )

    print("\n" + "=" * 50)
    print("TEST 1: Movie Name Recommend")
    print("=" * 50)

    sample_movie = df.iloc[0]["movie_name"]
    print(f"\nTest Movie: '{sample_movie}'")

    results, error = recommend_by_title(sample_movie, df, cosine_sim, top_n=5)

    if error:
        print(f" {error}")
    else:
        for r in results:
            print(f"{r['rank']}.{r['movie_name']}-" f"{r['similarity_score']}% Match")

    print("\n" + "=" * 50)
    print("TEST 2: Custom Storyline Recommend")
    print("=" * 50)

    test_story = (
        "A young detective investigates " "a mysterious murder case in a big city"
    )
    print(f"\nTest Storyline: '{test_story}'")

    results, error = recommend_by_storyline(
        test_story, df, vectorizer, tfidf_matrix, top_n=5
    )

    if error:
        print(f"{error}")
    else:
        for r in results:
            print(f"{r['rank']}.{r['movie_name']}-" f"{r['similarity_score']}% Match")
