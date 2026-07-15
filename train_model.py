import pandas as pd
import pickle
import ast

from sklearn.feature_extraction.text import TfidfVectorizer

print("Loading dataset...")

movies = pd.read_csv("dataset/tmdb_5000_movies.csv")
credits = pd.read_csv("dataset/tmdb_5000_credits.csv")

movies = movies.merge(credits, on="title")

movies = movies[[
    "movie_id",
    "title",
    "overview",
    "genres",
    "keywords",
    "cast",
    "crew"
]]

def convert(obj):
    L = []
    for i in ast.literal_eval(obj):
        L.append(i["name"])
    return L

def convert_cast(obj):
    L = []
    counter = 0
    for i in ast.literal_eval(obj):
        if counter != 3:
            L.append(i["name"])
            counter += 1
        else:
            break
    return L

def fetch_director(obj):
    L = []
    for i in ast.literal_eval(obj):
        if i["job"] == "Director":
            L.append(i["name"])
    return L

movies.dropna(inplace=True)

movies["genres"] = movies["genres"].apply(convert)
movies["keywords"] = movies["keywords"].apply(convert)
movies["cast"] = movies["cast"].apply(convert_cast)
movies["crew"] = movies["crew"].apply(fetch_director)

movies["overview"] = movies["overview"].apply(lambda x: x.split())

for col in ["genres","keywords","cast","crew"]:
    movies[col] = movies[col].apply(
        lambda x:[i.replace(" ","") for i in x]
    )

movies["tags"] = (
    movies["overview"]
    + movies["genres"]
    + movies["keywords"]
    + movies["cast"]
    + movies["crew"]
)

new_df = movies[["movie_id","title","tags"]]

new_df["tags"] = new_df["tags"].apply(lambda x:" ".join(x).lower())
print("Creating TF-IDF...")

tfidf = TfidfVectorizer(stop_words="english")

vectors = tfidf.fit_transform(new_df["tags"])

print("Saving files...")

with open("model/movies.pkl", "wb") as f:
    pickle.dump(new_df, f)

with open("model/tfidf.pkl", "wb") as f:
    pickle.dump((tfidf, vectors), f)

print("Movies file size saved")
print("TF-IDF file saved")
print("Done!")