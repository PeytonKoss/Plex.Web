import os
import json

# Paths
json_file = r"C:/Users/peyto/Documents/!My Games/Plex.Web/data/Library - Music - All [35].json"
output_file = r"C:/Users/peyto/Documents/!My Games/Plex.Web/plex_music.html"
images_folder = "images/music_images"

# Load JSON data
with open(json_file, "r", encoding="utf-8") as f:
    music_data = json.load(f)

# Start HTML content
html_content = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Plex Music</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #121212;
            color: #fff;
        }
        .button-container {
            margin: 20px;
            text-align: left;
        }
        .home-button {
            padding: 10px 20px;
            font-size: 16px;
            border: none;
            border-radius: 5px;
            background-color: #3a3a3a;
            color: white;
            cursor: pointer;
            text-decoration: none;
        }
        .home-button:hover {
            background-color: #555;
        }
        :root {
            --album-card-font-size: 14px;
            --artist-card-font-size: 12px;
        }
        .search-container {
            margin: 20px;
            text-align: center;
        }
        #search-bar {
            width: 50%;
            padding: 10px;
            border-radius: 8px;
            border: 1px solid #555;
            background-color: #1a1a1a;
            color: #fff;
            font-size: 16px;
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(125px, 1fr));
            gap: 20px;
            padding: 20px;
            justify-content: center;
            align-items: center;
        }
        .card {
            position: relative;
            overflow: hidden;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
            text-align: center;
            transition: all 0.5s ease;
            font-size: 12px;
            width: 100%; /* Make the width dynamic or adjust to desired size */
            max-width: 250px; /* Restrict the maximum width */
            aspect-ratio: 1 / 1; /* Forces a square ratio */
        }
        .album-card {
            position: relative;
            overflow: hidden;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
            text-align: center;
            font-size: var(--album-card-font-size);
            transition: all 0.5s ease;
            width: 100%; /* Make the width dynamic or adjust to desired size */
            max-width: 200px; /* Restrict the maximum width */
            aspect-ratio: 1 / 1; /* Forces a square ratio */
        }
        .card img, .album-card img {
            width: 100%;
            height: 100%;
            border-radius: 8px;
            transition: transform 0.3s ease;
        }
        .card:hover img, .album-card:hover img {
            transform: scale(1.1);
            filter: brightness(50%);
        }
        .details {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            padding: 10px;
            background: rgba(0, 0, 0, 0.7);
            transition: opacity 0.3s ease;
            width: 100%;
            height: 100%;
            opacity: 0;
        }
        .card:hover .details, .album-card:hover .details, .focused-card:hover .details {
            opacity: 1;
        }
        .overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(51, 51, 51, 0.9);
            z-index: 200;
            display: none;
            flex-direction: column;
            align-items: center;
            justify-content: flex-start;
            overflow-y: auto;
        }
        .overlay.active {
            display: flex;
        }
        .focused-card {
            position: relative; /* Keeps the card at the top during scrolling */
            top: 20px; /* Buffer from the top of the screen */
            margin: 0 auto 20px auto; /* Centered horizontally with bottom margin */
            width: 250px; /* Consistent size */
            border-radius: 8px;
            text-align: center;
            transition: all 0.5s ease;
            flex-shrink: 0;
            overflow: hidden;
        }

        .focused-card img {
            width: 100%;
            height: auto;
            border-radius: 8px;
            transition: transform 0.3s ease; /* Smooth hover effect */
        }

        .focused-card:hover img {
            transform: scale(1.05);
            filter: brightness(50%);
        }
        .album-grid {
            display: flex;
            flex-wrap: wrap;
            gap: 15px;
            margin: 20px auto 0 auto;
            padding: 10px;
            justify-content: center;
            max-width: 90%;
        }
    </style>
</head>
<body>
    <div class="button-container">
        <a href="index.html" class="home-button">Home</a>
    </div>
    <h1 style="text-align: center; padding: 15px;">Music</h1>
    <div class="search-container">
        <input type="text" id="search-bar" placeholder="Search artists...">
    </div>
    <div class="grid" id="music-grid">
'''

# Generate artist cards
for artist in music_data:
    artist_key = artist.get("ratingKey")
    artist_name = artist.get("title", "Unknown Artist")
    artist_poster_path = f"{images_folder}/{artist_key}.thumb.jpg"

    # Skip entries with any semicolons in the artist name
    if ";" in artist_name:
        continue

    if "♪" in artist_name:
        continue

    if not artist_key:
        continue

    albums = sorted(
        artist.get("albums", []),
        key=lambda a: a.get("originallyAvailableAt") or "9999",
        reverse=True
    )

    # Collect album years and track counts
    years = []
    total_tracks = 0
    album_cards = ""
    valid_album_count = 0

    for album in albums:
        album_key = album.get("ratingKey")
        album_title = album.get("title", "Unknown Album")
        album_date = album.get("originallyAvailableAt", "")
        album_year = album_date[:4] if album_date else "Unknown"
        album_tracks = album.get("tracks", [])

        if len(album_tracks) <= 1:
            continue

        years.append(int(album_year)) if album_year.isdigit() else None
        valid_album_count += 1
        total_tracks += len(album_tracks)
        audio_codec = album_tracks[0]["media"][0].get("audioCodec", "Unknown Codec")

        album_poster_path = f"{images_folder}/{album_key}.thumb.jpg"
        album_cards += f"""
            <div class="album-card">
                <img src="{album_poster_path}" alt="{album_title}">
                <div class="details">
                    <h3>{album_title}</h3>
                    <p>Tracks: {len(album_tracks)}</p>
                    <p>Codec: {audio_codec}</p>
                    <p>({album_year})</p>
                </div>
            </div>
        """

    # Skip artists with zero valid albums
    if valid_album_count == 0:
        continue

    # Artist year range
    year_range = f"{min(years)}-{max(years)}" if years else "Unknown"

    html_content += f"""
        <div class="card" data-artist="{artist_key}">
            <img src="{artist_poster_path}" alt="{artist_name}">
            <div class="details">
                <h3>{artist_name}</h3>
                <p>Albums: {valid_album_count} ({total_tracks} Tracks)</p>
                <p>({year_range})</p>
            </div>
        </div>
        <div class="overlay">
            <div class="focused-card">
                <img src="{artist_poster_path}" alt="{artist_name}">
                <div class="details">
                    <h3>{artist_name}</h3>
                    <p>Albums: {valid_album_count} ({total_tracks} Tracks)</p>
                    <p>({year_range})</p>
                </div>
            </div>
            <div class="album-grid">
                {album_cards}
            </div>
        </div>
    """

html_content += """
    </div>
    <script>
        // Live Search
        document.getElementById('search-bar').addEventListener('input', function(e) {
            const query = e.target.value.toLowerCase();
            const artists = document.querySelectorAll('.card');
            artists.forEach(artist => {
                const title = artist.querySelector('h3').textContent.toLowerCase();
                artist.style.display = title.includes(query) ? 'block' : 'none';
            });
        });

        const artistCards = document.querySelectorAll('.card[data-artist]');
        const overlays = document.querySelectorAll('.overlay');

        artistCards.forEach((card, index) => {
            card.addEventListener('click', () => {
                overlays.forEach(o => o.classList.remove('active'));
                overlays[index].classList.add('active');
            });
        });

        overlays.forEach(overlay => {
            overlay.addEventListener('click', (e) => {
                if (!e.target.closest('.focused-card') && !e.target.closest('.album-card')) {
                    overlay.classList.remove('active');
                }
            });
        });
    </script>
</body>
</html>
"""

# Save the HTML file
with open(output_file, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Music HTML page generated: {output_file}")
