from flask import Flask, request, jsonify
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity
from ast import literal_eval
import os

app = Flask(__name__)

# Verify files
path = "Datasets"
# print("Files in directory:", os.listdir(path))

try:
    credits_df = pd.read_csv(path + "/credits.csv")
    movies_df = pd.read_csv(path + "/movies.csv")
except Exception as e:
    print(f"Error reading CSV files: {e}")
    raise

# Display first few rows
# print("Movies DataFrame:")
# print(movies_df.head())
# print("\nCredits DataFrame:")
# print(credits_df.head())

# Rename columns in credits_df and merge with movies_df
credits_df.columns = ['id', 'title', 'cast', 'crew']
movies_df = movies_df.merge(credits_df, on="id")


# Display merged DataFrame
# print("\nMerged DataFrame:")
# print(movies_df.head())

# Demographic Filtering
C = movies_df["vote_average"].mean()
m = movies_df["vote_count"].quantile(0.9)

# print("\nC:", C)
# print("m:", m)

new_movies_df = movies_df.copy().loc[movies_df["vote_count"] >= m]
# print("\nNew Movies DataFrame shape:", new_movies_df.shape)

def weighted_rating(x, C=C, m=m):
    v = x["vote_count"]
    R = x["vote_average"]
    return (v/(v + m) * R) + (m/(v + m) * C)

new_movies_df["score"] = new_movies_df.apply(weighted_rating, axis=1)
new_movies_df = new_movies_df.sort_values('score', ascending=False)


# print("\nTop 10 Movies by Score:")
# print(new_movies_df[["original_title", "vote_count", "vote_average", "score"]].head(10))

# Plot top 10 movies
def plot():
    popularity = movies_df.sort_values("popularity", ascending=False)
    plt.figure(figsize=(12, 6))
    plt.barh(popularity["original_title"].head(10), popularity["popularity"].head(10), align="center", color="skyblue")
    plt.gca().invert_yaxis()
    plt.title("Top 10 Movies by Popularity")
    plt.xlabel("Popularity")
    # plt.show()

plot()

# Content-based Filtering
# print("\nMovie Overviews:")
# print(movies_df["overview"].head(5))

# Initialize TF-IDF Vectorizer and compute similarity matrix
tfidf = TfidfVectorizer(stop_words="english")
movies_df["overview"] = movies_df["overview"].fillna("")
tfidf_matrix = tfidf.fit_transform(movies_df["overview"])
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

# Create a Series for movie indices
indices = pd.Series(movies_df.index, index=movies_df["original_title"]).drop_duplicates()

def get_recommendations(title, cosine_sim=cosine_sim):
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    movies_indices = [ind[0] for ind in sim_scores]
    movies = movies_df["original_title"].iloc[movies_indices]
    return movies


# Data cleaning and feature extraction
features = ["cast", "crew", "keywords", "genres"]

for feature in features:
    movies_df[feature] = movies_df[feature].apply(literal_eval)

def get_director(x):
    for i in x:
        if i["job"] == "Director":
            return i["name"]
    return np.nan

def get_list(x):
    if isinstance(x, list):
        names = [i["name"] for i in x]
        if len(names) > 3:
            names = names[:3]
        return names
    return []

movies_df["director"] = movies_df["crew"].apply(get_director)

for feature in features:
    movies_df[feature] = movies_df[feature].apply(get_list)

def clean_data(x):
    if isinstance(x, list):
        return [str.lower(i.replace(" ", "")) for i in x]
    else:
        if isinstance(x, str):
            return str.lower(x.replace(" ", ""))
        else:
            return ""

for feature in ['cast', 'keywords', 'director', 'genres']:
    movies_df[feature] = movies_df[feature].apply(clean_data)

def create_soup(x):
    return ' '.join(x['keywords']) + ' ' + ' '.join(x['cast']) + ' ' + x['director'] + ' ' + ' '.join(x['genres'])

movies_df["soup"] = movies_df.apply(create_soup, axis=1)

# Initialize CountVectorizer and compute similarity matrix
count_vectorizer = CountVectorizer(stop_words="english")
count_matrix = count_vectorizer.fit_transform(movies_df["soup"])
cosine_sim2 = cosine_similarity(count_matrix, count_matrix)

movies_df = movies_df.reset_index()
indices = pd.Series(movies_df.index, index=movies_df['original_title'])

# print("\nContent-Based Filtering - Metadata Recommendations:")
# print("Recommendations for 'The Dark Knight Rises':")
# print(get_recommendations("The Dark Knight Rises", cosine_sim2))
# print("\nRecommendations for 'The Avengers':")
# print(get_recommendations("The Avengers", cosine_sim2))

# Interactive prompt for recommendations
# movie = input("Enter the movie: ")
# print(get_recommendations(movie, cosine_sim2))

@app.route('/recommendations', methods=['GET'])
def recommendations():
    movie_title = request.args.get('title')
    if not movie_title:
        return jsonify({"error": "No movie title provided."}), 400
    
    result = get_recommendations(movie_title, cosine_sim2)
    result_list = result.tolist()
    return jsonify({"recommendations": result_list})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)