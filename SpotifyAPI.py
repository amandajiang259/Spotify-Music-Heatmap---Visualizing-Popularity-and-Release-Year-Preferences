import requests

class SpotifyAPI:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = self.get_access_token()

    def get_access_token(self):
        """Authenticate with Spotify and get an access token."""
        url = "https://accounts.spotify.com/api/token"
        data = {"grant_type": "client_credentials"}
        response = requests.post(url, data=data, auth=(self.client_id, self.client_secret))
        if response.status_code != 200:
            raise Exception("Failed to authenticate with Spotify API")
        return response.json()["access_token"]

    def get_playlist_tracks(self, playlist_id):
        if not self.token:
            print("No token available.")
            return None

        url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            tracks = response.json().get("items", [])
            return tracks
        else:
            print(f"Failed to retrieve tracks: {response.status_code}")
            return None

    def get_playlist_name(self, playlist_id):
        """Fetch the playlist name using the Spotify API."""
        url = f"https://api.spotify.com/v1/playlists/{playlist_id}"
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            playlist_data = response.json()
            return playlist_data.get("name", "Unknown Playlist")
        else:
            print(f"Failed to retrieve playlist name: {response.status_code}")
            return "Unknown Playlist"

    def get_artist_popularity(self, artist_id):
        """Fetch artist popularity."""
        url = f"https://api.spotify.com/v1/artists/{artist_id}"
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise Exception("Failed to fetch artist data")
        return response.json()["popularity"]

    def parse_playlist_data(self, playlist_id):
        """Extract and process release date and artist popularity."""
        tracks = self.get_playlist_tracks(playlist_id)
        data = []
        for item in tracks:
            track = item["track"]
            release_date = track["album"]["release_date"]
            artist_id = track["artists"][0]["id"]
            artist_popularity = self.get_artist_popularity(artist_id)
            data.append((release_date, artist_popularity))
        return data