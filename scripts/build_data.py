import argparse
import pickle
from pathlib import Path

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def build_recommendation_artifacts(dataset_path: Path, movies_out: Path, similarity_out: Path, max_features: int):
    df = pd.read_csv(dataset_path)
    df = df[["id", "title", "overview", "genre"]].copy()
    df["overview"] = df["overview"].fillna("")
    df["genre"] = df["genre"].fillna("")
    df["tags"] = df["overview"] + " " + df["genre"]

    vectorizer = CountVectorizer(max_features=max_features, stop_words="english")
    vectors = vectorizer.fit_transform(df["tags"].astype("U")).toarray()
    similarity = cosine_similarity(vectors)

    df = df.drop(columns=["overview", "genre", "tags"])

    movies_out.parent.mkdir(parents=True, exist_ok=True)
    similarity_out.parent.mkdir(parents=True, exist_ok=True)

    with open(movies_out, "wb") as movie_file:
        pickle.dump(df, movie_file)

    with open(similarity_out, "wb") as sim_file:
        pickle.dump(similarity, sim_file)

    print(f"Saved {movies_out} and {similarity_out}")


def parse_args():
    parser = argparse.ArgumentParser(description="Build movie recommendation artifacts.")
    parser.add_argument("--dataset", default="dataset.csv", help="Input dataset CSV file.")
    parser.add_argument("--movies-out", default="movies_list.pkl", help="Movie artifact output path.")
    parser.add_argument("--similarity-out", default="similarity.pkl", help="Similarity artifact output path.")
    parser.add_argument("--max-features", type=int, default=10000, help="Max features for CountVectorizer.")
    return parser.parse_args()


def main():
    args = parse_args()
    build_recommendation_artifacts(
        Path(args.dataset),
        Path(args.movies_out),
        Path(args.similarity_out),
        args.max_features,
    )


if __name__ == "__main__":
    main()
