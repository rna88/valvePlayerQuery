import subprocess
import gi
gi.require_version('Notify', '0.7')
from gi.repository import Notify, GdkPixbuf
import valve.source.master_server
import time
import socket
import os
import sys

totalPlayers = 0
lastPlayers = 0
timeout = 0

if len(sys.argv) < 5:
	print("Usage: python valvePlayerQuery <gamedir> <minPlayers> <refreshRate> <retries>\n\n"
	+"<gamedir>       The ID string of the game, found by searching https://steamdb.info for the game, and looking under \"Information\"\n"
	+"<minPlayers>    Minimum player count before we display notification\n"
	+"<refreshRate>   Minutes before querying the master server again\n"
	+"<retries>       Number of times to retry connecting to the master server on timeout")
	sys.exit()

gameDir = sys.argv[1]
minPlayers = int(sys.argv[2])
refreshRate = int(sys.argv[3])
retries = int(sys.argv[4])

Notify.init("valvePlayerQuery")
notifyPlayers = Notify.Notification.new("You shouldn't be seeing this")
notifyTimeout = Notify.Notification.new("Timeout")

# Use a custom image for the notifications if we find one. 
if os.path.isfile(gameDir+".png"):
	image = GdkPixbuf.Pixbuf.new_from_file(gameDir+".png")
	notifyPlayers.set_icon_from_pixbuf(image)
	notifyPlayers.set_image_from_pixbuf(image)
	notifyTimeout.set_icon_from_pixbuf(image)
	notifyTimeout.set_image_from_pixbuf(image)
else:
	image = GdkPixbuf.Pixbuf.new_from_file("default.png")
	notifyPlayers.set_icon_from_pixbuf(image)
	notifyPlayers.set_image_from_pixbuf(image)
	notifyTimeout.set_icon_from_pixbuf(image)
	notifyTimeout.set_image_from_pixbuf(image)

while True:
	# Check if the game is running, if it is don't bother displaying a notification.
	playing = subprocess.call("ps -ef | grep "+gameDir+" | grep -vE '$$|"+sys.argv[0]+"'",stderr=subprocess.STDOUT,shell=True) 
	
	if playing == 1:
		msq = valve.source.master_server.MasterServerQuerier()
		try:
			for address in msq.find(region=[u"na", u"eu", u"sa", u"as",u"oc",u"af"], gamedir = gameDir):
				server = valve.source.a2s.ServerQuerier(address)
				info = server.get_info()["server_name"]
				playerCount  = server.get_players()["player_count"]
				try:
					playerCount
				except NameError:
					playercount = 0
				print(playerCount, info)
				totalPlayers += playerCount
			timeout = 0

		# Try reconnecting n times, if unsuccessful show timeout notification and sleep until next cycle.
		except (valve.source.a2s.NoResponseError, socket.error) as e:
			timeout += 1
			# Player count is reset on timeout for next request.
			playerCount = 0
			if timeout >= retries:
				notifyTimeout.show()
				print("Master server request timed out!")
				timout = 0
				time.sleep(refreshRate*60)
			continue

	if (totalPlayers >= minPlayers) & (totalPlayers != lastPlayers):
		lastPlayers = totalPlayers
		notifyPlayers.update( str(totalPlayers) + " online")
		notifyPlayers.show()
		totalPlayers = 0
	else: 
		pass

	time.sleep(refreshRate*60)	# convert refreshRate to seconds and sleep.
