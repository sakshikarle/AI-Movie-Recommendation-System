# 🎬 AI Movie Recommendation System

An AI-powered Movie Recommendation System built using **Flask**, **Python**, **MongoDB**, and the **TMDB API**. The application recommends similar movies based on content-based filtering and provides a modern, user-friendly interface with authentication and personalized features.

---

## Features

-  User Registration & Login
-  AI-Based Movie Recommendations
-  Movie Search
-  Add & Remove Favorites
-  Search History
-  User Dashboard
-  Trending Movies
-  Top Rated Movies
-  Genre-Based Movies
-  Upcoming Movies
-  Movie Posters & Details
-  Trailer Support
-  Responsive UI
-  Modern User Interface

---

##  Tech Stack

### Frontend
- HTML5
- CSS3
- JavaScript
- Bootstrap

### Backend
- Python
- Flask

### Database
- MongoDB

### Machine Learning
- Pandas
- Scikit-learn
- CountVectorizer
- Cosine Similarity

### API
- TMDB (The Movie Database) API

---

##  Project Structure

```
AI-Movie-Recommendation-System/
│
├── app.py
├── recommendation.py
├── config.py
├── requirements.txt
├── Procfile
├── runtime.txt
│
├── model/
│   ├── movies.pkl
│   └── similarity.pkl
│
├── static/
│   ├── css/
│   ├── js/
│   ├── images/
│   └── videos/
│
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── favorites.html
│   ├── history.html
│   └── recommendations.html
│
└── README.md
```

---

## Installation

### Clone Repository

```bash
git clone https://github.com/yourusername/AI-Movie-Recommendation-System.git

cd AI-Movie-Recommendation-System
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

Windows

```bash
venv\Scripts\activate
```

Linux / Mac

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

##  Run the Project

```bash
python app.py
```

Open your browser:

```
http://127.0.0.1:5000
```

---

##  Recommendation Algorithm

The recommendation engine uses **Content-Based Filtering**.

Steps:

1. Load movie dataset.
2. Preprocess movie genres and metadata.
3. Convert text into vectors using **CountVectorizer**.
4. Calculate similarity using **Cosine Similarity**.
5. Recommend the Top Similar Movies.

---

## Database

MongoDB stores:

- User Accounts
- Favorites
- Search History

---

##  TMDB API

The project uses the TMDB API to fetch:

- Movie Posters
- Overview
- Ratings
- Release Date
- Cast
- Trailers
- Similar Movies

---

##  Screenshots

Add screenshots here.

Example:

- Login Page
- Home Page
- Recommendation Page
- Dashboard
- Favorites
- History

---

## 🔮 Future Enhancements

- AI Chatbot for Movie Suggestions
- Voice Search
- Multi-language Support
- User Ratings & Reviews
- Watchlist
- Personalized Recommendations using Deep Learning

---

##  Developer

**Sakshi Karle**

Bachelor of Engineering (B.E.)

Python | Flask | MongoDB | Machine Learning | Web Development

---

##  License

This project is developed for educational and learning purposes.

---

## ⭐ Support

If you like this project, don't forget to give it a ⭐ on GitHub.
