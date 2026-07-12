import requests
from config import Config

TMDB_IMAGE_URL = "https://image.tmdb.org/t/p/w500"


# ==========================
# GET MOVIE DETAILS
# ==========================

def get_movie_details(movie_name):

    url = "https://api.themoviedb.org/3/search/movie"

    search_title = movie_name.split(" (")[0].strip()

    params = {
        "api_key": Config.TMDB_API_KEY,
        "query": search_title,
        "language": "en-US"
    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        if response.status_code != 200:
            return None

        data = response.json()

        if not data.get("results"):
            return None

        movie = None

        # Exact title match
        for result in data["results"]:

            if result.get("title", "").lower() == search_title.lower():

                movie = result
                break

        if movie is None:
            movie = data["results"][0]

        movie_id = movie.get("id")

        poster = ""

        if movie.get("poster_path"):

            poster = (
                TMDB_IMAGE_URL +
                movie["poster_path"]
            )

        trailer = get_movie_trailer(movie_id)

        cast = get_movie_cast(movie_id)

        director = get_movie_director(movie_id)

        similar_movies = get_similar_movies(movie_id)

        return {

            "id": movie_id,

            "title": movie.get("title", ""),

            "overview": movie.get("overview", ""),

            "rating": movie.get("vote_average", 0),

            "release_date": movie.get("release_date", ""),

            "poster": poster,

            "trailer": trailer,

            "cast": cast,

            "director": director,

            "similar_movies": similar_movies

        }

    except Exception as e:

        print("Movie Details Error:", e)

        return None


# ==========================
# GET MOVIE TRAILER
# ==========================

def get_movie_trailer(movie_id):

    url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos"

    params = {

        "api_key": Config.TMDB_API_KEY,

        "language": "en-US"

    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        if response.status_code != 200:
            return ""

        data = response.json()

        for video in data.get("results", []):

            if (
                video.get("site") == "YouTube"
                and video.get("type") == "Trailer"
            ):

                return (
                    "https://www.youtube.com/watch?v="
                    + video["key"]
                )

        return ""

    except Exception as e:

        print("Trailer Error:", e)

        return ""


# ==========================
# SEARCH AUTOCOMPLETE
# ==========================

def search_movies(query):

    url = "https://api.themoviedb.org/3/search/movie"

    params = {

        "api_key": Config.TMDB_API_KEY,

        "query": query,

        "language": "en-US"

    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        if response.status_code != 200:
            return []

        data = response.json()

        movies = []

        for movie in data.get("results", [])[:8]:

            poster = ""

            if movie.get("poster_path"):

                poster = (
                    TMDB_IMAGE_URL +
                    movie["poster_path"]
                )

            movies.append({

                "id": movie.get("id"),

                "title": movie.get("title", ""),

                "poster": poster,

                "rating": movie.get("vote_average", 0)

            })

        return movies

    except Exception as e:

        print("Search Error:", e)

        return []
    # ==========================
# GET SIMILAR MOVIES
# ==========================

def get_similar_movies(movie_id):

    url = (
        f"https://api.themoviedb.org/3/movie/"
        f"{movie_id}/similar"
    )

    params = {

        "api_key": Config.TMDB_API_KEY,

        "language": "en-US"

    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        if response.status_code != 200:

            return []

        data = response.json()

        movies = []

        for movie in data.get("results", [])[:6]:

            poster = ""

            if movie.get("poster_path"):

                poster = (
                    TMDB_IMAGE_URL +
                    movie["poster_path"]
                )

            movies.append({

                "id": movie.get("id"),

                "title": movie.get("title", ""),

                "poster": poster,

                "rating": movie.get("vote_average", 0)

            })

        return movies

    except Exception as e:

        print("Similar Movies Error:", e)

        return []


# ==========================
# GET MOVIE CAST
# ==========================

def get_movie_cast(movie_id):

    url = (
        f"https://api.themoviedb.org/3/movie/"
        f"{movie_id}/credits"
    )

    params = {

        "api_key": Config.TMDB_API_KEY,

        "language": "en-US"

    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        if response.status_code != 200:

            return []

        data = response.json()

        cast_list = []

        for actor in data.get("cast", [])[:5]:

            cast_list.append({

                "name": actor.get("name", ""),

                "character": actor.get("character", ""),

                "profile": (
                    TMDB_IMAGE_URL + actor["profile_path"]
                    if actor.get("profile_path")
                    else ""
                )

            })

        return cast_list

    except Exception as e:

        print("Cast Error:", e)

        return []


# ==========================
# GET MOVIE DIRECTOR
# ==========================

def get_movie_director(movie_id):

    url = (
        f"https://api.themoviedb.org/3/movie/"
        f"{movie_id}/credits"
    )

    params = {

        "api_key": Config.TMDB_API_KEY,

        "language": "en-US"

    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        if response.status_code != 200:

            return ""

        data = response.json()

        for person in data.get("crew", []):

            if person.get("job") == "Director":

                return person.get("name", "")

        return ""

    except Exception as e:

        print("Director Error:", e)

        return ""
    # ==========================
# GET TRENDING MOVIES
# ==========================

def get_trending_movies():

    url = (
        "https://api.themoviedb.org/3/"
        "trending/movie/week"
    )

    params = {

        "api_key": Config.TMDB_API_KEY,

        "language": "en-US"

    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        if response.status_code != 200:

            return []

        data = response.json()

        trending = []

        for movie in data.get("results", [])[:6]:

            poster = ""

            if movie.get("poster_path"):

                poster = (
                    TMDB_IMAGE_URL +
                    movie["poster_path"]
                )

            trending.append({

                "id": movie.get("id"),

                "title": movie.get("title", ""),

                "rating": movie.get("vote_average", 0),

                "poster": poster,

                "trailer": get_movie_trailer(movie.get("id"))

            })

        return trending

    except Exception as e:

        print("Trending Error:", e)

        return []


# ==========================
# GET MOVIES BY GENRE
# ==========================

def get_movies_by_genre(genre_id):

    url = "https://api.themoviedb.org/3/discover/movie"

    params = {

        "api_key": Config.TMDB_API_KEY,

        "with_genres": genre_id,

        "language": "en-US"

    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        if response.status_code != 200:

            return []

        data = response.json()

        movies = []

        for movie in data.get("results", [])[:6]:

            poster = ""

            if movie.get("poster_path"):

                poster = (
                    TMDB_IMAGE_URL +
                    movie["poster_path"]
                )

            movies.append({

                "id": movie.get("id"),

                "title": movie.get("title", ""),

                "rating": movie.get("vote_average", 0),

                "poster": poster

            })

        return movies

    except Exception as e:

        print("Genre Error:", e)

        return []


# ==========================
# GET TOP RATED MOVIES
# ==========================

def get_top_rated_movies():

    url = "https://api.themoviedb.org/3/movie/top_rated"

    params = {

        "api_key": Config.TMDB_API_KEY,

        "language": "en-US"

    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        if response.status_code != 200:

            return []

        data = response.json()

        movies = []

        for movie in data.get("results", [])[:10]:

            poster = ""

            if movie.get("poster_path"):

                poster = (
                    TMDB_IMAGE_URL +
                    movie["poster_path"]
                )

            movies.append({

                "id": movie.get("id"),

                "title": movie.get("title", ""),

                "poster": poster,

                "rating": movie.get("vote_average", 0),

                "trailer": get_movie_trailer(movie.get("id"))

            })

        return movies

    except Exception as e:

        print("Top Rated Error:", e)

        return []
    # ==========================
# GET UPCOMING MOVIES
# ==========================

def get_upcoming_movies():

    url = "https://api.themoviedb.org/3/movie/upcoming"

    params = {

        "api_key": Config.TMDB_API_KEY,

        "language": "en-US"

    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        if response.status_code != 200:

            return []

        data = response.json()

        movies = []

        for movie in data.get("results", [])[:10]:

            poster = ""

            if movie.get("poster_path"):

                poster = (
                    TMDB_IMAGE_URL +
                    movie["poster_path"]
                )

            movies.append({

                "id": movie.get("id"),

                "title": movie.get("title", ""),

                "poster": poster,

                "rating": movie.get("vote_average", 0),

                "trailer": get_movie_trailer(movie.get("id"))

            })

        return movies

    except Exception as e:

        print("Upcoming Error:", e)

        return []