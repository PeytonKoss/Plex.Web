import os
import json
import pandas as pd

# File Paths
movies_file = "C:/Users/peyto/Documents/!My Games/Plex.Web/data/Library - Movies - All [26].csv"
shows_file = "C:/Users/peyto/Documents/!My Games/Plex.Web/data/Library - TV Shows - All [24].json"
music_file = "C:/Users/peyto/Documents/!My Games/Plex.Web/data/Library - Music - All [35].json"
output_file = "C:/Users/peyto/Documents/!My Games/Plex.Web/index.html"

# Load Movies Data
movies_data = pd.read_csv(movies_file)
total_movies = len(movies_data)

# Load TV Shows Data
with open(shows_file, "r", encoding="utf-8") as f:
    shows_data = json.load(f)
total_shows = len(shows_data)
total_seasons = sum(len(show.get("seasons", [])) for show in shows_data)

# Load Music Data
with open(music_file, "r", encoding="utf-8") as f:
    music_data = json.load(f)
total_artists = len(music_data)
total_albums = sum(len(artist.get("albums", [])) for artist in music_data)
total_tracks = sum(
    len(album.get("tracks", [])) for artist in music_data for album in artist.get("albums", []))
# Format numbers with commas
num_albums = f"{total_albums:,}"  # Adds commas to total albums
num_tracks = f"{total_tracks:,}"  # Adds commas to total tracks

# CSS for scrolling and animation
scrolling_css = """
<style>
    @keyframes scroll-bg {
        0% { transform: translateY(5%) translateX(5%) scale(1.1); }
        50% { transform: translateY(-38%) translateX(-38%) scale(1.1); }
        100% { transform: translateY(5%) translateX(5%) scale(1.1); }
    }
    @keyframes staggered-slide {
        0% { opacity: 0; transform: translateY(20px); }
        100% { opacity: 1; transform: translateY(0); }
    }

    body {
        font-family: Arial, sans-serif;
        margin: 0; padding: 0;
        background-color: #121212;
        color: #fff;
    }
    .container {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 10px;
        padding: 20px;
        overflow: auto;
    }
    .category-card {
        position: relative;
        width: 80%; height: 150px;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.5);
        cursor: pointer;
        transition: transform 0.5s ease;
    }
    .category-card:hover { transform: scale(1.05); }

    .scrolling-background {
        position: absolute;
        top: 0; left: 0;
        width: 150%; height: 150%;
        animation: scroll-bg 120s linear infinite;
        filter: brightness(70%);
        z-index: -1;
    }
    .scrolling-background.movies { background: url('banners/movies_index.png') no-repeat center center/cover; }
    .scrolling-background.tvshows { background: url('banners/shows_index.png') no-repeat center center/cover; }
    .scrolling-background.music { background: url('banners/music_index.png') no-repeat center center/cover; }

    .overlay {
        position: absolute;
        top: 0; left: 0;
        width: 100%; height: 100%;
        background: rgba(0, 0, 0, 0.6);
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        color: #fff; /* Ensures text color is white */
    }
    .category-card .overlay h3 {
        margin: 0;
        font-size: 28px;
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        transition: transform 0.5s ease;
        color: #fff; /* Ensure title text is white */
    }
    .category-card:hover .overlay h3 {
        transform: translate(-50%, -200%); /* Slide up on hover */
    }
    .staggered div {
        opacity: 0;
        transform: translateY(35px);
        transition: all 0.5s ease;
    }
    .category-card:hover .staggered div:nth-child(1) {
        opacity: 1; transform: translateY(0); transition-delay: 0.1s;
    }
    .category-card:hover .staggered div:nth-child(2) {
        opacity: 1; transform: translateY(0); transition-delay: 0.2s;
    }
    .category-card:hover .staggered div:nth-child(3) {
        opacity: 1; transform: translateY(0); transition-delay: 0.3s;
    }
    .category-card:hover .staggered div:nth-child(4) {
        opacity: 1; transform: translateY(0); transition-delay: 0.4s;
    }

   /* Reverse the stagger when hover ends */
    .category-card .staggered div {
        transition-delay: 0.4s; /* Start the reverse with the last element */
    }
    .category-card .staggered div:nth-child(4) {
        transition-delay: 0.01s;
    }
    .category-card .staggered div:nth-child(3) {
        transition-delay: 0.075s;
    }
    .category-card .staggered div:nth-child(2) {
        transition-delay: 0.15s;
    }
    .category-card .staggered div:nth-child(1) {
        transition-delay: 0.225s;
    }
    .category-card:not(:hover) .overlay h3 {
        transition: transform 0.6s ease 0.3s; /* Delayed reset for smooth reverse */
    }
</style>

"""

# Start HTML Content
html_content = f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="default">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Plex Library - Main</title>
    {scrolling_css}
</head>
<body>
    <h1 style="text-align: center; padding: 20px;">🎥 PK+ 🎵</h1>
    <div class="container">
        <!-- Movies Card -->
        <a href="plex_movies.html" class="category-card">
            <div class="scrolling-background movies"></div>
            <div class="overlay">
                <h3>Movies</h3>
                <div class="staggered">
                    <div>{total_movies} Movies</div>
                    <div>(2.3 TB)</div>
                </div>
            </div>
        </a>
        <!-- TV Shows Card -->
        <a href="plex_tvshows.html" class="category-card">
            <div class="scrolling-background tvshows"></div>
            <div class="overlay">
                <h3>TV Shows</h3>
                <div class="staggered">
                    <div>{total_shows} Shows</div>
                    <div>{total_seasons} Seasons</div>
                    <div>(5.5 TB)</div>
                </div>
            </div>
        </a>
        <!-- Music Card -->

        <a href="plex_music.html" class="category-card">
            <div class="scrolling-background music"></div>
            <div class="overlay">
                <h3>Music</h3>
                <div class="staggered">
                    <div>{total_artists} Artists</div>
                    <div>{num_albums} Albums</div>
                    <div>{num_tracks} Tracks</div>
                    <div>(600 GB)</div>
                </div>
            </div>
        </a>
    </div>
</body>
</html>
'''

# Save the output file
with open(output_file, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Index HTML page generated: {output_file}")
