# from dotenv import load_dotenv
# import os
# import base64
# from requests import post
# import json

# load_dotenv()

# client_id = os.getenv("7df4568542cb41be8067f7a3d5faa09e")
# client_secret = os.getenv("e00f5391c34e43dd89c7484a971f38df")

# def get_token():
#     auth_string = client_id + ":" + client_secret
#     auth_bytes = auth_string.encode("utf-8")
#     auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

#     url = "https://accounts.spotify.com/api/token"
#     headers = {
#         "Authorization": "Basic " + auth_base64,
#         "Content-Type": "application/x-www-form-urlencoded"
#     }
#     data = {"grant_type": "client_credentials"}
#     result = post(url, headers = headers, data = data)
#     json_result = json.loads(result.content)
#     token = json_result["access_token"]
#     return token

# def get_auth_header(token):
#     return {"Authorization": "Bearer " + token}

# token = get_token()

import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Replace with your own values
CLIENT_ID = '7df4568542cb41be8067f7a3d5faa09e'
CLIENT_SECRET = 'e00f5391c34e43dd89c7484a971f38df'
REDIRECT_URI = 'http://localhost:8888/callback'

scope = "user-read-currently-playing user-read-playback-state user-modify-playback-state"

# Create a SpotifyOAuth object
sp_oauth = SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=scope
)

# Authenticate
sp = spotipy.Spotify(auth_manager=sp_oauth)

# Now you can use the API!
results = sp.current_user_playing_track()
print(results)