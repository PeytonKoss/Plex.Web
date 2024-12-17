import pandas as pd

# Load the CSV file
csv_file = r"C:/Users/peyto/Documents/!My Games/Plex.Web/data/Library - Movies - All [26].csv"  # Update the correct path
movies_data = pd.read_csv(csv_file)

# Helper function for runtime formatting
def format_runtime(milliseconds):
    if pd.isna(milliseconds):
        return "Unknown Runtime"
    seconds = milliseconds // 1000
    minutes = (seconds // 60) % 60
    hours = seconds // 3600
    return f"{int(hours)} Hour{'s' if hours != 1 else ''} {int(minutes)} Minute{'s' if minutes != 1 else ''}"

# Helper function for resolution formatting
def format_resolution(res):
    if res == "4k":
        return "2160p"
    return f"{res}p"

# Generate HTML content
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Plex Movies</title>
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
            grid-template-columns: repeat(auto-fill, minmax(175px, 1fr));
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
            max-width: 250px;
            transition: all 0.5s ease;
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
        .details h3 {
            margin: 10px 0;
            font-size: 18px;
        }
        .details p {
            margin: 5px 0;
            font-size: 14px;
        }
        .release-year {
            font-size: 14px;
            color: #aaa;
            margin-top: 5px;
        }
    </style>
</head>
<body>
    <div class="button-container">
        <a href="index.html" class="home-button">Home</a>
    </div>
    <h1 style="text-align: center; padding: 15px;">Movies</h1>
    <div class="search-container">
        <input type="text" id="search-bar" placeholder="Search movies...">
    </div>
    <div class="grid" id="movies-grid">
"""

# Populate movie cards, ignoring entries without a ratingKey
for _, movie in movies_data.iterrows():
    if pd.isna(movie['ratingKey']):  # Skip movies without a ratingKey
        continue

    title = movie['title']
    rating_key = str(int(movie['ratingKey']))
    poster_path = f"images/movie_images/{rating_key}.thumb.jpg"
    year = f"({int(movie['year'])})" if 'year' in movie and pd.notna(movie['year']) else ""
    runtime = format_runtime(movie['duration']) if 'duration' in movie else "Unknown Runtime"
    resolution = format_resolution(movie['media.videoResolution']) if 'media.videoResolution' in movie else "Unknown"
    codec = movie['media.videoCodec'].upper() if 'media.videoCodec' in movie else "Unknown"
    rating = movie['contentRating'] if 'contentRating' in movie and pd.notna(movie['contentRating']) else "NR"
    audio_codec = movie['media.audioCodec'].upper() if 'media.audioCodec' in movie else "Unknown Audio"
    container = f".{movie['media.container']}" if 'media.container' in movie else "Unknown Format"

    html_content += f"""
        <div class="card">
            <img src="{poster_path}" alt="{title}">
            <div class="details">
                <h3>{title}</h3>
                <p>Runtime: {runtime}</p>
                <p>Rating: {rating}</p>
                <p>Resolution: {resolution}</p>
                <p>Codec: {codec}</p>
                <p>Audio: {audio_codec}</p>
                <p>File Type: {container}</p>
            </div>
            <div class="release-year">{year}</div>
        </div>
    """

# Close the HTML structure
html_content += """
    </div>
    <script>
        // JavaScript for Live Search
        document.getElementById('search-bar').addEventListener('input', function(e) {
            const query = e.target.value.toLowerCase();
            const movies = document.querySelectorAll('.card');
            movies.forEach(movie => {
                const title = movie.querySelector('h3').textContent.toLowerCase();
                movie.style.display = title.includes(query) ? 'block' : 'none';
            });
        });
    </script>
</body>
</html>
"""

# Save the dynamic HTML file
output_file = r"C:/Users/peyto/Documents/!My Games/Plex.Web/plex_movies.html"  # Update with your desired path
with open(output_file, 'w', encoding='utf-8') as file:
    file.write(html_content)

print(f"Dynamic HTML with search and return button generated: {output_file}")
