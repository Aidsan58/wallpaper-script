import os

def run_i3_command(wallpaper: str):
    import subprocess
    command = f"feh --bg-fill {directory_path}{wallpaper}"
    subprocess.run(["i3-msg", command])

directory_path = "~/Pictures/Wallpapers/"

def wallpaper_swap():
    for item_name in os.listdir(directory_path):
        print(item_name)


