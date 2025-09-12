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
            if "wallpapers" not in data:
                data = {"wallpapers": []}
        except json.JSONDecodeError: # If program has trouble parsing json file, it is written to from scratch
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
try:
    with open(wallpaper_file, "w") as f:
        json.dump(data, f, indent=4)
except Exception as e:
    print(f"Failed to write wallpaper list: {e}") # If program fails to write

# Loads counter
def load_counter(counter_path: Path) -> int:
    try:
        with open(counter_path, "r") as f:
            content = f.read().strip()
            if content:
                return int(content)
            else:
                raise ValueError("Counter file is empty.")
    except (FileNotFoundError, ValueError) as e:
        print(f"Repairing counter.txt: {e}")
        with open(counter_path, "w") as f:
            f.write("0")
        return 0

count = load_counter(counter_file)

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
