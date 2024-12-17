import json
import os

# Paths
json_file = r"C:/Users/peyto/Documents/!My Games/Plex.Web/data/Library - TV Shows - All [24].json"
output_file = r"C:/Users/peyto/Documents/!My Games/Plex.Web/plex_tvshows.html"
images_folder = "images/show_images"

# Load JSON data
with open(json_file, "r", encoding="utf-8") as f:
    tv_shows_data = json.load(f)

# Helper function to extract media details
def extract_media_details(episodes):
    resolutions, codecs, file_types, audio_codecs = set(), set(), set(), set()
    runtime_total, runtime_count = 0, 0
    year = "Unknown"

    for episode in episodes:
        media = episode.get("media", [{}])[0]
        resolution = media.get("videoResolution")
        codec = media.get("videoCodec")
        file_type = media.get("container")
        audio_codec = media.get("audioCodec")
        duration = media.get("duration") or 0
        episode_year = episode.get("year")

        if resolution:
            resolutions.add(f"{resolution}p")
        if codec:
            codecs.add(codec.upper())
        if file_type:
            file_types.add(file_type)
        if audio_codec:
            audio_codecs.add(audio_codec.upper())

        runtime_total += duration
        if duration:
            runtime_count += 1

        if episode_year and year == "Unknown":
            year = episode_year  # Assign year from the first episode

    average_runtime = runtime_total // runtime_count if runtime_count > 0 else 0
    return {
        "resolutions": ", ".join(sorted(resolutions)),
        "codecs": ", ".join(sorted(codecs)),
        "file_types": ", ".join(sorted(file_types)),
        "audio_codecs": ", ".join(sorted(audio_codecs)),
        "average_runtime": average_runtime // 60000,
        "year": year,
    }

# Start HTML content
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Plex TV Shows</title>
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
            --main-card-font-size: 14px;
            --focused-card-font-size: 12px;
            --season-card-font-size: 10px;
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
            grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
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
            font-size: var(--main-card-font-size);
            text-align: center;
            transition: all 0.5s ease;
            width: 100%; /* Make the width dynamic or adjust to desired size */
            max-width: 300px; /* Restrict the maximum width */
        }
        .card img {
            width: 100%;
            height: auto;
            border-radius: 8px;
            transition: transform 0.3s ease;
        }
        .card:hover img {
            transform: scale(1.1);
            filter: brightness(50%);
        }
        .details {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            opacity: 0;
            background: rgba(0, 0, 0, 0.7);
            text-align: center;
            padding: 0px;
            transition: opacity 0.3s ease;
        }
        .card:hover .details {
            opacity: 1;
        }
        .release-year {
            font-size: 14px;
            color: #aaa;
            margin-top: 5px;
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
        .focused-show {
            position: relative;
            height: 333px;            
            width: 200px;
            border-radius: 8px;
            margin-bottom: 20px;
            flex-shrink: 0;
            font-size: var(--focused-card-font-size);
            text-align: center;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        .season-grid {
            display: flex;
            flex-wrap: wrap;
            gap: 15px;
            margin: 20px auto 0 auto;
            padding: 10px;
            justify-content: center;
            max-width: 90%;
        }
        .season-card {
            position: relative;
            overflow: hidden;
            border-radius: 8px;
            text-align: center;
            width: 150px;
            height: 225px;
            font-size: var(--season-card-font-size);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        .season-card img {
            width: 100%;
            height: 100%;
            border-radius: 8px;
            transition: transform 0.3s ease;
        }
        .season-card:hover img {
            transform: scale(1.1);
            filter: brightness(70%);
        }
        .season-card .details {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            opacity: 0;
            background: rgba(0, 0, 0, 0.8);
            text-align: center;
            padding: 0;
            transition: opacity 0.3s ease;
        }
        .season-card:hover .details {
            opacity: 1;
        }
    </style>
</head>
<body>
    <div class="button-container">
        <a href="index.html" class="home-button">Home</a>
    </div>
    <h1 style="text-align: center; padding: 15px;">TV Shows</h1>
    <div class="search-container">
        <input type="text" id="search-bar" placeholder="Search shows...">
    </div>
    <div class="grid" id="tv-shows-grid">
"""

# Script continues with HTML generation and logic...
# Generate main cards and season grids
for show in tv_shows_data:
    # Extract media details for the show
    show_details = extract_media_details([ep for season in show.get("seasons", []) for ep in season.get("episodes", [])])
    total_episodes = sum(len(season.get("episodes", [])) for season in show.get("seasons", []))
    poster_path = f"{images_folder}/{show['ratingKey']}.thumb.jpg"

    html_content += f"""
        <div class="card" data-show="{show['ratingKey']}">
            <img src="{poster_path}" alt="{show['title']}">
            <div class="details">
                <h3>{show['title']}</h3>
                <p>Seasons: {len(show.get("seasons", []))} ({total_episodes} Episodes)</p>
                <p>Avg Runtime: {show_details['average_runtime']}m</p>
                <p>Resolution: {show_details['resolutions']}</p>
                <p>Codec: {show_details['codecs']}</p>
                <p>File Type: {show_details['file_types']}</p>
            </div>
            <div class="release-year">({show.get('originallyAvailableAt', 'Unknown')[:4]})</div>
        </div>
    """

    # Generate season grid
    html_content += "<div class='season-grid' style='display: none;'>"
    for season in show.get("seasons", []):
        # Extract media details for the season
        season_details = extract_media_details(season.get("episodes", []))
        season_poster_path = f"{images_folder}/{season['ratingKey']}.thumb.jpg"

        html_content += f"""
            <div class="season-card">
                <img src="{season_poster_path}" alt="{season['title']}">
                <div class="details">
                    <h3>{season['title']}</h3>
                    <p>Year: {season_details['year']}</p>
                    <p>Episodes: {len(season.get("episodes", []))}</p>
                    <p>Avg Runtime: {season_details['average_runtime']}m</p>
                    <p>Resolution: {season_details['resolutions']}</p>
                    <p>Codec: {season_details['codecs']}</p>
                </div>
                <div class="release-year">({season_details['year']})</div>
            </div>
        """
    html_content += "</div>"

# Add the closing HTML and JavaScript
html_content += """
    </div>
    <div class="overlay" id="overlay"></div>
    <script>
        // Live Search
        document.getElementById('search-bar').addEventListener('input', function(e) {
            const query = e.target.value.toLowerCase();
            const shows = document.querySelectorAll('.card');
            shows.forEach(show => {
                const title = show.querySelector('h3').textContent.toLowerCase();
                show.style.display = title.includes(query) ? 'block' : 'none';
            });
        });

        const cards = document.querySelectorAll('.card[data-show]');
        const overlay = document.getElementById('overlay');

        cards.forEach((card) => {
            card.addEventListener('click', () => {
                const isOverlayActive = overlay.classList.contains('active');
                overlay.innerHTML = '';

                if (isOverlayActive) {
                    overlay.classList.remove('active');
                    return;
                }

                const focusedShow = document.createElement('div');
                focusedShow.className = 'focused-show card';
                focusedShow.innerHTML = card.innerHTML;

                const seasonGrid = card.nextElementSibling.cloneNode(true);
                seasonGrid.style.display = 'flex';

                overlay.appendChild(focusedShow);
                overlay.appendChild(seasonGrid);
                overlay.classList.add('active');
            });
        });

        overlay.addEventListener('click', (e) => {
            if (e.target === overlay) {
                overlay.classList.remove('active');
            }
        });
    </script>
</body>
</html>
"""

# Write to file
with open(output_file, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"HTML file generated: {output_file}")

