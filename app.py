import streamlit as st
import pickle
import pandas as pd
import requests


def fetch_poster(movie_id):
  response = requests.get(
    'https://api.themoviedb.org/3/movie/{}?api_key=YOUR_TMDB_API_KEY&language=en%20US'
    .format(movie_id))
  if response.status_code == 200:
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
  else:
    return None


def recommend(movie):
  if movie in movies['title'].values:
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),
                         reverse=True,
                         key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
      movie_id = movies.iloc[i[0]].movie_id

      recommended_movies.append(movies.iloc[i[0]].title)
      poster_url = fetch_poster(movie_id)
      if poster_url:
        recommended_movies_posters.append(poster_url)
      else:
        recommended_movies_posters.append("URL_NOT_AVAILABLE")

    return recommended_movies, recommended_movies_posters
  else:
    return [], []


movies_dict = pickle.load(open('Movie Recommendation System/movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('Movie Recommendation System/similarity.pkl', 'rb'))

# Title
st.title('Movie Recommender System')

# SelectBox
selected_movie_name = st.selectbox('Select a movie:', movies['title'].values)

# Recommend
if st.button('Recommend'):
  names, posters = recommend(selected_movie_name)

  if names:
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
      st.text(names[0])
      st.image(posters[0])

    with col2:
      st.text(names[1])
      st.image(posters[1])

    with col3:
      st.text(names[2])
      st.image(posters[2])

    with col4:
      st.text(names[3])
      st.image(posters[3])

    with col5:
      st.text(names[4])
      st.image(posters[4])
  else:
    st.warning("Movie not found in the dataset.")
