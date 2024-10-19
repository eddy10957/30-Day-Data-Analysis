# data_analysis.py - My small project applying Pandas for movie ratings analysis

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Create a sample movie ratings dataset
np.random.seed(42)
n_movies = 100
n_users = 1000

movies = pd.DataFrame({
    'movie_id': range(1, n_movies + 1),
    'title': [f'Movie {i}' for i in range(1, n_movies + 1)],
    'genre': np.random.choice(['Action', 'Comedy', 'Drama', 'Sci-Fi'], n_movies),
    'release_year': np.random.randint(1990, 2024, n_movies)
})

ratings = pd.DataFrame({
    'user_id': np.random.randint(1, n_users + 1, n_users * 10),
    'movie_id': np.random.randint(1, n_movies + 1, n_users * 10),
    'rating': np.random.randint(1, 6, n_users * 10)
})

print("1. Data Overview:")
print("\nMovies dataset:")
print(movies.head())
print("\nRatings dataset:")
print(ratings.head())

print("\n2. Basic Statistics:")
print("\nMovie statistics:")
print(movies.describe())
print("\nRatings statistics:")
print(ratings.describe())

print("\n3. Data Cleaning:")
# Remove duplicate ratings
ratings_clean = ratings.drop_duplicates()
print(f"\nRemoved {len(ratings) - len(ratings_clean)} duplicate ratings")

# Check for missing values
print("\nMissing values in movies dataset:")
print(movies.isnull().sum())
print("\nMissing values in ratings dataset:")
print(ratings_clean.isnull().sum())

print("\n4. Data Analysis:")
# Calculate average rating for each movie
movie_ratings = ratings_clean.groupby('movie_id')['rating'].agg(['mean', 'count']).reset_index()
movie_ratings = movie_ratings.merge(movies, on='movie_id')
movie_ratings = movie_ratings.sort_values('mean', ascending=False)

print("\nTop 10 highest-rated movies:")
print(movie_ratings[['title', 'mean', 'count']].head(10))

# Calculate average rating by genre
genre_ratings = movie_ratings.groupby('genre')[['mean', 'count']].mean().sort_values('mean', ascending=False)
print("\nAverage ratings by genre:")
print(genre_ratings)

# Analyze ratings distribution
plt.figure(figsize=(10, 6))
ratings_clean['rating'].hist(bins=5)
plt.title('Distribution of Ratings')
plt.xlabel('Rating')
plt.ylabel('Count')
plt.savefig('ratings_distribution.png')
plt.close()

# Analyze average rating by release year
year_ratings = movie_ratings.groupby('release_year')[['mean', 'count']].mean().reset_index()
plt.figure(figsize=(12, 6))
plt.scatter(year_ratings['release_year'], year_ratings['mean'], alpha=0.5)
plt.title('Average Rating by Release Year')
plt.xlabel('Release Year')
plt.ylabel('Average Rating')
plt.savefig('rating_by_year.png')
plt.close()

print("\n5. Insights:")
print(f"Total number of movies: {len(movies)}")
print(f"Total number of ratings: {len(ratings_clean)}")
print(f"Average rating across all movies: {ratings_clean['rating'].mean():.2f}")
print(f"Movie with highest average rating: {movie_ratings.iloc[0]['title']} ({movie_ratings.iloc[0]['mean']:.2f})")
print(f"Most rated movie: {movie_ratings.sort_values('count', ascending=False).iloc[0]['title']} ({int(movie_ratings.sort_values('count', ascending=False).iloc[0]['count'])} ratings)")
print(f"Highest-rated genre: {genre_ratings.index[0]} ({genre_ratings.iloc[0]['mean']:.2f})")

print("\n6. My custom experiment:")
# Analyze user rating behavior
user_ratings = ratings_clean.groupby('user_id')['rating'].agg(['mean', 'count', 'std']).reset_index()
print("\nUser rating behavior:")
print(user_ratings.describe())

# Find users with most diverse ratings
diverse_raters = user_ratings.sort_values('std', ascending=False).head(10)
print("\nTop 10 users with most diverse ratings:")
print(diverse_raters)

# Correlation between number of ratings and average rating
correlation = user_ratings['mean'].corr(user_ratings['count'])
print(f"\nCorrelation between number of ratings and average rating: {correlation:.2f}")

print("\nAnalysis complete! Check out 'ratings_distribution.png' and 'rating_by_year.png' for visualizations.")