import pickle

from sklearn.metrics.pairwise import linear_kernel


movies = pickle.load(
    open("model/movies.pkl","rb")
)

tfidf, vectors = pickle.load(
    open("model/tfidf.pkl","rb")
)


def recommend(movie_name):

    movie_name = movie_name.lower().strip()

    match = movies[
        movies["title"].str.lower() == movie_name
    ]

    if match.empty:

        match = movies[
            movies["title"]
            .str.lower()
            .str.contains(movie_name)
        ]

        if match.empty:
            return []

    index = match.index[0]

    similarity = linear_kernel(
    vectors[index],
    vectors
    ).flatten()

    movies_list = sorted(
        enumerate(similarity),
        reverse=True,
        key=lambda x: x[1]
    )[1:11]


    result = []

    for i in movies_list:
        result.append(
            movies.iloc[i[0]]["title"]
        )

    return result