import streamlit as st
import json

def show_genre():
    with open("data/songs.json", "r") as f:
        songs = json.load(f)

    st.write("🎶 Browse by Genre")
    genres = {}
    for song in songs:
        genre = song.get("genre", "Unknown")
        if genre not in genres:
            genres[genre] = []
        genres[genre].append(song)

    for genre, genre_songs in genres.items():
        st.subheader(genre)
        for song in genre_songs:
            st.markdown(f"""
            <div style="border: 1px solid #ccc; border-radius: 10px; padding: 1rem; margin-bottom: 1rem; background-color: #f9f9f9;">
                <h4>{song['title']}</h4>
                <p>{song['artist']}</p>
                <img src="{song['cover']}" width="100"/>
            </div>
            """, unsafe_allow_html=True)


# def run():
#     import streamlit as st
#     import pandas as pd
#     import joblib

#     df = pd.read_pickle('model/genre/data_by_genre.pkl')
#     scaled_features = joblib.load('model/genre/scaled_features_by_genre.pkl')
#     scaler = joblib.load('model/genre/scaler_by_genre.pkl')
#     model = joblib.load('model/genre/logreg_model_by_genre.pkl')

#     st.write("🎧 Rekomendasi Lagu Berdasarkan Genre")

#     available_genres = df['track_genre'].unique().tolist()
#     selected_genre = st.selectbox("Pilih Genre:", sorted(available_genres))
#     num_recommendations = st.slider("Jumlah Rekomendasi:", 1, 10, 5)

#     recommendations = df[df['track_genre'] == selected_genre].head(num_recommendations)
#     for _, row in recommendations.iterrows():
#         st.write(f"🎶 {row['track_name']} - {row['artists']}")


import base64

def get_base64_image(image_path):
    with open(image_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

image_base64 = get_base64_image("assets/cover.png")

def run():
    import streamlit as st
    import pandas as pd
    import joblib

    df = pd.read_pickle('model/genre/data_by_genre.pkl')
    scaled_features = joblib.load('model/genre/scaled_features_by_genre.pkl')
    scaler = joblib.load('model/genre/scaler_by_genre.pkl')
    model = joblib.load('model/genre/logreg_model_by_genre.pkl')

    st.write("🎧 Rekomendasi Lagu Berdasarkan Genre")

    # Pilihan genre
    available_genres = df['track_genre'].unique().tolist()
    selected_genre = st.selectbox("Pilih Genre:", sorted(available_genres))

    # Slider jumlah rekomendasi
    num_recommendations = st.slider("Jumlah Rekomendasi:", 1, 10, 5)

    # Tombol untuk menampilkan rekomendasi
    if st.button("Tampilkan Rekomendasi"):
        recommendations = df[df['track_genre'] == selected_genre].head(num_recommendations)
        
        if recommendations.empty:
            st.warning(f"Tidak ada lagu untuk genre '{selected_genre}'.")
        else:
            st.success(f"Menampilkan rekomendasi lagu dari genre '{selected_genre}'")
            for _, row in recommendations.iterrows():
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
                        background-color: black;
                        box-shadow: 2px 2px 8px rgba(0,0,0,0.05);
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
                            <p style="margin:0">{row['artists'][0]}</p>
                        </div>
                    </div>
                """, unsafe_allow_html=True)




