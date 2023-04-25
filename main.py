# SPOTIFY TIME MACHINE (Creates a Spotify Playlist with Billboard's Top 100 songs from the entered date)

import os
import spotipy
import requests
from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyOAuth


SPOTIFY_CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")
URL = "https://www.billboard.com/charts/hot-100/"


# Scraping Billboard 100
date = input("Which year do you want to travel to? Type the date in this format (YYYY-MM-DD): ")

response = requests.get(url=f"{URL}{date}/")
billboard_website_html = response.text
soup = BeautifulSoup(billboard_website_html, "html.parser")
song_list = soup.find_all(name="h3", id="title-of-a-story", class_="a-no-trucate")
top_100_songs = [song.getText().strip() for song in song_list]


# Spotify Authentication
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]


# Searching Spotify for songs by title
song_URI = []
year = date.split("-")[0]
for song in top_100_songs:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_URI.append(uri)
    except IndexError:
        pass


# Creating a new private playlist in Spotify
playlist_id = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)


# Adding songs found into the new playlist
sp.playlist_add_items(playlist_id["id"], items=song_URI)
print("Playlist Created!")