# Spotify Music Heatmap - Visualizing Popularity and Release Date Preferences
Welcome to our Spotify Music Heatmap generator!


How to Run Our Code:

1. verify that you are using Python version 3.11 or 3.12
2. verify that you have installed all of the following libraries/packages, which are necessary to run this program
    a. requests          ver. 2.32.3
    b. numpy             ver. 2.1.3
    c. matplotlib        ver. 3.9.3
3. run the program through the main.cpp file
4. first enter the ID for the playlist you wish to use for the heatmap (there is a list provided below, we recommend a smaller one (1000, or less), but larger ones will work too)
5. now enter either "hashmap" or "heap" to choose which datastructure you wish to use in order to create the heatmap.
6. wait while the data is fetched from Spotify (this can take some time for larger datasets/playlists since Spotify limits the number of API calls per 30 second window)
7. review the heatmap that has been generated
