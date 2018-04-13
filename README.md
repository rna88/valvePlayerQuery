# Valve Player Query
This python script will show notifications of increasing online player count for multiplayer games hosted with the valve master server. This is only useful for games with a low player count that have sporadic activity; you can be informed when people are playing without leaving the game running or needing to check a website.

## Usage for Linux
### Dependencies
You will specifically need [libnotify], [python-valve], and [psutil]. The other modules should come with a default python install:
```
sudo pacman -S libnotify (use your distro's package manager)
sudo pip install python-valve
sudo pip install psutil
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
Demonstrating "daemonized" usage for Fistful of Frags:

`setsid python valvePlayerQuery.py fof 20 10 3 >/dev/null 2>&1`

## Usage for other OS's
Everything besides the notification library is cross-platform. The notification lib could be replaced with pyQT to make it completely cross-platform, otherwise you'll have to settle for looking at the output in a terminal.

## License
This repository is licensed under the [MIT License](LICENSE)

[python-valve]: (https://github.com/serverstf/python-valve)
[psutil]: (https://github.com/giampaolo/psutil)
[libnotify]: (https://wiki.archlinux.org/index.php/Desktop_notifications#Libnotify)
