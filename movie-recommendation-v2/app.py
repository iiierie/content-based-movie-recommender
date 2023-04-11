import numpy
import pandas
import pickle
import requests
import streamlit as st
similarity = pickle.load(open('similarity.pkl','rb'))
movies = pickle.load(open('movies_list.pkl', 'rb'))

import requests

def getposters(m_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=fb7016c253f63cedcd89d18381bbc01c&language=en-US'.format(m_id))
    data = response.json()
    if 'poster_path' in data:
        return 'https://image.tmdb.org/t/p/w500/' + data['poster_path']
    else:
        return None



def recommend(movie):
    recommended_movies = []
    recommended_movies_posters = []
    movie_index = movies[movies['title'] == movie].index[0]
    ## then find the similiar vector for this particular movie
    curr_movie_similarity = similarity[movie_index]
    movies_list = sorted(list(enumerate(curr_movie_similarity)), reverse=True, key=lambda x: x[1])[1:6]

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        ## get poster from some API
        recommended_movies_posters.append(getposters(movie_id))
        recommended_movies.append((movies.iloc[i[0]].title))
    return recommended_movies , recommended_movies_posters


st.title('Movie Recommendation System')
selected_movie_name = st.selectbox(
    'Select a movie for more similiar recommendations',
    movies.title)

st.write('So, you watched \n', selected_movie_name)
import streamlit as st

if st.button('Recommend'):
    names, poster = recommend(selected_movie_name)
    if names and poster:
        st.write('You should definitely try watching one of these similar movies:')
        num_columns = 3
        cols = []
        for j in range(len(names)):
            if j % num_columns == 0:
                col = st.columns(num_columns,gap="medium")
                cols.append(col)

            with cols[j // num_columns][j % num_columns]:
                st.text(names[j])
                st.image(poster[j])
    else:
        st.write('Sorry, no similar movies found.')
else:
    st.write('Click for recommendations')



