#!/usr/bin/python3

import os
import time
from random import randint as random
import sys
from threading import Thread

try:
	import pyglet
	from pyglet.window import key
	from pyglet.window import mouse
except ImportError:
	print("Pyglet is required to run Martians Attack!")
	sys.exit(1)
try:
	import vlc
	vlci = vlc.Instance("--input-repeat=999999")
	vlcp = vlci.media_player_new(os.path.join(os.path.dirname(os.path.realpath(__file__)), "res/music.mp3"))
	vlcp.play()
except ImportError:
	print("python-vlc is not installed, music will not be played in background!")
	class vlcp:
		def stop(*argvs, **kwargs):
			pass

def restart():
	os.execvp("martians-attack", sys.argv)

window = pyglet.window.Window(width=1104, height=720, caption="Martians Attack")

pyglet.resource.path = ["res"]

player_image = pyglet.resource.image("player.png")
player_image.width = 48
player_image.height = 48
bullet_image = pyglet.resource.image("bullet.png")
enemy_image = pyglet.resource.image("enemy.png")
enemy_image.width = 40
enemy_image.height = 40

playerIsAlive = True
enemiesMoved = False
score = 0
enemySpeed = 1
gun = "pistol"
won = False

player = pyglet.sprite.Sprite(player_image, x=0, y=0)
playerDied = pyglet.text.Label(text="You died!", color=[255, 0, 0, 150], bold=True, x=window.width//2, y=window.height//2, anchor_x="center", anchor_y="center", font_size=100)
playerDiedInfo = pyglet.text.Label(text="Press any key to restart", color=[255, 0, 0, 150], x=window.width//2, y=window.height//2 - 100, anchor_x="center", anchor_y="center", font_size=50)
playerWon = pyglet.text.Label(text="You won!", color=[0, 255, 0, 150], bold=True, x=window.width//2, y=window.height//2, anchor_x="center", anchor_y="center", font_size=100)
playerWonInfo = pyglet.text.Label(text="Press any key to restart", color=[0, 255, 0, 150], x=window.width//2, y=window.height//2 - 100, anchor_x="center", anchor_y="center", font_size=50)
bullets = []
enemies = []

@window.event
def on_close():
	vlcp.stop()

@window.event
def on_mouse_press(x, y, button, modifiers):
	if button == mouse.LEFT:
		pass
	elif button == mouse.RIGHT:
		pass

@window.event
def on_key_press(symbol, modifiers):
	global playerIsAlive
	global won
	if playerIsAlive and not won:
		if symbol == key.W or symbol == key.UP or symbol == key.I:
			if player.y < window.height - 48:
				player.y += 48
		elif symbol == key.A or symbol == key.LEFT or symbol == key.J:
			if player.x > 47:
				player.x -= 48
		elif symbol == key.S or symbol == key.DOWN or symbol == key.K:
			if player.y > 47:
				player.y -= 48
		elif symbol == key.D or symbol == key.RIGHT or symbol == key.L:
			if player.x < window.width - 48:
				player.x += 48
		elif symbol == key.SPACE or symbol == key.LSHIFT or symbol == key.RSHIFT or symbol == key.ENTER:
			if gun == "pistol":
				bullets.append(pyglet.sprite.Sprite(bullet_image, player.x + 16, player.y + 48))
			elif gun == "shotgun":
				bullets.append(pyglet.sprite.Sprite(bullet_image, player.x + 16, player.y + 48))
				bullets.append(pyglet.sprite.Sprite(bullet_image, player.x + 32, player.y + 48))
				bullets.append(pyglet.sprite.Sprite(bullet_image, player.x, player.y + 48))
			elif gun == "shotgun+":
				bullets.append(pyglet.sprite.Sprite(bullet_image, player.x + 16, player.y + 48))
				bullets.append(pyglet.sprite.Sprite(bullet_image, player.x + 32, player.y + 48))
				bullets.append(pyglet.sprite.Sprite(bullet_image, player.x, player.y + 48))
				bullets.append(pyglet.sprite.Sprite(bullet_image, player.x - 16, player.y + 48))
				bullets.append(pyglet.sprite.Sprite(bullet_image, player.x + 48, player.y + 48))
		elif symbol == key.ESCAPE:
			vlcp.stop()
			sys.exit(0)
	elif not playerIsAlive or won:
		restart()

@window.event
def on_draw():
	global score
	global enemySpeed
	window.clear()
	if playerIsAlive and not won:
		player.draw()
		for bullet in bullets:
			if bullet.y < 1081:
				bullet.draw()
		for enemy in enemies:
			if not enemy.died and not enemy.y < 0:
				enemy.draw()
		scoreLabel = pyglet.text.Label(text="Score: " + str(score), color=[255, 255, 255, 100], x=10, y=10, anchor_x="left", anchor_y="bottom", font_size=20)
		scoreLabel.draw()
	elif not playerIsAlive and not won:
		playerDied.draw()
		playerDiedInfo.draw()
	elif won:
		playerWon.draw()
		playerWonInfo.draw()
	enemySpeed += 0.0002

def update(*argvs, **kwargs):
	global playerIsAlive
	global enemiesMoved
	global gun
	global won
	for bullet in bullets:
		bullet.y += 15
	def rembullets():
		i = 0
		bad = False
		for bullet in bullets:
			if bullet.y > 1100:
				bullets.pop(i)
				bad = True
				break
		if bad:
			rembullets()
	rembullets()
	for bullet in bullets:
		for enemy in enemies:
			if abs(bullet.y - enemy.y) < 10 and abs(bullet.x - enemy.x) < 24:
				enemy.died = True
	def remenemies():
		global score
		i = 0
		bad = False
		for enemy in enemies:
			if enemy.died:
				enemies.pop(i)
				bad = True
				score += 1
				break
		if bad:
			remenemies()
	remenemies()
	if enemiesMoved:
		enemiesMoved = False
	else:
		enemiesMoved = True
	for enemy in enemies:
		if not enemiesMoved:
			enemy.y -= enemySpeed
		if enemy.y < 0:
			if not won:
				playerIsAlive = False
	if score >= 50 and not gun == "shotgun":
		gun = "shotgun"
	if score >= 100 and not gun == "shotgun+":
		gun = "shotgun+"
	if score >= 150:
		won = True

def createEnemies(*argvs, **kwargs):
	enemiesl = len(enemies)
	enemies.append(pyglet.sprite.Sprite(enemy_image, random(0, 1040), 700))
	enemies[enemiesl].died = False

pyglet.clock.schedule_interval(update, 0.01)
pyglet.clock.schedule_interval(createEnemies, 2)

pyglet.app.run()

