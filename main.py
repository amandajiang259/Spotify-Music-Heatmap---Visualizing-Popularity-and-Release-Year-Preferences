# Import relevant libraries
import time
import numpy as np
import matplotlib.pyplot as plt
from minHeap import MinHeap
from hashmap import HashMap
from SpotifyAPI import SpotifyAPI

# Function used to create a heatmap based on popularity and date of release, and display it.
def generate_heatmap(frequency_map, playlist_name, generation_time, structure_choice):
    print(frequency_map)

    # Extract years and popularity values from the frequency map
    x_values = sorted({int(key.split("-")[0]) for key in frequency_map.keys()})  # Extract years
    y_values = sorted({int(key.split("-")[1]) for key in frequency_map.keys()})  # Extract unique popularity values from the map

    # Create a 2D grid (heatmap matrix)
    heatmap = np.zeros((len(y_values), len(x_values)))  # Rows = popularity, columns = years

    # Fill the heatmap with frequencies
    for key, count in frequency_map.items():
        year = int(key.split("-")[0])  # Extract year from the key
        popularity = int(key.split("-")[1])  # Extract popularity from the key
        x_idx = x_values.index(year)  # Column index (year)
        y_idx = y_values.index(popularity)  # Row index (popularity)
        heatmap[y_idx, x_idx] = count  # Assign count to the grid cell

    # Normalize the heatmap for coloring (percentage of total)
    total_count = heatmap.sum()
    heatmap_normalized = heatmap / total_count

    # Create the heatmap
    fig, ax = plt.subplots(figsize=(10, 6))
    img = ax.imshow(heatmap_normalized, cmap="viridis", aspect="auto",
                    extent=[min(x_values), max(x_values), min(y_values), max(y_values)],
                    origin='lower')

    # Add titles and labels
    ax.set_title(f"Heatmap of Songs by Release Date and Artist Popularity\n"
                 f"Playlist: {playlist_name} | Structure: {structure_choice.capitalize()}",
                 fontsize=14)
    ax.set_xlabel("Year (Release Date)")
    ax.set_ylabel("Artist Popularity")
    ax.grid(False)  # Disable the grid for a cleaner heatmap look

    # Add color bar for intensity
    cbar = plt.colorbar(img, label="Percentage of Songs (%)")

    # Add text annotation for generation time
    plt.figtext(0.85, 0.95, f"Generation Time: {generation_time:.8f} sec", ha='center', fontsize=10,
                bbox=dict(facecolor='white', alpha=0.7))

    # Show plot
    plt.show()

# Main function used to handle user input and function calls
def main():
    CLIENT_ID = "684b5f074fa14833a3e66e09442e81bd"
    CLIENT_SECRET = "d156206f74ab4d20aac0b0b0e0ba2ebe"
    playlist_id = input("Enter the Spotify playlist ID: ").strip() # Prompts the user to input the ID of the playlist
    if not playlist_id: # If the user inputs an invalid (empty) playlist ID, then print an error
        print("Error: Playlist ID cannot be empty.")
        return

    # Prompts the user to enter the desired datastructure to complete the operation
    structure_choice = input("Choose the data structure (heap or hashmap): ").strip().lower()

    # If the user has not chosen a valid datastructure, print an error message
    if structure_choice not in {"heap", "hashmap"}:
        print("Error: Invalid choice. Please choose 'heap' or 'hashmap'.")
        return

    spotify = SpotifyAPI(CLIENT_ID, CLIENT_SECRET)
    # Try to gather data from Spotify using the API
    try:
        print("Fetching data from Spotify...")

        data = spotify.parse_playlist_data(playlist_id)
        playlist_name = spotify.get_playlist_name(playlist_id)
    # If the data cannot be gathered, print the error message and return
    except Exception as e:
        print(f"Error: {e}")
        return

    # If the user has entered "heap" as their choice of datastructure, then set the structure to a MinHeap() object and push the release date and popularity values
    if structure_choice == "heap":
        start_time = time.perf_counter()
        structure = MinHeap()
        for release_date, artist_popularity in data:
            structure.push(release_date, artist_popularity)
    # Otherwise if the user has entered "hashmap" as their choice of datastructure, set the structure to HashMap() object and push the release date and popularity values
    elif structure_choice == "hashmap":
        start_time = time.perf_counter()
        structure = HashMap()
        for release_date, artist_popularity in data:
            structure.insert(release_date, artist_popularity)

    # Print a message to the console informing the user that the heatmap is being generated
    print("Generating heatmap...")
    frequency_map = structure.get_frequency()
    generation_time = time.perf_counter() - start_time # Calculate the time it took to generate
    generate_heatmap(frequency_map, playlist_name, generation_time, structure_choice) # Create and display the heatmap for the user

if __name__ == "__main__":
    main()