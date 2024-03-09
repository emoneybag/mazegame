import turtle
import math
import random
import time

wn = turtle.Screen()
wn.bgcolor("black")
wn.title("A Maze Game")
wn.setup(650, 650)
wn.tracer(0)

images = ["enemy_right.gif", "enemy_left.gif", "wizard_right.gif", "wizard_left.gif", "treasure.gif", "wall.gif", "door.gif", "bgpic.gif"]

for image in images:
	turtle.register_shape(image)

class Pen(turtle.Turtle):
	def __init__(self):
		turtle.Turtle.__init__(self)
		self.shape("wall.gif")
		self.color("white")
		self.penup()
		self.speed(0)

class Player(turtle.Turtle):
	def __init__(self):
		turtle.Turtle.__init__(self)
		self.shape("wizard_right.gif")
		self.color("blue")
		self.penup()
		self.speed(0)
		self.gold = 0

	def go_up(self):
		move_to_x = self.xcor()
		move_to_y = self.ycor() + 24

		if (move_to_x, move_to_y) not in walls:
			self.goto(self.xcor(), self.ycor() + 24)

	def go_down(self):
		move_to_x = self.xcor()
		move_to_y = self.ycor() - 24

		if (move_to_x, move_to_y) not in walls:
			self.goto(self.xcor(), self.ycor() - 24)

	def go_left(self):
		move_to_x = self.xcor() - 24
		move_to_y = self.ycor()
		self.shape("wizard_left.gif")

		if (move_to_x, move_to_y) not in walls:
			self.goto(self.xcor() - 24, self.ycor())

	def go_right(self):
		move_to_x = self.xcor() + 24
		move_to_y = self.ycor()
		self.shape("wizard_right.gif")

		if (move_to_x, move_to_y) not in walls:
			self.goto(self.xcor() + 24, self.ycor())

	def is_collision(self, other):
		a = self.xcor() - other.xcor()
		b = self.ycor() - other.ycor()
		distance = math.sqrt((a ** 2) + (b ** 2))

		if distance < 5:
			return True
		else:
			return False

class Treasure(turtle.Turtle):
	def __init__(self, x, y):
		turtle.Turtle.__init__(self)
		self.shape("treasure.gif")
		self.color("gold")
		self.penup()
		self.speed(0)
		self.gold = 100
		self.goto(x, y)

	def destroy(self):
		self.goto(2000, 2000)
		self.hideturtle()

class Enemy(turtle.Turtle):
	def __init__(self, x, y):
		turtle.Turtle.__init__(self)
		self.shape("enemy_right.gif")
		self.color("red")
		self.penup()
		self.speed(0)
		self.gold = 25
		self.goto(x, y)
		self.direction = random.choice(["up", "down", "left", "right"])

	def move(self):
		if self.direction == "up":
			dx = 0
			dy = 24
		if self.direction == "down":
			dx = 0
			dy = -24
		if self.direction == "left":
			dx = -24
			dy = 0
			self.shape("enemy_left.gif")
		if self.direction == "right":
			dx = 24
			dy = 0
			self.shape("enemy_right.gif")
		if self.is_close(player):
			if player.xcor() < self.xcor():
				self.direction = "left"
			if player.xcor() > self.xcor():
				self.direction = "right"
			if player.ycor() < self.ycor():
				self.direction = "down"
			if player.ycor() > self.ycor():
				self.direction = "up"

		move_to_x = self.xcor() + dx
		move_to_y = self.ycor() + dy

		if (move_to_x, move_to_y) not in walls:
			self.goto(move_to_x, move_to_y)

		else:
			self.direction = random.choice(["up", "down", "left", "right"])

		turtle.ontimer(self.move, t=random.randint(100, 300))

	def is_close(self, other):
		a = self.xcor() - other.xcor()
		b = self.ycor() - other.ycor()
		distance = math.sqrt((a ** 2) + (b ** 2))

		if distance < 75:
			return True
		else:
			return False

	def destroy(self):
		self.goto(2000, 2000)
		self.hideturtle()

class Door(turtle.Turtle):
	def __init__(self, x, y):
		turtle.Turtle.__init__(self)
		self.shape("door.gif")
		self.color("brown")
		self.penup()
		self.speed(0)
		self.goto(x, y)

levels = [""]

level_1 = [
"XXXXXXXXXXXXXXXXXXXXXXXXX",
"XP XXXXXXXE         XXXXX",
"X  XXXXXXX  XXXXXX  XXXXX",
"X           XXXXXX  XXXXX",
"X           XXX       EXX",
"XXXXXX      XXXT       XX",
"XXXXXX      XXXXXXXXXXXXX",
"XXXXXX        XXXXXXXXXXX",
"XXXXXX        XXXXXXXXXXX",
"XXXXXX   XXXXXXXXXXXXXXXX",
"X        XXXXXXXXXXXXXXXX",
"X                       X",
"XXXXXXXXXXXXXXX         X",
"XXXXXXXXXXXXXXX         X",
"XXX  XXXXXXXXXX         X",
"XXXE                    X",
"XXX         XXXXXXXXXXXXX",
"XXXXXXXXXX  XXXXXXXXXXXXX",
"XXXXXXXXXX              X",
"XX  TXXXXX              X",
"XX   XXXXXXXXXXXXX  XXXXX",
"XX    XXXXXXXXXXXX  XXXXX",
"XX          XXXX        D",
"XXXXE                   X",
"XXXXXXXXXXXXXXXXXXXXXXXXX"
]

level_2 = [
"XXXXXXXXXXXXXXXXXXXXXXXXX",
"XXXXXXXXXX          XXXXX",
"XXXXXXXXXX  XXXXXX  XXXXX",
"X           XXXXXX  XXXXX",
"D           XXX       EXX",
"XXXXXX      XXX        XX",
"XXXXXX      XXX        XX",
"XXXXXX      XXX        XX",
"XXXXXX      XXX   T    XX",
"XXXXXX    XXXXXXXXXXXXXXX",
"XE        XXXXXXXXXXXXXXX",
"X                 XXXXXXX",
"XXXXXXXXXXXXXXX         X",
"XXXXXXXXXXXXXXX         X",
"XXXXXXXXXXXXXXXXXXXXXX  X",
"XXXE                    X",
"XXXT                    X",
"XXXXXXXXXX    XXXXXXXXXXX",
"XXXXXXXXXX              X",
"XX   XXXXX             EX",
"XX   XXXXXXXXXXXX   XXXXX",
"XX   XXXXXXXXXXXX   XXXXX",
"XXP                    TX",
"XX                      X",
"XXXXXXXXXXXXXXXXXXXXXXXXX"
]

treasures = []
doors = []
enemies = []
walls = []

pen = Pen()
player = Player()

levels.append(level_1)
levels.append(level_2)

def setup_maze(level):
	for y in range(len(level)):
		for x in range(len(level[y])):
			character = level[y][x]
			screen_x = -288 + (x * 24)
			screen_y = 288 - (y * 24)
			if character == "X":
				pen.goto(screen_x, screen_y)
				pen.stamp()
				walls.append((screen_x, screen_y))
			if character == "P":
				player.goto(screen_x, screen_y)
				print(screen_x, screen_y)
			if character == "T":
				treasures.append(Treasure(screen_x, screen_y))
			if character == "E":
				enemies.append(Enemy(screen_x, screen_y))
			if character == "D":
				doors.append(Door(screen_x, screen_y))

setup_maze(levels[1])

wn.listen()
wn.onkey(player.go_left, "Left")
wn.onkey(player.go_right, "Right")
wn.onkey(player.go_up, "Up")
wn.onkey(player.go_down, "Down")

for enemy in enemies:
	turtle.ontimer(enemy.move, t=250)

while True:

	for treasure in treasures:
		if player.is_collision(treasure):
			player.gold += treasure.gold
			print("Player Gold: {}".format(player.gold))
			treasure.destroy()
			treasures.remove(treasure)

	for enemy in enemies:
		if player.is_collision(enemy):
			print("Player dies!")
			answer = input("Do you wish to retry? (y/n) : ")
			if answer in ["Y", "y"]:
				answer = "y"
			if player.gold <= 0 or answer in ["N", "n"]:
				answer = "n"
			if answer == "y":
				for enemy in enemies:
					enemy.destroy()
				for treasure in treasures:
					treasure.destroy()
				setup_maze(levels[1])
				for enemy in enemies:
					enemy.move()
				player.gold = 0
			else:
				quit()
		
	for door in doors:
		if player.is_collision(door):
			print("Level Advance")
			time.sleep(1)
			wn.clear()
			wn.bgcolor("black")
			wn.tracer(0)
			for enemy in enemies:
				enemy.destroy()
			for treasure in treasures:
				treasure.destroy()
			levels.remove(level_1)
			setup_maze(levels[1])
			for enemy in enemies:
				enemy.move()
			player.showturtle()

	wn.update()

wn.mainloop()