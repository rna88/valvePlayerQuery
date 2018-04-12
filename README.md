# Valve Player Query
This python script will show notifications of increasing online player count for multiplayer games hosted with the valve master server. This is only useful for games with a low player count that have sporadic activity; you can be informed when people are playing without leaving the game running or needing to check a website.

## Usage for Linux
### Dependencies
You will need [python-valve], [libnotify], and of course the python 2 or 3 packages installed.
```
sudo pip install python-valve
sudo pacman -S libnotify
```

### Running
Basic usage: 

`python valvePlayerQuery <gamedir> <minPlayers> <refreshRate> <retries>`

`<gamedir>`       The ID string of the game, found by searching https://steamdb.info for the game, and looking under "Information"  
`<minPlayers>`    Minimum player count before we display notification  
`<refreshRate>`   Minutes before querying the master server again  
`<retries>`       Number of times to retry connecting to the master server on timeout  

Optionally you may place a small image called <gamedir>.png in the same location as the script. This image will appear on the notification, allowing you to easily identify different notifications for different games.

### Example
Demonstrating usage for fistful of frags:

`setsid python valvePlayerQuery.py fof 20 10 3 >/dev/null 2>&1`

## License
This repository is licensed under the [MIT License](LICENSE)

[python-valve]: (https://github.com/serverstf/python-valve)
[libnotify]: (https://wiki.archlinux.org/index.php/Desktop_notifications#Libnotify)
