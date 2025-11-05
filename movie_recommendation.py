import streamlit as st
import pickle
import pandas as pd
from difflib import SequenceMatcher

st.title('Movie Recommendation System')

similarity = pickle.load(open('similarity_mtx.pkl','rb'))
def sentence_similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()

def recommendations(movie):
    movie_idx = data[data['title'].str.lower() == movie.lower()]
    word_similarity = set()
    movie_id = set()
    if not movie_idx.empty:
        movie_idx = movie_idx.index[0]
        distance = similarity[movie_idx]
        movie_list = sorted(list(enumerate(distance)),reverse=True,key = lambda x: x[1])[0:6]
        for i in movie_list:
            word_similarity.add(data.iloc[i[0]].title)
            movie_id.add(data.iloc[i[0]].id)


    for i,df_movie in enumerate(data['title'].str.lower()):
        ratio = sentence_similarity(df_movie,movie.lower())
        if ratio >= 0.8:
            word_similarity.add(data.iloc[i].title)
            movie_id.add(data.iloc[i].id)
    return word_similarity,movie_id
movie_dist = pickle.load(open('movie_dist.pkl', 'rb'))
data = pd.DataFrame(movie_dist)

option = st.selectbox(
    'Select Movie Recommendation System',
    data['title'].values)

if st.button('recommend'):
    movie_recommend_list,movie_id = recommendations(option)
    for i in movie_recommend_list:
        # st.image
        st.write(i)