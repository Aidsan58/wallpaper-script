# Description
This is a straightforward python program that iterates through a directory of wallpapers (default: located in ~/Pictures/Wallpapers). Every time the script is called in i3 (I use a keybind that I set in i3) a new wallpaper is set. When all wallpapers have been used, it goes back to the beginning of the list. There is also a startup script that uses the last wallpaper that was set with the command.

There is also a keybind to iterate backwards through the directory of wallpapers.

You need to have feh and i3 installed, and a recent version of python.

# i3 Config
Add these lines to your i3 config. Remember to set your preferred keybind:

\#Adds feh wallpaper to startup     
exec --no-startup-id python3 ~/.config/i3/scripts/wallpaper-swap/wallpaper-script.py --startup
\#Cycles through different wallpapers     
bindsym $mod+Shift+w exec --no-startup-id python3 ~/.config/i3/scripts/wallpaper-swap/wallpaper-script.py --next
\#Cycles backwards through different wallpapers           
bindsym $mod+Ctrl+w exec --no-startup-id python3 ~/.config/i3/scripts/wallpaper-swap/wallpaper-script.py --prev
