import os
import json
from pathlib import Path

wallpaper_file = Path("wallpaper-list.json")
directory_path = "~/Pictures/Wallpapers/"
counter_file = Path("counter.txt")

# Read the current value
try:
    with open(counter_file, "r") as f:
        count = int(f.read())
except FileNotFoundError:
    count = 0  # If file doesn't exist

def run_i3_command(wallpaper: str):
    import subprocess
    command = f"feh --bg-fill {directory_path}{wallpaper}"
    subprocess.run(["i3-msg", command])

def wallpaper_add():
    with open(wallpaper_file, "r+") as f: # Adds item to json file unless item already in json file
        for item_name in os.listdir(directory_path):
            if item_name in wallpaper_file:
                continue
            else:
                json.dump(item_name, f)

        data = json.loads(wallpaper_file)
        try:
            new_wallpaper = data["wallpapers"].index[count]
        except IndexError:
            count = 0
            new_wallpaper = data["wallpapers"].index[count]
        # Increment the value
        count += 1
        return new_wallpaper, count


wallpaper_add()
run_i3_command(new_wallpaper)

# Save it back
with open(counter_file, "w") as f:
    f.write(str(count))
