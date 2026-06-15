import os
import pickle
import requests

from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)

ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173")
CORS(app, origins=[origin.strip() for origin in ALLOWED_ORIGINS.split(",") if origin.strip()])

MOVIES_PKL = os.getenv("MOVIES_PKL", "movies_list.pkl")
SIMILARITY_PKL = os.getenv("SIMILARITY_PKL", "similarity.pkl")
OMDB_API_KEY = os.getenv("OMDB_API_KEY", "")
FLASK_RUN_PORT = int(os.getenv("FLASK_RUN_PORT", "5000"))


def load_pickle(path):
    with open(path, "rb") as file:
        return pickle.load(file)

try:
    movies = load_pickle(MOVIES_PKL)
    similarity = load_pickle(SIMILARITY_PKL)
except FileNotFoundError as exc:
    raise SystemExit(f"Missing artifact: {exc.filename}") from exc

poster_cache = {}
session = requests.Session()


def fetch_poster(title):
    if title in poster_cache:
        return poster_cache[title]

    if not OMDB_API_KEY:
        poster_cache[title] = "https://via.placeholder.com/500x750?text=No+API+Key"
        return poster_cache[title]

    try:
        url = f"http://www.omdbapi.com/?t={title}&apikey={OMDB_API_KEY}"
        response = session.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        poster = data.get("Poster", "https://via.placeholder.com/500x750?text=No+Image")
    except requests.RequestException:
        poster = "https://via.placeholder.com/500x750?text=Error"

    poster_cache[title] = poster
    return poster


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@app.route("/movie_titles", methods=["GET"])
def get_title():
    return jsonify(list(movies["title"].values))


@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.get_json(silent=True)
    if not data or "movie" not in data:
        return jsonify({"error": "movie is required"}), 400

    movie = data["movie"]
    if movie not in movies["title"].values:
        return jsonify([])

    index = movies[movies["title"] == movie].index[0]
    distance = list(enumerate(similarity[index]))
    sorted_movies = sorted(distance, key=lambda x: x[1], reverse=True)[1:6]

    recommendations = []
    for position, score in sorted_movies:
        title = movies.iloc[position].title
        poster = fetch_poster(title)
        recommendations.append({"title": title, "poster": poster})

    return jsonify(recommendations)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=FLASK_RUN_PORT, debug=os.getenv("FLASK_ENV") == "development")


