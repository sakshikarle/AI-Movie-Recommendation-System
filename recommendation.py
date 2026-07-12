import pickle

movies = pickle.load(open("model/movies.pkl", "rb"))
similarity = pickle.load(open("model/similarity.pkl", "rb"))


def recommend(movie_name):

    movie_name = movie_name.lower().strip()

    # Exact match first
    exact_match = movies[
        movies["title"].str.lower() == movie_name
    ]

    if not exact_match.empty:
        index = exact_match.index[0]

    else:
        # Partial match
        matches = movies[
            movies["title"].str.lower().str.contains(movie_name, regex=False)
        ]

        if matches.empty:
            return None

        index = matches.index[0]


    distances = list(enumerate(similarity[index]))

    distances = sorted(
        distances,
        key=lambda x: x[1],
        reverse=True
    )

    recommended_movies = []

    for i in distances[1:]:

        title = movies.iloc[i[0]].title

        # 👇 हे print add कर
        print("Recommended Title:", title)

        match_percentage = round(i[1] * 100, 2)

        if title not in [movie["title"] for movie in recommended_movies]:

            recommended_movies.append({
                "title": title,
                "similarity": match_percentage
            })

        if len(recommended_movies) == 10:
            break

    # 👇 हे पण add कर
    print("Final Recommendations:", recommended_movies)

    return recommended_movies