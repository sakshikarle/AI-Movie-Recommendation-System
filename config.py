class Config:

    # Flask Secret Key
    SECRET_KEY = "movie_ai_secret_key"

    # MongoDB Configuration
    MONGO_URI = "mongodb://localhost:27017"
    DATABASE_NAME = "movie_recommendation"

    # TMDB API Key
    TMDB_API_KEY = "48b79977ecfca05dd1e05d036205791a"

    # Model Files
    MODEL_PATH = "model/similarity.pkl"
    MOVIES_PATH = "model/movies.pkl"