import pandas as pd
import pickle
import ast
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

print("Loading TMDB dataset...")

# Load datasets
movies = pd.read_csv("dataset/tmdb_5000_movies.csv")
credits = pd.read_csv("dataset/tmdb_5000_credits.csv")

# Merge datasets
movies = movies.merge(credits, on="title")

# Keep only required columns
movies = movies[
    [
        "title",
        "overview",
        "genres",
        "keywords",
        "cast",
        "crew"
    ]
]

# Fill missing values
movies.fillna("", inplace=True)


# Convert genres and keywords
def convert(text):
    result = []

    try:
        data = ast.literal_eval(text)

        for item in data:
            result.append(item["name"])

    except:
        pass

    return " ".join(result)


# Get first 3 cast members
def fetch_cast(text):
    result = []

    try:
        data = ast.literal_eval(text)

        for item in data[:3]:
            result.append(item["name"])

    except:
        pass

    return " ".join(result)


# Get director name
def fetch_director(text):

    result = ""

    try:
        data = ast.literal_eval(text)

        for item in data:

            if item["job"] == "Director":
                result = item["name"]
                break

    except:
        pass

    return result

# Apply functions
movies["genres"] = movies["genres"].apply(convert)
movies["keywords"] = movies["keywords"].apply(convert)
movies["cast"] = movies["cast"].apply(fetch_cast)
movies["director"] = movies["crew"].apply(fetch_director)
movies["crew"] = movies["crew"].apply(fetch_director)


# Create content
movies["content"] = (
    movies["overview"].astype(str) + " " +
    movies["genres"].astype(str) + " " +
    movies["keywords"].astype(str) + " " +
    movies["cast"].astype(str) + " " +
    movies["director"].astype(str)
)

print("Creating TF-IDF vectors...")

tfidf = TfidfVectorizer(
    stop_words="english",
    max_features=8000,
    ngram_range=(1,2)
)

vectors = tfidf.fit_transform(movies["content"])

print("Calculating similarity...")

similarity = cosine_similarity(vectors)

# Save model
pickle.dump(movies, open("model/movies.pkl", "wb"))
pickle.dump(similarity, open("model/similarity.pkl", "wb"))

print("✅ Model Trained Successfully")