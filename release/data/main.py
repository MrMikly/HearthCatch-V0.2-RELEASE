#import all libs
from time import ctime, time, sleep
from random import randint, choice
import pygame.freetype
from sys import exit
import pygame as pg
import configparser
pygame.font.init()

# colors
YELLOW = (230, 230, 0)

# textures
a = pg.image.load("assets\\backGround\\BG.00.png")
bg = pg.transform.scale(a, (500, 600))
del a

#open config(s) and log
config = configparser.ConfigParser()
config.read("config.ini")
LOG = open("log.txt", "w")
LOG.write("===================================================\n\n")
ExitCode = 0

# player config
PlayerH = int(config['PLAYER']['Height'])
PlayerW = int(config['PLAYER']['Width'])
BonusH = int(config['BONUS']['Height'])
BonusW = int(config['BONUS']['Width'])
Coins = 0

# game config
WindowH = int(config['WINDOW']['Height'])
WindowW = int(config['WINDOW']['Width'])
FPS = int(config['GAME']['MaxFPS'])
CountLife = int(config['GAME']['CountLife'])

# initializate pygame lib and root
pg.init()
root = pg.display.set_mode((WindowW, WindowH))
pg.display.set_caption("HeartCatch")

# font
FONT = pygame.font.SysFont("assets\\fonts\\Arial.ttf", 35)

# sound init
BOOM = pg.mixer.Sound('sounds\\boom.wav')
BUY = pg.mixer.Sound('sounds\\buyLife.wav')
COIN = pg.mixer.Sound('sounds\\coin.wav')
DEATH = pg.mixer.Sound('sounds\\death.wav')

MUSIC = pg.mixer.Sound('music\\ColdLake.mp3')
MUSIC.play()

# init class "Bonus"
class Bonus(pg.sprite.Sprite):
	def __init__(self):
		pg.sprite.Sprite.__init__(self)
		self.type = choice(["heart", "bomb", "coin"])
		image = pg.image.load("assets\\bonus\\" + self.type + ".png")
		self.image = pg.transform.scale(image, (BonusW, BonusH))
		self.rect = self.image.get_rect()
		self.x = randint(10, WindowW-10)
		self.y = 0-BonusH
		self.speed = randint(1, 2)

	def __str__(self):
		return "Type: %s; Image: %s; X: %d; Y: %d; Speed %d." %(self.type, self.image, self.x, self.y, self.speed)

	def update(self):
		global Coins, CountLife
		if not pg.sprite.collide_mask(self, player):
			self.rect = self.rect.move(0, self.speed)
		else:
			if self.type == "heart":
				if CountLife < 5:
					CountLife += 1
				BUY.play()
			elif self.type == "bomb":
				CountLife -= 1
				BOOM.play()
			elif self.type == "coin":
				Coins += 1
				COIN.play()
			self.kill()

		if self.y > WindowH:
			print("A")
			if self.type == "heart":
				print("B")
				CountLife -= 1
			self.kill()


class Player(pg.sprite.Sprite):
	def __init__(self):
		pg.sprite.Sprite.__init__(self)
		image = pg.image.load("assets\\player\\stand.png")
		self.image = pg.transform.scale(image, (PlayerW, PlayerH))
		self.rect = self.image.get_rect()
		self.speed = float(config['PLAYER']['Speed'])
		self.x = float(config['PLAYER']['StartX'])
		self.y = float(config['PLAYER']['StartY'])

	def __str__(self):
		return "X: %d; Y: %d" %(self.x, self.y)

	def update(self):
		pass

class Heart(pg.sprite.Sprite):
	def __init__(self):
		pg.sprite.Sprite.__init__(self)
		image = pg.image.load("assets\\heartBar\\heart.05.png")
		self.image = pg.transform.scale(image, (150, 30))
		self.rect = self.image.get_rect()

	def update(self):
		if CountLife == 0:
			DEATH.play()
			sleep(4)
			exit()
		elif CountLife == 1:
			image = pg.image.load("assets\\heartBar\\heart.01.png")
			self.image = pg.transform.scale(image, (150, 30))
		elif CountLife == 2:
			image = pg.image.load("assets\\heartBar\\heart.02.png")
			self.image = pg.transform.scale(image, (150, 30))
		elif CountLife == 3:
			image = pg.image.load("assets\\heartBar\\heart.03.png")
			self.image = pg.transform.scale(image, (150, 30))
		elif CountLife == 4:
			image = pg.image.load("assets\\heartBar\\heart.04.png")
			self.image = pg.transform.scale(image, (150, 30))
		elif CountLife >= 5:
			image = pg.image.load("assets\\heartBar\\heart.05.png")
			self.image = pg.transform.scale(image, (150, 30))
		
# rendering
def Render():
	global WalkCount
	if motion == "STOP":
		image = pg.image.load("assets\\player\\stand.png")
		player.image = pg.transform.scale(image, (PlayerW, PlayerH))
	elif motion == "RIGHT":
		WalkCount += 1
		if WalkCount == 1:
			image = pg.image.load("assets\\player\\run.right.00.png")
			player.image = pg.transform.scale(image, (PlayerW, PlayerH))
		elif WalkCount == 20:
			image = pg.image.load("assets\\player\\run.right.01.png")
			player.image = pg.transform.scale(image, (PlayerW, PlayerH))
		elif WalkCount == 40:
			image = pg.image.load("assets\\player\\run.right.02.png")
			player.image = pg.transform.scale(image, (PlayerW, PlayerH))
			WalkCount = 1
	elif motion == "LEFT":
		WalkCount -= 1
		if WalkCount == -1:
			image = pg.image.load("assets\\player\\run.left.00.png")
			player.image = pg.transform.scale(image, (PlayerW, PlayerH))
		elif WalkCount == -20:
			image = pg.image.load("assets\\player\\run.left.01.png")
			player.image = pg.transform.scale(image, (PlayerW, PlayerH))
		elif WalkCount == -40:
			image = pg.image.load("assets\\player\\run.left.02.png")
			player.image = pg.transform.scale(image, (PlayerW, PlayerH))
			WalkCount = -1

	root.blit(bg, (0,0))
	BonusList.draw(root)
	PlayerList.draw(root)
	HeartBarList.draw(root)
	root.blit(TextCoins, (0, WindowH-40))
	pg.display.flip()

# init bonus list and "out" variable for next
BonusList = pg.sprite.Group()
PlayerList = pg.sprite.Group()
HeartBarList = pg.sprite.Group()
out = False
b = 1
motion = ""
WalkCount = 0

# player add
player = Player()
PlayerList.add(player)
# bonus add
bonus = Bonus()
BonusList.add(bonus)
# heart-bar add
heartBar = Heart()
HeartBarList.add(heartBar)

# main loop
while out != True:
	for event in pg.event.get():
		if event.type == pg.QUIT:
			out = True
			ExitCode = -1
		if out:
			break
			ExitCode = 0
		##########################
		keys = pg.key.get_pressed()
		if event.type == pg.KEYDOWN:
			if keys[pg.K_RIGHT]:
				motion = "RIGHT"
			elif keys[pg.K_LEFT]:
				motion = "LEFT"
		elif event.type == pygame.KEYUP:
			motion = "STOP"
			WalkCount = 0

		if keys[pg.K_UP] and Coins >= 10:
			CountLife += 1
			Coins -= 10
			BUY.play()
		##########################
		LOG.write(ctime(time()) + ": BonusList-" + str(BonusList) + "; PlayerList-" + str(PlayerList) + "; PlayerCoords-" + str(player)+ "; ExitCode-" + str(ExitCode) + "\n\n")
		##########################
	if b == 180:
		bonus = Bonus()
		BonusList.add(bonus)
		b = 1
	else:
		b += 1

	if motion == "RIGHT":
		player.x += player.speed
	elif motion == "LEFT":
		player.x -= player.speed

	# change positions
	heartBar.rect.x = player.x - 40
	heartBar.rect.y = player.y - 50
	bonus.rect.x = bonus.x
	bonus.rect.y = bonus.y
	player.rect.x = player.x
	player.rect.y = player.y

	# render / sprite lists
	BonusList.update()
	HeartBarList.update()
	PlayerList.update()
	TextCoins = FONT.render("Coins: " + str(Coins) + " | [UP] - Buy heart by 10 coins", False, YELLOW)
	Render()

LOG.close()
pg.quit()