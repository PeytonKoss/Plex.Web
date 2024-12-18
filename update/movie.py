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
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="default">
    <meta name="theme-color" content="#121212">
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
            position: fixed;
            z-index: 300;
        }
        .home-button {
            padding: 10px 20px;
            font-size: 25px;
            border: 1px solid #555;
            border-radius: 16px;
            background-color: #212121;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
            color: white;
            cursor: pointer;
            text-decoration: none;
        }
        .home-button:hover {
            background-color: #666;
        }
        .flipped-arrow {
            display: inline-block; /* Ensure transform applies */
            transform: scaleX(-1); /* Flip the arrow horizontally */
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
            grid-template-columns: repeat(auto-fill, minmax(145px, 1fr));
            gap: 10px;
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
        .card.active .details {
            opacity: 1; /* Mimics the hover effect */
        }
        .card.active img {
            transform: scale(1.1); /* Optional: Keep zoom effect */
            filter: brightness(50%);
        }
        .details h3 {
            margin: 10px 0;
            font-size: 14px;
        }
        .details p {
            margin: 7px 0;
            font-size: 10px;
        }
        .release-year {
            font-size: 12px;
            color: #aaa;
            margin-top: 5px;
        }
        #scroll-to-top {
            display: none;
            position: fixed;
            width: 40px; /* Set button width */
            height: 40px; /* Set button height */
            top: 10px;
            left: 50%;
            padding: 10px;
            padding-top: 10px; /* Add artificial space above the ^ */
            font-size: 20px;
            background-color: #212121;
            color: #fff;
            border: 1px solid #555;
            border-radius: 24px;
            cursor: pointer;
            z-index: 200;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
            transition: top 0.5s ease, opacity 0.5s ease;
        }
        #scroll-to-top:hover {
            background-color: #666;
        }
        #scroll-to-top.visible {
            display: block;
            transform: translateX(-50%);
            opacity: 1;
        }
    </style>
</head>
<body>
    <div class="button-container">
        <a href="index.html" class="home-button">
            <span class="flipped-arrow">➔</span>
        </a>
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
            <img src="{poster_path}" loading="lazy" alt="{title}">
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
    <button id="scroll-to-top">^</button>
    <script>
        // Enable hover effect toggle on click
        document.querySelectorAll('.card').forEach(card => {
            card.addEventListener('click', () => {
                const isActive = card.classList.contains('active');

                // Remove 'active' class from all cards
                document.querySelectorAll('.card').forEach(c => c.classList.remove('active'));
    
                // Toggle the 'active' class only for the clicked card
                if (!isActive) {
                    card.classList.add('active');
                }
            });
        });

        // Optional: Allow clicking outside a card to reset all cards
        document.body.addEventListener('click', (e) => {
            if (!e.target.closest('.card')) {
                document.querySelectorAll('.card').forEach(c => c.classList.remove('active'));
            }
        });

        document.addEventListener('DOMContentLoaded', () => {
            const scrollToTopBtn = document.getElementById('scroll-to-top');
            const searchContainer = document.querySelector('.search-container'); // Target the live search box

            window.addEventListener('scroll', () => {
                const searchContainerBottom = searchContainer.getBoundingClientRect().bottom;
                if (searchContainerBottom < 0) {
                    scrollToTopBtn.classList.add('visible');
                } else {
                    scrollToTopBtn.classList.remove('visible');
                }
            });

            scrollToTopBtn.addEventListener('click', () => {
                window.scrollTo({ top: 0, behavior: 'smooth' });
            });
        });

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
