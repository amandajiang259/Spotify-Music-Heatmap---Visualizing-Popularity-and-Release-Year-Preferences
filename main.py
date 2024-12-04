import tkinter as tk
from tkinter import ttk, messagebox
import time
import threading
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
from minHeap import MinHeap
from hashmap import HashMap
from SpotifyAPI import SpotifyAPI


def generate_heatmap(frequency_map, playlist_name, generation_time, structure_choice):
    # Functionality same as your original function
    x_values = list(range(1960, 2025))
    y_values = list(range(0, 101))
    heatmap = np.zeros((len(y_values), len(x_values)))

    for key, count in frequency_map.items():
        year = int(key.split("-")[0])
        popularity = int(key.split("-")[1])
        if 1960 <= year <= 2024 and 0 <= popularity <= 100:
            x_idx = x_values.index(year)
            y_idx = y_values.index(popularity)
            heatmap[y_idx, x_idx] = count

    total_count = heatmap.sum()
    heatmap_normalized = heatmap / total_count if total_count > 0 else heatmap

    fig, ax = plt.subplots(figsize=(10, 6))
    img = ax.imshow(heatmap_normalized, cmap="viridis", aspect="auto",
                    extent=[1960, 2024, 0, 100], origin='lower')

    ax.set_title(f"Heatmap of Songs by Release Date and Artist Popularity\n"
                 f"Playlist: {playlist_name} | Structure: {structure_choice.capitalize()}",
                 fontsize=14)
    ax.set_xlabel("Year (Release Date)")
    ax.set_ylabel("Artist Popularity")
    cbar = plt.colorbar(img, label="Percentage of Songs (%)")
    plt.figtext(0.85, 0.95, f"Generation Time: {generation_time:.8f} sec", ha='center', fontsize=10,
                bbox=dict(facecolor='white', alpha=0.7))
    plt.show()


def process_data(playlist_id, structure_choice, label_status):
    CLIENT_ID = "dc0ce8799b2945a0bab45c6881104944"
    CLIENT_SECRET = "bebc2fd1df064f10be9382c921000dae"

    spotify = SpotifyAPI(CLIENT_ID, CLIENT_SECRET)
    label_status.config(text="Fetching data from Spotify...")
    try:
        data = spotify.parse_playlist_data(playlist_id)
        playlist_name = spotify.get_playlist_name(playlist_id)
    except Exception as e:
        messagebox.showerror("Error", f"Spotify API error: {e}")
        label_status.config(text="Idle")
        return

    start_time = time.perf_counter()
    if structure_choice == "heap":
        structure = MinHeap()
        for release_date, artist_popularity in data:
            structure.push(release_date, artist_popularity)
    elif structure_choice == "hashmap":
        structure = HashMap()
        for release_date, artist_popularity in data:
            structure.insert(release_date, artist_popularity)

    label_status.config(text="Generating heatmap...")
    frequency_map = structure.get_frequency()
    generation_time = time.perf_counter() - start_time
    generate_heatmap(frequency_map, playlist_name, generation_time, structure_choice)
    label_status.config(text="Idle")


def on_submit(entry_playlist_id, structure_choice, label_status):
    playlist_id = entry_playlist_id.get().strip()
    if not playlist_id:
        messagebox.showerror("Error", "Playlist ID cannot be empty.")
        return

    if structure_choice.get() not in {"heap", "hashmap"}:
        messagebox.showerror("Error", "Invalid structure choice. Please select Heap or HashMap.")
        return

    label_status.config(text="Processing...")
    threading.Thread(target=process_data, args=(playlist_id, structure_choice.get(), label_status)).start()


# Main GUI setup
def main_gui():
    root = tk.Tk()
    root.title("Spotify Playlist Heatmap Generator")
    root.geometry("400x300")

    # Playlist ID input
    tk.Label(root, text="Enter Playlist ID:").pack(pady=10)
    entry_playlist_id = tk.Entry(root, width=50)
    entry_playlist_id.pack(pady=5)

    # Data structure selection
    tk.Label(root, text="Select Data Structure:").pack(pady=10)
    structure_choice = tk.StringVar(value="heap")
    tk.Radiobutton(root, text="Heap", variable=structure_choice, value="heap").pack()
    tk.Radiobutton(root, text="HashMap", variable=structure_choice, value="hashmap").pack()

    # Status label
    label_status = tk.Label(root, text="Idle", fg="green")
    label_status.pack(pady=10)

    # Submit button
    ttk.Button(root, text="Generate Heatmap",
               command=lambda: on_submit(entry_playlist_id, structure_choice, label_status)).pack(pady=20)

    root.mainloop()


if __name__ == "__main__":
    main_gui()