#!/bin/bash

# Variables
CLIENT_ID="dc0ce8799b2945a0bab45c6881104944"
CLIENT_SECRET="bebc2fd1df064f10be9382c921000dae"
PLAYLIST_ID=$1  # Get playlist ID from the first argument
OUTPUT_FILE="tempo_and_keys.txt"

# Validate the playlist ID
if [ -z "$PLAYLIST_ID" ]; then
    echo "Error: Playlist ID is required."
    exit 1
fi

# Step 1: Get the access token
TOKEN_RESPONSE=$(curl -k -s -X POST "https://accounts.spotify.com/api/token" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "grant_type=client_credentials&client_id=$CLIENT_ID&client_secret=$CLIENT_SECRET"
)

# Extract the access token from the response (using grep/sed)
TOKEN=$(echo '{"access_token":"BQCKw4-UL0gBvaq1MJiAndbUJ7kiV-RySmI9HoAli6GW7VSz2P1oWoTVcDGLyswMlj5piSpX99qYyFROOnkvM4-xmsaxyEIL-titnYsEz6HTG4DDsyk","token_type":"Bearer","expires_in":3600}' \
    | grep -o '"access_token":"[^"]*"' \
    | sed 's/"access_token":"\([^"]*\)"/\1/')

# Check if the token was extracted
if [ -z "$TOKEN" ]; then
    echo "Failed to get access token."
    exit 1
fi

# Step 2: Get tracks from the playlist
TRACK_IDS=$(curl -s -k -X GET "https://api.spotify.com/v1/playlists/$PLAYLIST_ID/tracks?fields=items(track(id))&limit=100" \
     -H "Authorization: Bearer $TOKEN" | grep -o '"id":"[^"]*"' | sed 's/"id":"\([^"]*\)"/\1/')

# Check if TRACK_IDS is empty
if [ -z "$TRACK_IDS" ]; then
    echo "No tracks found or invalid playlist ID."
    exit 1
fi

# Step 3: Get audio features for each track and output tempo and key
echo "Track ID | Album Release Date | Artist Popularity" > $OUTPUT_FILE
for TRACK_ID in $TRACK_IDS; do
    TRACK=$(curl -s -k --request GET \
  --url https://api.spotify.com/v1/tracks/$TRACK_ID \
  --header "Authorization: Bearer $TOKEN")
    
    # Extract release date using grep and sed
    RELEASE_DATE=$(echo $TRACK | grep -o '"release_date":"[^"]*"' | sed 's/"release_date":"\([^"]*\)"/\1/')
    
    # Extract artist ID using grep and sed
    ARTIST_ID=$(echo $TRACK | grep -o '"id":"[^"]*"' | sed 's/"id":"\([^"]*\)"/\1/' | head -n 1)
    
    # Get artist metadata
    ARTIST=$(curl -s -k --request GET \
  --url https://api.spotify.com/v1/artists/$ARTIST_ID \
  --header "Authorization: Bearer $TOKEN")
    
    # Extract artist popularity using grep and sed
    ARTIST_POPULARITY=$(echo $ARTIST | grep -o '"popularity":[^,]*' | sed 's/"popularity":\([^,]*\)/\1/')
    
    echo "$TRACK_ID | $RELEASE_DATE | $ARTIST_POPULARITY" >> $OUTPUT_FILE
done

echo "Data saved to $OUTPUT_FILE"
