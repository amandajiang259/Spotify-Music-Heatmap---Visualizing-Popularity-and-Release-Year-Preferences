# Import relevant libraries
import time
import requests # ver. 2.32.3
from collections import deque

# Class used to create SpotifyAPI objects that enable the gathering of data from Spotify
class SpotifyAPI:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = self.get_access_token()
        self.token_expiration_time = time.time() + 3600  # Tokens are valid for 1 hour
        self.call_times = deque()  # Track the timestamps of API calls
        self.rate_limit = 50  # Maximum calls in a 30-second window
        self.window_size = 30  # Rolling window in seconds

    def get_access_token(self):
        # Authenticate with Spotify and get an access token.
        url = "https://accounts.spotify.com/api/token"
        data = {"grant_type": "client_credentials"}
        response = requests.post(url, data=data, auth=(self.client_id, self.client_secret))
        if response.status_code != 200:
            raise Exception("Failed to authenticate with Spotify API")
        return response.json()["access_token"]

    def refresh_token_if_needed(self):
        # Refresh the access token if it's expired.
        if time.time() >= self.token_expiration_time:
            print("Access token expired. Refreshing token...")
            self.token = self.get_access_token()
            self.token_expiration_time = time.time() + 3600  # Reset the expiration time

    def wait_if_rate_limited(self):
        # Wait if the rate limit is close to being exceeded.
        current_time = time.time()

        # Remove timestamps outside the rolling window
        while self.call_times and self.call_times[0] < current_time - self.window_size:
            self.call_times.popleft()

        if len(self.call_times) >= self.rate_limit:
            # Calculate how long to wait
            wait_time = self.window_size - (current_time - self.call_times[0])
            print(f"Rate limit approaching. Waiting for {wait_time:.2f} seconds.")
            time.sleep(wait_time)

    def make_api_call(self, url, headers):
        # Make a single API call, respecting rate limits and refreshing the token if needed.
        self.refresh_token_if_needed()  # Ensure the token is valid
        headers["Authorization"] = f"Bearer {self.token}"  # Update header with the valid token

        self.wait_if_rate_limited()
        response = requests.get(url, headers=headers)
        self.call_times.append(time.time())  # Record the time of this call

        if response.status_code == 429:  # Rate limited
            retry_after = int(response.headers.get("Retry-After", 1))
            print(f"Rate limited. Retrying after {retry_after} seconds.")
            time.sleep(retry_after)
            return self.make_api_call(url, headers)  # Retry the call

        return response

    def get_playlist_tracks(self, playlist_id):
        # Retrieve all tracks from a playlist, handling pagination.
        url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks?limit=100"
        headers = {"Authorization": f"Bearer {self.token}"}

        all_tracks = []

        while url:
            response = self.make_api_call(url, headers)
            if response.status_code == 200:
                data = response.json()
                tracks = data.get("items", [])
                all_tracks.extend(tracks)
                url = data.get("next")  # Next page URL
            else:
                print(f"Failed to retrieve tracks: {response.status_code}")
                break

        return all_tracks

    def get_playlist_name(self, playlist_id):
        # Fetch the playlist name using the Spotify API.
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
        # Fetch artist popularity.
        url = f"https://api.spotify.com/v1/artists/{artist_id}"
        headers = {"Authorization": f"Bearer {self.token}"}
        response = self.make_api_call(url, headers)

        if response.status_code == 200:
            return response.json().get("popularity", None)
        else:
            print(f"Failed to fetch artist data for {artist_id}. Status code: {response.status_code}")
            return None

    def parse_playlist_data(self, playlist_id):
        # Extract and process release date and artist popularity.
        tracks = self.get_playlist_tracks(playlist_id)
        data = []
        count = 0

        for item in tracks:
            track = item.get("track")  # Access track data
            if not track:
                continue  # Skip if no track data

            release_date = track.get("album", {}).get("release_date", "Unknown")
            artist_id = track.get("artists", [{}])[0].get("id", None)

            if artist_id is None:
                print(f"Skipping track due to missing artist data: {track.get('name', 'Unknown')}")
                continue

            artist_popularity = self.get_artist_popularity(artist_id)
            if artist_popularity is not None:
                data.append((release_date, artist_popularity))
                count += 1

        print(f"Total songs processed: {count}")
        return data
