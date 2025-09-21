import os
import json
import subprocess
from pathlib import Path

wallpaper_file = Path("wallpaper-list.json")
counter_file = Path("counter.txt")
directory_path = Path("~/Pictures/Wallpapers/").expanduser()
bool_file = Path("bool-wallpaper.txt")

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

with open(bool_file, "r") as f:
    content = f.read().strip()
    if content == "true":
        index = (count - 1) % len(wallpapers) # wallpaper-switcher.py increments count by 1, so we revert this here so we get the same wpp
    else:
        index = (count + 1) % len(wallpapers) # wallpaper-switcher-backwards.py decrements the count by 1, so we revert this to get the same wpp


# Set wallpaper using feh
def set_wallpaper(wallpaper: str):
    wallpaper_path = directory_path / wallpaper
    subprocess.run(["feh", "--bg-fill", str(wallpaper_path)])

set_wallpaper(new_wallpaper)
