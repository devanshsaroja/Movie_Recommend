import streamlit as st
import pickle as pk
import pandas as pd
import requests

# Load the data
movies_dict = pk.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pk.load(open('similarity.pkl', 'rb'))

# Fetch movie posters from the API
def fetch_posters(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=3786a13ea0c164ca7502af894bafff62&language=en-US')
    data = response.json()
    return 'https://image.tmdb.org/t/p/w500/' + data['poster_path']

# Recommend function to get similar movies
def recommend(movie):
    ll = []
    
    # Normalize input: strip spaces and lowercase all words
    movie = movie.strip().lower()

    # Normalize titles in the DataFrame and find the index of the specified movie
    matched_movies = movies[movies['title'].str.strip().str.lower() == movie]
    
    # Check if the movie is found
    if matched_movies.empty:
        st.write(f"Movie '{movie}' not found in the dataset.")
        return [], []  # Return empty lists if no match is found
    
    # Get the index of the movie in the DataFrame
    index = matched_movies.index[0]
    
    # Get the list of similar movies
    movies_list = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    movies_list = movies_list[1:6]  # Get top 5 similar movies, excluding the movie itself

    recommended_movies_posters = []
    recommended_movies = []
    
    for i in movies_list:
        # Access the movie title using iloc
        recommended_movies.append(movies.iloc[i[0]]['title'])
        
        # Fetch movie poster using the movie ID
        movie_id = movies.iloc[i[0]]['id']
        recommended_movies_posters.append(fetch_posters(movie_id))
    
    return recommended_movies, recommended_movies_posters


st.title("MOVIE RECOMMENATION SYSTEM")
st.image("sunrise.jpeg", caption="Sunrise by the mountains")


option = st.selectbox(
    "Movies",
    (movies['title'].values),
)

if st.button("Recommend"):
    names, posters=recommend(option)

# Create 5 columns
cols = st.columns(5)
# Loop through each column
for i in range(5):
    with cols[i]:  # Access each column by its index
        st.text(names[i])  # Different header for each column
        st.image(posters[i])