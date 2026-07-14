class Config:

    # Flask Secret Key
    SECRET_KEY = "movie_ai_secret_key"

    # MongoDB Atlas Configuration
    MONGO_URI = "mongodb+srv://movieadmin:movie123@cluster0.fcdygaf.mongodb.net/movie_recommendation?retryWrites=true&w=majority&appName=Cluster0"
    DATABASE_NAME = "movie_recommendation"

    # TMDB API Key
    TMDB_API_KEY = "48b79977ecfca05dd1e05d036205791a"

    # Model Files
    MODEL_PATH = "model/similarity.pkl"
    MOVIES_PATH = "model/movies.pkl"