import os

directory_path = "~/Pictures/Wallpapers"

def wallpaper_swap():
    for item_name in os.listdir(directory_path):
        print(item_name)
