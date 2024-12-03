import matplotlib.pyplot as plt
import time
from minHeap import MinHeap
from hashmap import HashMap
from SpotifyAPI import SpotifyAPI


def add_track_to_heatmap_hash(heatmap_data, year, popularity):
    """Add a track's data to the heatmap."""
    # Popularity buckets in increments of 10
    popularity_buckets = {i: 0 for i in range(0, 101, 10)}
    bucket = (popularity // 10) * 10  # Find the bucket (0-9 -> 0, 10-19 -> 10, etc.)

    year_data = heatmap_data.get(year)
    if year_data is None:
        year_data = popularity_buckets.copy()
    year_data[bucket] += 1
    heatmap_data.insert(year, year_data)

def generate_heatmap(frequency_map, playlist_name, generation_time, structure_choice):
    x_values = []
    y_values = []
    colors = []

    total_count = sum(frequency_map.values())
    for (x, y), count in frequency_map.items():
        x_values.append(int(x.split("-")[0]))  # Convert year to integer
        y_values.append(y)
        colors.append(count / total_count)  # Percentage

    fig, ax = plt.subplots(figsize=(10, 6))
    scatter = ax.scatter(x_values, y_values, c=colors, cmap="viridis", s=100)

    ax.set_title(f"Heatmap of Songs by Release Date and Artist Popularity\n"
                 f"Playlist: {playlist_name} | Structure: {structure_choice.capitalize()}",
                 fontsize=14)

    # Add color bar
    plt.colorbar(scatter, label="Percentage of Songs (%)")
    ax.set_xlabel("Year (Release Date)")
    ax.set_ylabel("Artist Popularity")
    ax.grid(True)

    plt.figtext(0.85, 0.95, f"Generation Time: {generation_time:.2f} sec", ha='center', fontsize=12,
                bbox=dict(facecolor='white', alpha=0.7))

    # Show plot
    plt.show()


def main():
    CLIENT_ID = "35aeb022d82e4e4eab00a6d61fc4bd0c"
    CLIENT_SECRET = "c8a031c755134ec8ac17f4f969249bcb"
    playlist_id = input("Enter the Spotify playlist ID: ").strip()
    if not playlist_id:
        print("Error: Playlist ID cannot be empty.")
        return

    structure_choice = input("Choose the data structure (heap or hashmap): ").strip().lower()
    if structure_choice not in {"heap", "hashmap"}:
        print("Error: Invalid choice. Please choose 'heap' or 'hashmap'.")
        return

    spotify = SpotifyAPI(CLIENT_ID, CLIENT_SECRET)

    try:
        print("Fetching data from Spotify...")
        start_time = time.time()

        data = spotify.parse_playlist_data(playlist_id)
        playlist_name = spotify.get_playlist_name(playlist_id)
    except Exception as e:
        print(f"Error: {e}")
        return

    if structure_choice == "heap":
        structure = MinHeap()
        for release_date, artist_popularity in data:
            structure.push(release_date, artist_popularity)
    elif structure_choice == "hashmap":
        structure = HashMap()
        for release_date, artist_popularity in data:
            add_track_to_heatmap_hash(structure, release_date, artist_popularity)

    print("Generating heatmap...")
    frequency_map = structure.get_frequency()

    generation_time = time.time() - start_time
    generate_heatmap(frequency_map, playlist_name, generation_time, structure_choice)


if __name__ == "__main__":
    main()
