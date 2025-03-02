import streamlit  as st
import pickle
import pandas as pd
import  requests
import gzip
import os

# 914c8081c0fbc417e62a135966381641
# https://image.tmdb.org/t/p/w500/1E5baAaEse26fej7uHcjOgEE2t2.jpg

def fetch_poster(movie_id):
    response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=914c8081c0fbc417e62a135966381641&language=en-Us")
    data = response.json()
    # st.text(data)

    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommend_movies = []
    recommend_movies_posters = []

    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommend_movies.append(movies.iloc[i[0]].title)

        #  Fetch Poster from Api
        recommend_movies_posters.append(fetch_poster(movie_id))

    return recommend_movies , recommend_movies_posters

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))

#Merging pickl files into single file
chunk_files = ['similarity_part_1.pkl.gz', 'similarity_part_2.pkl.gz', 'similarity_part_3.pkl.gz',
               'similarity_part_4.pkl.gz', 'similarity_part_5.pkl.gz', 'similarity_part_6.pkl.gz',
               'similarity_part_7.pkl.gz', 'similarity_part_8.pkl.gz']  # Add all parts

# Merge the chunks
merged_data = b""
for file in chunk_files:
    with gzip.open(file, 'rb') as f:
        merged_data += f.read()

# Save the reconstructed pickle file
with open('similarity.pkl', 'wb') as f:
    f.write(merged_data)

# Load the similarity model after reconstruction
similarity = pickle.load(open('similarity.pkl', 'rb'))
print("Similarity model loaded successfully!")

# end of pkl file merge

#similarity = pickle.load(open('similarity.pkl', 'rb'))

movies = pd.DataFrame(movies_dict)

st.title('Movie Recommender System')

selected_movie_name = st.selectbox('How would you like to be contacted?',
                      movies['title'].values)


if st.button('Recommend'):
    names ,poster = recommend(selected_movie_name)

    col1, col2, col3 ,col4,col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(poster[0])

    with col2:
        st.text(names[1])
        st.image(poster[1])

    with col3:
        st.text(names[2])
        st.image(poster[2])

    with col4:
        st.text(names[3])
        st.image(poster[3])

    with col5:
        st.text(names[4])
        st.image(poster[4])
