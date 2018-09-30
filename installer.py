#!/usr/bin/python3

import os
import sys

try:
	import pyglet
except ImportError:
	print("Pyglet is required to run Martians Attack!")
	want = input("Do you want to install pyglet [y/n]? ")
	if want:
		os.system("pip3 install pyglet --user")
	else:
		sys.exit(1)

print("Installing martians attack...")

home = os.getenv("HOME")
dirname = os.path.dirname(os.path.realpath(__file__))

if not os.path.exists(os.path.join(home + "/bin")):
	os.makedirs(os.path.join(home + "/bin"))

with open(home + "/bin/martians-attack", "w+") as f:
	os.system("touch " + dirname + "/main.py")
	f.write("#!/bin/sh\npython3 " + dirname + "/main.py")
	os.system("chmod 755 " + home + "/bin/martians-attack")

print("Installed!\n\nUsage:\nmartians-attack\n")

desktop = input("Do you want to add Martians Attack to your desktop [y/n]? ") == "y"

if desktop:
	os.system("touch " + home + "/Desktop/martians-attack.desktop")
	with open(home + "/Desktop/martians-attack.desktop", "w+") as f:
		f.write("[Desktop Entry]\nType=Application\nName=Martians Attack\nGenericName=Martians Attack\nComment=Martians Attack\nExec=martians-attack\nIcon=" + dirname + "/res/enemy.png" + "\nTerminal=false\nCategories=Games;\nKeywords=martians")

print("\nFinished!")
