import requests
import time

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

        url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks?limit=100"
        headers = {"Authorization": f"Bearer {self.token}"}

        all_tracks = []  # To store all tracks

        while url:  # While there's a URL for the next page
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                data = response.json()
                tracks = data.get("items", [])
                all_tracks.extend(tracks)  # Add the new tracks to the list

                # Update the URL to the next page of results
                url = data.get("next")  # This will be None if no more pages
            elif response.status_code == 429:  # Rate limit exceeded
                retry_after = int(response.headers.get('Retry-After', 1))  # Default to 1 second if no header is found
                print(f"Rate limit exceeded, retrying after {retry_after} seconds.")
                time.sleep(retry_after)  # Wait for the specified time before retrying
            else:
                print(f"Failed to retrieve tracks: {response.status_code}")
                break  # Stop if there was an error

        return all_tracks

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

        if response.status_code == 429:  # If rate limited
            retry_after = int(response.headers.get('Retry-After', 1))  # Default to 1 second if no header is found
            print(f"Rate limited, waiting for {retry_after} seconds.")
            time.sleep(retry_after)  # Wait for the time specified in the Retry-After header

            # Retry after waiting
            response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print(f"Failed to fetch artist data for {artist_id}. Status code: {response.status_code}")
            return None  # Handle failed response

        return response.json().get("popularity", None)

    def parse_playlist_data(self, playlist_id):
        """Extract and process release date and artist popularity."""
        tracks = self.get_playlist_tracks(playlist_id)  # Get all tracks across multiple pages
        data = []
        count = 0

        for item in tracks:
            # Access the track data properly (it's inside 'track' in the item)
            track = item.get("track")  # item is a dictionary containing the 'track' key
            if not track:
                continue  # Skip if there's no 'track' data

            release_date = track.get("album", {}).get("release_date", "Unknown")
            artist_id = track.get("artists", [{}])[0].get("id", None)

            if artist_id is None:
                print(f"Skipping track due to missing artist data: {track.get('name', 'Unknown')}")
                continue  # Skip this track if artist data is missing

            artist_popularity = self.get_artist_popularity(artist_id)
            if artist_popularity is not None:
                data.append((release_date, artist_popularity))
                count += 1

        print(f"Total songs: {count}")
        return data
