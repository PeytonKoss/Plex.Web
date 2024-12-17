import os

# Path to the images folder
images_folder = 'path/to/images'  # Replace with the actual path

# Iterate through all files in the folder
for file in os.listdir(images_folder):
    if file.endswith(".thumb.jpg"):  # Ensure it's a thumb image
        # Extract the ratingKey from the filename (assuming it’s in the format 'Title [ratingKey].thumb.jpg')
        try:
            rating_key = file.split("[")[-1].split("]")[0]  # Extract text between [ ]
            new_filename = f"{rating_key}.thumb.jpg"
            
            # Rename the file
            old_path = os.path.join(images_folder, file)
            new_path = os.path.join(images_folder, new_filename)
            os.rename(old_path, new_path)
            print(f"Renamed: {file} -> {new_filename}")
        except IndexError:
            print(f"Skipping file (couldn't extract ratingKey): {file}")

print("Renaming complete!")
