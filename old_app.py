import streamlit as st
import pickle
import requests
import os
from secret import OMDB_API_KEY

#load api 
API_KEY = OMDB_API_KEY

@st.cache_data(show_spinner=False)
def fetch_poster(movie_id):
    try:
        
        url = f"http://www.omdbapi.com/?t={movie_id}&apikey={OMDB_API_KEY}"
        response = requests.get(url)
        response.raise_for_status()
        data=response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return  "http://img.omdbapi.com/?apikey={OMDM_API_KEY}&"+poster_path
        else:
            return "https://via.placeholder.com/500x750?text=No+Image"
        
    except:
        return "https://via.placeholder.com/500x750?text=No+Image"


#load movie data
try:    
    movies = pickle.load(open("movies_list.pkl", 'rb'))
    similarity = pickle.load(open("similarity.pkl", 'rb'))
except FileNotFoundError:
    st.error("required moedl files not found.Please check 'movies.pkl' and 'similarity.pkl'.")
    st.stop()

movies_list=movies['title'].values


#app header
st.header("Movie Recommender System")


#carousel
import streamlit.components.v1 as components

imageCarouselComponent = components.declare_component("image-carousel-component", path="frontend_old\public")
imageUrls = [
    fetch_poster(1632),
    fetch_poster(299536),
    fetch_poster(17455),
    fetch_poster(2830),
    fetch_poster(429422),
    fetch_poster(9722),
    fetch_poster(13972),
    fetch_poster(240),
    fetch_poster(155),
    fetch_poster(598),
    fetch_poster(914),
    fetch_poster(255709),
    fetch_poster(572154)
   
    ]


imageCarouselComponent(imageUrls=imageUrls, height=200)
selectvalue=st.selectbox("Select movie from dropdown", movies_list)


#recommendation logic
def recommend(movie):
    if movie not in movies['title'].values:
        return [],[]
    
    index = movies[movies['title']==movie].index[0]
    distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector:vector[1])
    recommend_movie=[]
    recommend_poster=[]

    for i in distance[1:6]:
        movies_id=movies.iloc[i[0]].id
        recommend_movie.append(movies.iloc[i[0]].title)
        recommend_poster.append(fetch_poster(movies_id))
    
    return recommend_movie, recommend_poster


#recommend button
if st.button("Show Recommend"):
    with st.spinner("Fetching posters..."):
         movie_name, movie_poster = recommend(selectvalue)
    
    col1,col2,col3,col4,col5=st.columns(5)
    with col1:
        st.text(movie_name[0])
        st.image(movie_poster[0])
    with col2:
        st.text(movie_name[1])
        st.image(movie_poster[1])
    with col3:
        st.text(movie_name[2])
        st.image(movie_poster[2])
    with col4:
        st.text(movie_name[3])
        st.image(movie_poster[3])
    with col5:
        st.text(movie_name[4])
        st.image(movie_poster[4])