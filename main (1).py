
from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load movie and TV show data
df = pd.read_csv("Copy of movies_tv_guide - movies_tv_guide.csv")


# HOME PAGE
@app.route("/")
def home():
    movies_data = df.to_dict(orient="records")

    genres = sorted(
        df["genre"].dropna().astype(str).str.strip().unique().tolist()
    )

    platforms = sorted(
        df["platform"].dropna().astype(str).str.strip().unique().tolist()
    )

    return render_template(
        "index.html",
        movies=movies_data,
        genres=genres,
        platforms=platforms
    )


# GENRES PAGE
@app.route("/genre")
def genre():
    selected_genre = request.args.get("genre", "").strip()

    filtered_df = df

    if selected_genre:
        filtered_df = df[
            df["genre"].fillna("").astype(str).str.strip().str.casefold()
            == selected_genre.casefold()
        ]

    movies_data = filtered_df.to_dict(orient="records")

    return render_template(
        "genre.html",
        movies=movies_data,
        selected_genre=selected_genre
    )


# PLATFORMS PAGE
@app.route("/platform")
def platform():
    selected_platform = request.args.get("platform", "").strip()

    filtered_df = df

    if selected_platform:
        filtered_df = df[
            df["platform"].fillna("").astype(str).str.strip().str.casefold()
            == selected_platform.casefold()
        ]

    movies_data = filtered_df.to_dict(orient="records")

    return render_template(
        "platform.html",
        movies=movies_data,
        selected_platform=selected_platform
    )


# SEARCH
@app.route("/search", methods=["POST"])
def search():
    search_term = request.form.get("search", "").strip().lower()

    results = df[
        df.apply(
            lambda row: row.astype(str).str.lower()
            .str.contains(search_term, regex=False).any(),
            axis=1
        )
    ]

    genres = sorted(
        df["genre"].dropna().astype(str).str.strip().unique().tolist()
    )

    platforms = sorted(
        df["platform"].dropna().astype(str).str.strip().unique().tolist()
    )

    return render_template(
        "index.html",
        movies=results.to_dict(orient="records"),
        genres=genres,
        platforms=platforms,
        search_term=search_term
    )


if __name__ == "__main__":
    app.run(debug=True)
