import streamlit as st
import pickle
import pandas as pd
import requests
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("OMDB_API_KEY")

st.set_page_config(page_title="CineMatch", page_icon="🎬", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@300;400;600&display=swap');

/* Background with animated stars */
.stApp {
    background: radial-gradient(ellipse at top, #0d0d1a 0%, #000000 60%);
    background-attachment: fixed;
    overflow: hidden;
}

/* Floating particles */
.stApp::before {
    content: '';
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    background-image:
        radial-gradient(1px 1px at 10% 20%, #ffffff33, transparent),
        radial-gradient(1px 1px at 30% 60%, #ffffff22, transparent),
        radial-gradient(1px 1px at 50% 10%, #ffffff44, transparent),
        radial-gradient(1px 1px at 70% 80%, #ffffff22, transparent),
        radial-gradient(1px 1px at 90% 40%, #ffffff33, transparent),
        radial-gradient(2px 2px at 20% 90%, #FF4B4B44, transparent),
        radial-gradient(2px 2px at 80% 10%, #FFD70044, transparent);
    pointer-events: none;
    z-index: 0;
}

header[data-testid="stHeader"] { background: transparent; }

/* 3D Title */
.main-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 80px;
    letter-spacing: 8px;
    text-align: center;
    margin-bottom: 0px;
    line-height: 1;
    background: linear-gradient(135deg, #FF4B4B 0%, #FFD700 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    /* 3D text shadow effect */
    filter: drop-shadow(0 1px 0 #cc3300)
            drop-shadow(0 2px 0 #aa2200)
            drop-shadow(0 3px 0 #881100)
            drop-shadow(0 4px 0 #660000)
            drop-shadow(0 8px 15px rgba(255,75,75,0.4));
    animation: float-title 4s ease-in-out infinite;
}

@keyframes float-title {
    0%, 100% { transform: translateY(0px); }
    50%       { transform: translateY(-8px); }
}

.subtitle {
    font-family: 'Inter', sans-serif;
    font-weight: 300;
    font-size: 13px;
    color: #888888;
    text-align: center;
    letter-spacing: 4px;
    text-transform: uppercase;
    margin-top: 8px;
}

@keyframes blink {
    0%, 100% { opacity: 1; }
    50%       { opacity: 0.2; }
}
.blink {
    animation: blink 2s ease-in-out infinite;
    color: #00D4FF;
    font-size: 12px;
    letter-spacing: 2px;
    text-align: center;
    text-transform: uppercase;
    margin-top: 4px;
}

.custom-divider {
    border: none;
    height: 1px;
    background: linear-gradient(to right, transparent, #FF4B4B, transparent);
    margin: 20px 0;
}

/* 3D Container */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(255, 255, 255, 0.03) !important;
    border: 1px solid rgba(255, 75, 75, 0.25) !important;
    border-radius: 20px !important;
    backdrop-filter: blur(20px);
    box-shadow:
        0 0 0 1px rgba(255,75,75,0.1),
        0 10px 40px rgba(0,0,0,0.6),
        0 2px 0 rgba(255,255,255,0.05) inset,
        0 -2px 0 rgba(0,0,0,0.3) inset !important;
    transform: perspective(1000px) rotateX(1deg);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

div[data-testid="stVerticalBlockBorderWrapper"]:hover {
    transform: perspective(1000px) rotateX(0deg) translateY(-4px);
    box-shadow:
        0 0 0 1px rgba(255,75,75,0.2),
        0 20px 60px rgba(0,0,0,0.8),
        0 2px 0 rgba(255,255,255,0.05) inset !important;
}

div[data-testid="stSelectbox"] label {
    font-family: 'Inter', sans-serif;
    color: #aaaaaa !important;
    font-size: 12px;
    letter-spacing: 2px;
    text-transform: uppercase;
}

div[data-testid="stSelectbox"] > div > div {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,75,75,0.3) !important;
    border-radius: 10px !important;
    color: white !important;
    box-shadow: 0 4px 15px rgba(0,0,0,0.3), inset 0 1px 0 rgba(255,255,255,0.1) !important;
}

/* 3D Button */
div[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #FF4B4B 0%, #FF8C00 100%) !important;
    color: white !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 14px 0 !important;
    font-size: 13px !important;
    /* 3D button effect */
    box-shadow:
        0 6px 0 #aa2200,
        0 8px 15px rgba(255,75,75,0.4) !important;
    transform: translateY(0px);
    transition: all 0.1s ease !important;
}
div[data-testid="stButton"] > button:hover {
    box-shadow:
        0 4px 0 #aa2200,
        0 6px 10px rgba(255,75,75,0.4) !important;
    transform: translateY(2px) !important;
}
div[data-testid="stButton"] > button:active {
    box-shadow: 0 1px 0 #aa2200 !important;
    transform: translateY(5px) !important;
}

/* 3D Movie card */
.movie-card {
    background: linear-gradient(145deg, rgba(255,255,255,0.07), rgba(255,255,255,0.02));
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 14px;
    padding: 8px;
    text-align: center;
    transform: perspective(600px) rotateY(0deg);
    transition: transform 0.4s ease, box-shadow 0.4s ease, border-color 0.4s ease;
    box-shadow:
        0 8px 32px rgba(0,0,0,0.5),
        inset 0 1px 0 rgba(255,255,255,0.1);
    cursor: pointer;
}
.movie-card:hover {
    transform: perspective(600px) rotateY(-8deg) translateY(-10px) scale(1.04);
    border-color: rgba(255, 75, 75, 0.6);
    box-shadow:
        8px 20px 40px rgba(0,0,0,0.7),
        -2px 0 20px rgba(255,75,75,0.3),
        inset 0 1px 0 rgba(255,255,255,0.15);
}
.movie-card img {
    border-radius: 8px;
    width: 100%;
    box-shadow: 0 4px 12px rgba(0,0,0,0.4);
}
.movie-title {
    font-family: 'Inter', sans-serif;
    font-size: 11px;
    color: #cccccc;
    letter-spacing: 0.5px;
    margin-top: 8px;
    text-align: center;
}

/* Result label */
.result-label {
    text-align: center;
    color: #888;
    font-size: 12px;
    letter-spacing: 3px;
    text-transform: uppercase;
    font-family: 'Inter', sans-serif;
}

div[data-testid="stAlert"] {
    background: rgba(255, 75, 75, 0.08) !important;
    border: 1px solid rgba(255, 75, 75, 0.3) !important;
    border-radius: 10px !important;
}
</style>
""", unsafe_allow_html=True)


# ── Data & functions ─────────────────────────────────────────────────────────
def fetch_poster(movie_title):
    url = f"http://www.omdbapi.com/?t={movie_title}&apikey={API_KEY}"
    response = requests.get(url)
    data = response.json()
    if data.get('Poster') and data['Poster'] != 'N/A':
        return data['Poster']
    return "https://via.placeholder.com/500x750/1a1a2e/FF4B4B?text=No+Poster"


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommend_movies = []
    for i in distances[1:6]:
        recommend_movies.append(movies.iloc[i[0]].title)
    return recommend_movies


movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
similarity  = pickle.load(open('similarity.pkl', 'rb'))
movies      = pd.DataFrame(movies_dict)


# ── Header ───────────────────────────────────────────────────────────────────
st.markdown("<div class='main-title'>CineMatch</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>AI · Powered · Movie · Recommendations · by · Jeevan</div>", unsafe_allow_html=True)
st.markdown("""
    <p class='blink'>✦ Boss just chill ✦</p>
""", unsafe_allow_html=True)
st.markdown("<hr class='custom-divider'>", unsafe_allow_html=True)


# ── Main card ────────────────────────────────────────────────────────────────
with st.container(border=True):
    selected_movie_name = st.selectbox(
        "PICK A MOVIE YOU ENJOYED",
        movies['title'].values,
        index=None,
        placeholder="Search by title..."
    )

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        clicked = st.button("🎬  Find My Movies", use_container_width=True)

    if clicked:
        if selected_movie_name:
            recommendations = recommend(selected_movie_name)

            st.markdown("<hr class='custom-divider'>", unsafe_allow_html=True)
            st.markdown(f"""
                <p class='result-label'>Because you watched · 
                <span style='color:#FF4B4B'>{selected_movie_name}</span></p>
            """, unsafe_allow_html=True)

            cols = st.columns(5)
            for idx, movie in enumerate(recommendations):
                with cols[idx]:
                    poster = fetch_poster(movie)
                    st.markdown(f"""
                        <div class='movie-card'>
                            <img src='{poster}'/>
                            <div class='movie-title'>{movie}</div>
                        </div>
                    """, unsafe_allow_html=True)
        else:
            st.warning("Please select a movie first.")