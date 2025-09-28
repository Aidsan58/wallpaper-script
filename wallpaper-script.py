import os
import json
import subprocess
import argparse 
from pathlib import Path
# Added parse library for custom command line arguments, necessary for the different inputs we will have
# subprocess is for interacting with the command line

# Config
wallpaper_file = Path("wallpaper-list.json")
counter_file = Path("counter.txt")
directory_path = Path("~/Pictures/Wallpapers/").expanduser()
bool_file = Path("bool-wallpaper.txt")
valid_extensions = (".jpg", ".jpeg", ".png", ".bmp", ".webp") # These are the valid file extensions for wallpapers, any others will be ignored

# If wallpaper list doesn't exist, creates one
def load_wallpaper_list() -> list[str]:
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
    
    return [wp for wp in data["wallpapers"] if (directory_path / wp).exists()] # checks to make sure file exists

# Loads counter
def load_counter() -> int:
    try:
        with open(counter_file, "r") as f:
            return int(f.read().strip()) # Returns what will be used as the counter index            
    except (FileNotFoundError, ValueError) as e:
        print(f"Repairing counter.txt: {e}")
        with open(counter_file, "w") as f:
            f.write("0")
        return 0
