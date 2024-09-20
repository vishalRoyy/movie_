import pickle
import streamlit as st
import requests
import pandas as pd

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        poster_path = data.get('poster_path', '')
        return f"matrix_1999_subway_original_film_art_a_0bddb409-7b88-41f8-a2e0-1eb811b4f7e2.webp" if poster_path else None
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch poster for movie_id: {movie_id}. Error: {e}")
        return None

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].get('movie_id', '')  # Use 'get' to avoid KeyError
        if not movie_id:
            continue
        poster_url = fetch_poster(movie_id)
        if poster_url:
            recommended_movie_posters.append(poster_url)
            recommended_movie_names.append(movies.iloc[i[0]].title)
    return recommended_movie_names, recommended_movie_posters

st.markdown(
    """
    <style>
    .stApp {
        background-image: url('https://your-image-url.com/your-background-image.jpg');
        background-size: cover;
        background-position: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.header('Movie Recommender System')

# Load the pickle files with error handling
try:
    # Load DataFrame and similarity matrix
    movies = pickle.load(open('C:/Users/HARSHIT ANAND/Desktop/data/movie.pkl', 'rb'))
    similarity = pickle.load(open('C:/Users/HARSHIT ANAND/Desktop/data/similarity.pkl', 'rb'))

    # Check the type of 'movies' and its columns
    if not isinstance(movies, pd.DataFrame):
        st.error("The loaded 'movies' data is not a DataFrame.")
    else:
        st.write("Columns in movies DataFrame:", movies.columns)  # Display columns for debugging
        
        if 'title' not in movies.columns:
            st.error("The loaded data does not contain the 'title' column.")
        else:
            movie_list = movies['title'].values
            selected_movie = st.selectbox(
                "Type or select a movie from the dropdown",
                movie_list
            )

            if st.button('Show Recommendation'):
                recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
                
                # Display recommendations in columns
                cols = st.columns(5)
                for col, name, poster in zip(cols, recommended_movie_names, recommended_movie_posters):
                    with col:
                        st.text(name)
                        st.image(poster)

except FileNotFoundError as e:
    st.error(f"File not found: {e}")
except KeyError as e:
    st.error(f"Column not found: {e}")
except Exception as e:
    st.error(f"An error occurred: {e}")
