import streamlit as st
import pandas as pd
import requests

def fetch_poster(movie_id):
    response = requests.get("https://api.themoviedb.org/3/movie/{}?api_key=aee93cb3693450d7ae1240d0e360af26&language=en-US".format(movie_id))
    data = response.json()
    poster_path = data.get('poster_path')
    if poster_path:
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        return full_path
    else:
        return "image.png"

def recommend_movies(movie_title, cosine_sim, movies_list):
    idx = movies_list[movies_list['title'] == movie_title].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]

    recommend_movies = []
    recommended_movies_poster = []
    for i in sim_scores:
        movie_id = movies_list['id'].iloc[i[0]]
        recommend_movies.append(movies_list['title'].iloc[i[0]])
        recommended_movies_poster.append(fetch_poster(movie_id))

    return recommend_movies, recommended_movies_poster

movies_list = pd.read_pickle('movies.pkl')
cosine_sim = pd.read_pickle('similarity.pkl')

st.set_page_config(
    page_title="Search Your Relative Movies",
    page_icon="image.png"
)

title_style = "font-size: 40px; color: pale-blue; font-family: Georgia, serif;"
image = st.image("image.png" , width=80)
st.markdown(f'<h1 style="{title_style}">Search Your Relative Movies</h1>', unsafe_allow_html=True)


selected_movie_name = st.selectbox(
    "",
    movies_list['title'].values,
    index=None,
    help="Select Movies..."
)

names = []
posters = []

if st.button('Show Movies'):
    names, posters = recommend_movies(selected_movie_name, cosine_sim, movies_list)

st.subheader(f"Recommended Movies for {selected_movie_name}")

html_content = """
<style>
    *,
    *:after {
      box-sizing: border-box;
    }

    h1 {
      font-size: clamp(20px, 15vmin, 20px);
      font-family: sans-serif;
      color: hsl(0 0% 98%);
      position: relative;
    }

    h1:after {
      content: "";
      position: absolute;
      width: 100%;
      height: 5px;
      background: hsl(130 80% 50%);
      left: 0;
      bottom: 0;
    }
</style>
"""

st.write(html_content, unsafe_allow_html=True)

num_columns = 3
for i in range(0, len(names), num_columns):
    columns = st.columns(num_columns)
    for j in range(num_columns):
        if i + j < len(names):
            with columns[j]:
                st.image(posters[i + j], width=200)
                st.markdown(f"<h1>{names[i + j]}</h1>", unsafe_allow_html=True)
