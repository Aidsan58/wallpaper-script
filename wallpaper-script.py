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

def save_counter(count: int):
    with open(counter_file, "w") as f:
        f.write(str(count))

def load_direction() -> str:
    if not bool_file.exists():
        with open(bool_file, "w") as f:
            f.write("true")
        return "true" # We need a return value even if the file doesn't exist yet, and we default to true
    with open(bool_file, "r") as f:
        return f.read().strip()

def save_direction(direction: str):
    with open(bool_file, "w") as f:
        f.write(direction)

def set_wallpaper(filename: str):
    wallpaper_path = directory_path / filename
    subprocess.run(["feh", "--bg-fill", str(wallpaper_path)])

def main():
    parser = argparse.ArgumentParser(description="Wallpaper switcher")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--next", action="store_true", help="Set next wallpaper")
    group.add_argument("--prev", action="store_true", help="Set previous wallpaper")
    group.add_argument("--startup", action="store_true", help="Set wallpaper on startup")

    args = parser.parse_args()
    wallpapers = load_wallpaper_list()

    if not wallpapers:
        print("No wallpapers found.")
        return
    
    count = load_counter()
    direction = load_direction()

    if args.next:
        index = count % len(wallpapers)
        save_direction("true")
        set_wallpaper(wallpapers[index])
        save_counter(count + 1)

    elif args.prev:
        index = (count - 1) % len(wallpapers)
        save_direction("false")
        set_wallpaper(wallpapers[index])
        save_counter(max(count - 1, 0))

    elif args.startup:
        if direction == "true":
            index = (count - 1) % len(wallpapers)
        else:
            index = (count + 1) % len(wallpapers)
        set_wallpaper(wallpapers[index])

if __name__ == "__main__":
    main()
