from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

df = pd.read_csv("netflix_titles.csv")

# 🎬 Recommendation Logic
def recommend_content(genre, content_type):
    filtered = df[
        (df['listed_in'].str.contains(genre, case=False, na=False)) &
        (df['type'] == content_type)
    ]

    return filtered[['title', 'rating']].head(5).to_dict('records')


# 📊 Business Insights
def get_insights():
    top_genres = df['listed_in'].str.split(', ').explode().value_counts().head(5)
    content_type = df['type'].value_counts()
    top_countries = df['country'].value_counts().head(5)

    return {
        "top_genres": top_genres,
        "content_type": content_type,
        "top_countries": top_countries
    }


# 🏠 Home Page
@app.route("/")
def home():
    return render_template("index.html")


# 🎯 Recommendation Page
@app.route("/recommend", methods=["POST"])
def recommend():
    genre = request.form.get("genre")
    content_type = request.form.get("type")

    results = recommend_content(genre, content_type)
    return render_template("recommend.html", results=results)


# 📊 Dashboard Page
@app.route("/dashboard")
def dashboard():
    insights = get_insights()
    return render_template("dashboard.html", insights=insights)


if __name__ == "__main__":
    app.run(debug=True)