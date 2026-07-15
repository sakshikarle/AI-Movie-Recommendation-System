from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import requests
from bson.objectid import ObjectId

from config import Config
from auth import register_user, login_user
from recommendation import recommend
from database.mongodb import users, favorites, history

from tmdb import (
    get_movie_details,
    get_trending_movies,
    get_movies_by_genre,
    get_top_rated_movies,
    get_upcoming_movies,
    search_movies
)


app = Flask(__name__)

app.secret_key = Config.SECRET_KEY



# ==========================
# HOME PAGE
# ==========================

@app.route("/")
def home():

    if "username" not in session:
        return redirect(url_for("login"))


    trending_movies = get_trending_movies()


    return render_template(
        "index.html",
        username=session["username"],
        trending_movies=trending_movies
    )



# ==========================
# SEARCH AUTOCOMPLETE
# ==========================

@app.route("/autocomplete")
def autocomplete():

    if "username" not in session:
        return jsonify([])


    query = request.args.get("q","")


    if not query:
        return jsonify([])


    movies = search_movies(query)


    return jsonify(movies)
# ==========================
# LOGIN
# ==========================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]

        password = request.form["password"]


        user = login_user(
            username,
            password
        )


        if user:

            session["username"] = user["username"]

            flash(
                "Login Successful!",
                "success"
            )


            return redirect(
                url_for("home")
            )


        flash(
            "Invalid Username or Password",
            "danger"
        )


    return render_template(
        "login.html"
    )





# ==========================
# REGISTER
# ==========================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":


        username = request.form["username"]

        email = request.form["email"]

        password = request.form["password"]



        success = register_user(
            username,
            email,
            password
        )



        if success:


            flash(
                "Registration Successful",
                "success"
            )


            return redirect(
                url_for("login")
            )



        flash(
            "Username or Email already exists",
            "danger"
        )


    return render_template(
        "register.html"
    )





# ==========================
# MOVIE RECOMMENDATION
# ==========================

@app.route("/recommend", methods=["POST"])
def recommendation():


    if "username" not in session:

        return redirect(
            url_for("login")
        )



    movie_name = request.form["movie"]



    recommended_movies = recommend(
        movie_name
    )



    print(
        "RECOMMENDED:",
        recommended_movies
    )



    if not recommended_movies:


        flash(
            "Movie not found!",
            "warning"
        )


        return render_template(
            "index.html",
            username=session["username"],
            trending_movies=get_trending_movies()
        )



    history.insert_one({

        "username": session["username"],

        "searched_movie": movie_name

    })



    movie_details = []


    for movie in recommended_movies:

        details = get_movie_details(movie)

        if details:

            movie_details.append(details)



    return render_template(

        "recommendation.html",

        username=session["username"],

        recommendations=recommended_movies,

        movie_details=movie_details,

        searched_movie=movie_name

    )

        
    
# ==========================
# MOVIE DETAILS PAGE
# ==========================

@app.route("/movie/<movie_id>")
def movie_details(movie_id):

    if "username" not in session:
        return redirect(url_for("login"))


    url = (
        f"https://api.themoviedb.org/3/movie/{movie_id}"
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


        movie = response.json()



        details = get_movie_details(
            movie.get("title","")
        )



        return render_template(

            "movie.html",

            movie=movie,

            details=details

        )



    except Exception as e:


        print(
            "Movie Page Error:",
            e
        )


        return redirect(
            url_for("home")
        )





# ==========================
# GENRE MOVIES
# ==========================

@app.route("/genre/<int:genre_id>")
def genre_movies(genre_id):

    if "username" not in session:
        return redirect(url_for("login"))


    movies = get_movies_by_genre(
        genre_id
    )


    return render_template(

        "genre.html",

        username=session["username"],

        movies=movies

    )





# ==========================
# ADD FAVORITE
# ==========================

@app.route("/favorite/<movie>")
def add_favorite(movie):

    if "username" not in session:
        return redirect(url_for("login"))



    exists = favorites.find_one({

        "username": session["username"],

        "movie": movie

    })



    if not exists:


        favorites.insert_one({

            "username": session["username"],

            "movie": movie

        })



    flash(

        "Movie added to favourites.",

        "success"

    )


    return redirect(
        url_for("home")
    )





# ==========================
# REMOVE FAVORITE
# ==========================

@app.route("/remove-favorite/<movie>")
def remove_favorite(movie):

    if "username" not in session:
        return redirect(url_for("login"))



    favorites.delete_one({

        "username": session["username"],

        "movie": movie

    })



    flash(

        "Movie removed from favourites.",

        "success"

    )


    return redirect(
        url_for("view_favorites")
    )





# ==========================
# VIEW FAVORITES
# ==========================

@app.route("/favorites")
def view_favorites():

    if "username" not in session:
        return redirect(url_for("login"))



    movies = favorites.find({

        "username": session["username"]

    })



    return render_template(

        "favorites.html",

        username=session["username"],

        movies=movies

    )
# ==========================
# VIEW HISTORY
# ==========================

@app.route("/history")
def view_history():

    if "username" not in session:
        return redirect(url_for("login"))


    movie_history = history.find({

        "username": session["username"]

    }).sort("_id", -1)



    return render_template(

        "history.html",

        username=session["username"],

        history=movie_history

    )





# ==========================
# DELETE SEARCH HISTORY
# ==========================

@app.route("/delete-history/<history_id>")
def delete_history(history_id):

    if "username" not in session:
        return redirect(url_for("login"))


    try:

        history.delete_one({

            "_id": ObjectId(history_id),

            "username": session["username"]

        })


        flash(
            "History deleted successfully.",
            "success"
        )


    except Exception as e:

        print(
            "Delete History Error:",
            e
        )


    return redirect(
        url_for("view_history")
    )





# ==========================
# PROFILE
# ==========================

@app.route("/profile")
def profile():

    if "username" not in session:
        return redirect(url_for("login"))


    user = users.find_one({

        "username": session["username"]

    })


    return render_template(

        "profile.html",

        user=user

    )





# ==========================
# DASHBOARD
# ==========================

@app.route("/dashboard")
def dashboard():

    if "username" not in session:
        return redirect(url_for("login"))



    username = session["username"]



    search_count = history.count_documents({

        "username": username

    })


    favorite_count = favorites.count_documents({

        "username": username

    })


    recent_history = history.find({

        "username": username

    }).sort("_id",-1).limit(5)



    return render_template(

        "dashboard.html",

        username=username,

        search_count=search_count,

        favorite_count=favorite_count,

        history_count=search_count,

        recent_history=recent_history

    )





# ==========================
# TOP RATED MOVIES
# ==========================

@app.route("/top-rated")
def top_rated():

    if "username" not in session:
        return redirect(url_for("login"))



    movies = get_top_rated_movies()



    return render_template(

        "top_rated.html",

        username=session["username"],

        movies=movies

    )





# ==========================
# UPCOMING MOVIES
# ==========================

@app.route("/upcoming")
def upcoming_movies():

    if "username" not in session:
        return redirect(url_for("login"))



    movies = get_upcoming_movies()



    return render_template(

        "upcoming.html",

        username=session["username"],

        movies=movies

    )





# ==========================
# LOGOUT
# ==========================

@app.route("/logout")
def logout():

    session.clear()


    flash(

        "Logged out successfully.",

        "success"

    )


    return redirect(
        url_for("login")
    )





# ==========================
# ERROR HANDLERS
# ==========================

@app.errorhandler(404)
def page_not_found(error):

    return render_template(
        "error.html"
    ),404



@app.errorhandler(500)
def internal_server_error(error):

    return str(error),500





# ==========================
# RUN APPLICATION
# ==========================

if __name__ == "__main__":

    app.run(

        debug=True,

        host="0.0.0.0",

        port=5000

    )