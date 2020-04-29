import pygame as game
import random
from pygame import mixer


#initialize
game.init()

#background 
screen = game.display.set_mode((600,600))

#background music
mixer.music.load("sounds\\BlankSpace.mp3")
mixer.music.play(-1)

#title and icon 
game.display.set_caption("flappy")
icon = game.image.load("assets\\game.png")
game.display.set_icon(icon)

#player 
player = game.image.load("assets\\game.png")
playerX = random.randint(200,250)
playerY = random.randint(300,410)

def resetPlayer():
	# reset player 
	playerX = random.randint(200,250)
	playerY = random.randint(300,410)

def drawPlayer():
	# display player image
	screen.blit(player,(playerX,playerY))

# object or buildings
building = game.image.load("assets\\object.png")
buildings = [(400,321),(800,350)]

def resetBuildings():
	# reset all building or objects
	count = 0
	x = 0
	for build in buildings:
		x += 400
		buildings[count] = (x,random.randint(321,360))
		count += 1

def hitted():
	# returns True if the player is hitted by object
	for (x,y) in buildings:
		if (x <= (playerX+15) <= (x+50)) and (y <= (playerY+15) <= (y+100)):
			return True


def drawBuildings():
	# draws object or buildings
	for build in buildings:
		screen.blit(building, build)

def updateBuilding():
	# updates objects or buildings
	cnt = 0
	for (x,y) in buildings:
		x -= 3
		buildings[cnt] = (x,y)
		if x <= -50:
			buildings[cnt] = (random.randint(800,900),random.randint(321,360))
		cnt += 1

#background work

bg = game.image.load("assets\\bg.png")
gr = game.image.load("assets\\ground.png")
cloudImg = game.image.load("assets\\cloud.png")
text = game.font.Font("freesansbold.ttf",20)

clouds = [(100,100),(400,50),(500,70),(600,89),(250,46)]
speed = [0.3,0.24,0.4,0.5,0.3]

def shScore(score_value):
	# shows score on screen
	score = text.render(f"Score: {int(score_value)}",True,(0,0,200))
	screen.blit(score,(10,10))	

def setBG():
	# displays the background image
	screen.blit(bg, (0,0))

def setClouds():
	# Set Clouds
	for cloud in clouds:
		screen.blit(cloudImg, cloud)

def setGround():
	# displays the ground image 
	screen.blit(gr, (0,421))

def updateClouds():
	# updates clouds
	current = 0
	for (x,y) in clouds:
		x -= speed[current]
		clouds[current] = (x,y)
		if x <= (-80):
			clouds[current] = (random.randint(600,700),random.randint(0,150))
		current += 1 

def checkGround():
	# returns True if the player is on the ground and if not then return False
	return True if playerY > 395 else False

#warning

paused = game.image.load("assets\\paused.png")
warning = game.image.load("assets\\warning.png")

def hitSound():
	# produce sound if player hits the object
	hit_sound = mixer.Sound("sounds\\hit.wav")
	hit_sound.play()

def jumpSound():
	# produce sound if player jumps
	jump_sound = mixer.Sound("sounds\\jump.wav")
	jump_sound.play()

def shWarning():
	# display warning
	screen.blit(warning, (200,150))

def shPaused():
	# display paused screen 
	screen.blit(paused,(200,150))

#main gameloop
def reset():
	# reset all data and objects
	resetPlayer()
	resetBuildings()

gameOver = False
onGround = False
gravity = 2
jump = 0
gamePause = False
score = 0
running = True
warningAppeared = False


while not gameOver and running:
	# 1. Display background
	setBG()	
	# 2. Display buildings 
	drawBuildings()
	# 3. Display Ground
	setGround()
	# 4. Display Player
	drawPlayer()
	# 5. Display Score
	shScore(score)

	# 6. Display Warning and take choice from user and Produce hit sound
	if hitted():
			if not warningAppeared:
				hitSound()
			gamePause = True
			warningAppeared = True	
			shWarning()	
	elif gamePause:
		# 7. If Game is paused show Pause menu
		shPaused()

	# 8. Display Clouds
	setClouds()

	# 9. Update Clouds
	updateClouds()

	# 9. Update Frames
	game.display.update()

	# Check for events during the gameloop
	for event in game.event.get():

		# Check if window is closed
		if event.type == game.QUIT:
			running = False

		# Check if any key is pressed
		if event.type == game.KEYDOWN:

			# If SPACE key event is occured then jump and produce jump sound
			if event.key == game.K_SPACE and not gamePause:
				if onGround:
					jumpSound()
					jump = 20

			# If ESCAPE event is occured then show the pause screen menu
			if event.key == game.K_ESCAPE and not warningAppeared:		
				gamePause = not gamePause
				
			# If N key event is occured on PAUSE or on GAME OVER menu then exit the gameloop
			if event.key == game.K_n and gamePause:
				gameOver = True
				continue

			# If Y key event is occured on PAUSE or on GAME OVER menu then reset player and objects 
			if event.key == game.K_y and gamePause: 
				reset()
				score = 0
				gamePause = False
				warningAppeared = False
	
	# If Game is Paused then skip ground check and objects position updation
	if not gamePause:
		onGround = checkGround()
		playerY -= jump
		if jump > 0:
			jump -= 1

		# adjust Player posistion according to the Gravity if Player is not on ground
		if not onGround:
			playerY += gravity	
			gravity += 0.13
		else:
			gravity = 2

		# Update Score
		score += 0.01
		
		# Update Buildings
		updateBuilding()