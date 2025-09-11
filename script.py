import os
import json
import subprocess
from pathlib import Path

wallpaper_file = Path("wallpaper-list.json")
counter_file = Path("counter.txt")
directory_path = Path("~/Pictures/Wallpapers/").expanduser()

# If wallpaper list doesn't exist, creates one
if wallpaper_file.exists():
    with open(wallpaper_file, "r") as f:
        try:
            data = json.load(f)
            if "wallpapers" not in wallpaper_file:
                data = {"wallpapers": []}
        except json.JSONDecodeError: # if program has trouble parsing json file, it is written to from scratch
            data = {"wallpapers": []}
else:
    data = {"wallpapers": []}

# Adds new wallpapers if they don't already exist
valid_extensions = (".jpg", ".jpeg", ".png", ".bmp", ".webp")
for item_name in os.listdir(directory_path):
    if item_name.lower().endswith(valid_extensions):
        if item_name not in data["wallpapers"]:
            data["wallpapers"].append(item_name)

# Saves updated list
with open(wallpaper_file, "w") as f:
    json.dump(data, f, indent=4)

# Loads counter
try:
    with open(counter_file, "r") as f:
        count = int(f.read())
except FileNotFoundError:
    count = 0

wallpapers = data["wallpapers"]
if not wallpapers:
    print("No wallpapers found.")
    exit(1)

index = count % len(wallpapers)
new_wallpaper = wallpapers[index]

# Set wallpaper using feh
def set_wallpaper(wallpaper: str):
    wallpaper_path = directory_path / wallpaper
    subprocess.run(["feh", "--bg-fill", str(wallpaper_path)])

set_wallpaper(new_wallpaper)

# Save it back
count += 1
with open(counter_file, "w") as f:
    f.write(str(count))
