import streamlit as st
import json
import pandas as pd
import joblib

def show_artis():
    with open("data/songs.json", "r") as f:
        songs = json.load(f)

    st.write("🔍 Browse by Artist")
    for song in songs:
        st.markdown(f"""
        <div style="border: 1px solid #ccc; border-radius: 10px; padding: 1rem; margin-bottom: 1rem; background-color: #f9f9f9;">
            <h4>{song['title']}</h4>
            <p>{song['artist']}</p>
            <img src="{song['cover']}" width="100"/>
        </div>
        """, unsafe_allow_html=True)

import base64

def get_base64_image(image_path):
    with open(image_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

image_base64 = get_base64_image("assets/cover.png")

def run():
    df = joblib.load("model/artist/data.pkl")
    scaled_features = joblib.load("model/artist/scaled_features.pkl")
    artists_df = pd.read_csv("model/artist/top_artists.csv")
    artists = sorted(artists_df["artist"].unique())

    st.write("🎵 Rekomendasi Lagu Berdasarkan Nama Artis")
    selected_artist = st.selectbox("Pilih Artis", artists)
    x = st.slider("Jumlah Rekomendasi:", 1, 10, 5)

    if st.button("Tampilkan Rekomendasi"):
        artist_tracks = df[df["artists"].apply(lambda x: selected_artist in x)]
        if artist_tracks.empty:
            st.warning(f"Tidak ada lagu dari artis '{selected_artist}'.")
        else:
            st.success(f"Menampilkan rekomendasi lagu dari artis '{selected_artist}'")
            for _, row in artist_tracks.head(x).iterrows():
                # HTML untuk card
                st.markdown(f"""
                    <style>
                    .song-card {{
                        display: flex;
                        align-items: center;
                        border: 1px solid #ccc;
                        border-radius: 10px;
                        padding: 10px;
                        margin-bottom: 15px;
                        background-color: #f9f9f9;
                        box-shadow: 2px 2px 8px rgba(0,0,0,0.05);
                        background-color: black;
                    }}
                    .song-card img {{
                        border-radius: 8px;
                        width: 80px;
                        height: 80px;
                        object-fit: cover;
                        margin-right: 15px;
                    }}
                    .song-info {{
                        flex-grow: 1;
                    }}
                    .song-button {{
                        margin-left: auto;
                    }}
                    </style>

                    <div class="song-card">
                        <img src="data:image/png;base64,{image_base64}" alt="Album Art"/>
                        <div class="song-info">
                            <h4 style="margin:0">{row['track_name']}</h4>
                            <p style="margin:0">{selected_artist}</p>
                        </div>
                    </div>
                """, unsafe_allow_html=True)