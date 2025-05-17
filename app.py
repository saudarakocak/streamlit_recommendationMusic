import streamlit as st
import json
from artis import show_artis
from genre import show_genre
import csv
import artis
import genre


# Load dummy data lagu
# with open("data/songs.json", "r") as f:
#     songs = json.load(f)

# Baca data dari CSV dan simpan ke list of dicts
songs = []
with open("model/artist/top_songs.csv", newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        songs.append(row)

st.set_page_config(page_title="Music App", layout="wide")

# Sidebar
st.sidebar.image("assets/logo.png", width=150)
menu = st.sidebar.radio("Menu", ["Populer", "Artis", "Genre"])

# Styling
st.markdown("""
    <style>
        .song-card {
            border: 1px solid #ccc;
            border-radius: 10px;
            padding: 1rem;
            margin-bottom: 1rem;
            background-color: #f9f9f9;
        }
    </style>
""", unsafe_allow_html=True)

# Header
st.title("🎵 Music Recommendations")

# Music Player
if "current_song" in st.session_state:
    song = st.session_state["current_song"]
    st.markdown(f"**Now Playing:** {song['title']} by {song['artist']}")
    st.audio(song["audio"], format="audio/mp3")
    st.markdown("---")

st.subheader(f"{menu}")

import base64
def get_base64_image(image_path):
    with open(image_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

image_base64 = get_base64_image("assets/cover.png")

# Content
if menu == "Populer":
    cols = st.columns(3)
    # for i, song in enumerate(songs[:6]):
    #     with cols[i % 3]:
    #         st.image(song["cover"], width=150)
    #         st.write(f"**{song['title']}**")
    #         st.caption(f"{song['artist']}")
    #         if st.button(f"▶️ Play", key=f"play_{i}"):
    #             st.session_state["current_song"] = song
    for i, song in enumerate(songs[:12]):
        with cols[i % 3]:
            with st.container():
                st.markdown(f"""
                    <div style="
                        border: 1px solid #ccc;
                        border-radius: 10px;
                        padding: 10px;
                        margin-bottom: 10px;
                        background-color: black;
                        text-align: center;
                    ">
                        <img src="data:image/png;base64,{image_base64}" alt="Album Art" style="width:120px; border-radius:8px;"/>
                        <h4 style="margin: 10px 0 5px;">{song['track_name']}</h4>
                        <p style="margin:0; color: #666;">{song['artists'].strip("[]").strip("'")}</p>
                    </div>
                """, unsafe_allow_html=True)

                # Tombol di luar div supaya tetap bisa diproses Python
                if st.button(f"▶️ Play", key=f"play_{i}"):
                    song = {
                            "title": song['track_name'],
                            "artist": song['artists'].strip("[]").strip("'"),
                            "cover": "assets/cover.png",
                            "audio": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"
                        }
                    st.session_state["current_song"] = song


elif menu == "Artis":
    artis.run()

elif menu == "Genre":
    genre.run()
