from tkinter import *
import random



GAME_WIDTH = 600
GAME_HEIGHT= 600
SPEED = 50
SPACE_SIZE = 25
BODY_PARTS = 3
snek_COLOR = "#FFFFFF"
FOOD_COLOR = ["#FF0000",'#FFC300',"#C70039","#DAF7A6","#33ffcd"]


BACKGROUND_COLOR = "#000000"

class sneks:
	def __init__(self):
		self.body_sz=BODY_PARTS
		self.coordinate=[]
		self.square=[]
		#generate the snek

		for i in range(0,BODY_PARTS):
			self.coordinate.append([0,0])

		for x,y in self.coordinate:
			squares= canvas.create_rectangle(x,y, x + SPACE_SIZE, y + SPACE_SIZE, fill =snek_COLOR, tag="snek")
			self.square.append(squares)

class foods:
	def __init__(self):

		x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
		y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE
		#food chng color
		new_fodcol=random.choice(FOOD_COLOR)
		self.coordinate=[x,y]
		

		canvas.create_oval(x,y, x + SPACE_SIZE,y + SPACE_SIZE, fill=new_fodcol, tag="food")


def snek_move(snek,food):
	x,y=snek.coordinate[0]

	if direction == "up":
		y -= SPACE_SIZE
	elif direction == "down":
		y += SPACE_SIZE
	elif direction == "left":
		x -= SPACE_SIZE
	elif direction == "right":
		x += SPACE_SIZE

	snek.coordinate.insert(0,(x,y))

	square=canvas.create_rectangle(x,y, x + SPACE_SIZE, y + SPACE_SIZE, fill=snek_COLOR)
	snek.square.insert(0,square)

	#eating the food
	if x == food.coordinate[0] and y == food.coordinate[1]:
		#add score
		global score
		score += 1
		label.config(text="score:{}".format(score))
		canvas.delete("food")
		food=foods()
	else:
		#delete extra body parts
		del snek.coordinate[-1]
		canvas.delete(snek.square[-1])
		del snek.square[-1]

	if collision_chk(snek):
		game_over()
	else:
		#snek speed
		window.after(SPEED,snek_move,snek,food)
	
#snek move
def chng_direct(new_direction):
	global direction

	if new_direction == 'left':
		if new_direction != 'right':
			direction = new_direction 
	elif new_direction == 'right':
		if new_direction != 'left':
			direction = new_direction 
	elif new_direction == 'up':
		if new_direction != 'down':
			direction = new_direction
	elif new_direction == 'down':
		if new_direction != 'up':
			direction = new_direction  

#chck snek collision
def collision_chk(snek):
	#collison in border
	x,y=snek.coordinate[0]

	if x < 0 or x >= GAME_WIDTH:
		return True
	elif y < 0 or y >= GAME_WIDTH:
		return True
	#collision in body part
	for body_part in snek.coordinate[1:]:
		if x == body_part[0] and y == body_part[1]:
			return True

	return False

def game_over():
	canvas.delete("all")
	#show text
	canvas.create_text(canvas.winfo_width()/2,canvas.winfo_height()/2,
						font=('verdana',50),text="GAME OVER!",fill="red",
						tag="gameover")
	p=canvas.create_text(canvas.winfo_width()/2,canvas.winfo_height()/2,
						font=('verdana',20),text="pressed space bar to restart",
						fill="green",
						tag="gameover")
	canvas.moveto(p, x=100, y=0)

	#presed to restart game
	window.bind('<space>',lambda event: game_restart())


#restart game
def game_restart():
	global snek,food,score,direction
	canvas.delete("all")
	snek=sneks()
	food=foods()
	score=0
	direction='down'
	label.config(text="score:{}".format(score))
	snek_move(snek,food)
	

#crete window
window = Tk()
window.title("snek game")
window.resizable(False,False)

score = 0
direction = 'down'

label = Label(window, text="score:{}".format(score), font=('verdana',45))
label.pack()

canvas=Canvas(window,bg=BACKGROUND_COLOR,height=GAME_HEIGHT,width=GAME_WIDTH)
canvas.pack()

#center window when open
window.update()
window_width=window.winfo_width()
window_height=window.winfo_height()
screen_width=window.winfo_screenwidth()
screen_height=window.winfo_screenheight()

x=int((screen_width/2)-(window_width/2))
y=int((screen_height/2)-(window_height/2))
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

#keys
window.bind('<Left>',lambda event: chng_direct('left'))
window.bind('<Right>',lambda event: chng_direct('right'))
window.bind('<Up>',lambda event: chng_direct('up'))
window.bind('<Down>',lambda event: chng_direct('down'))


snek=sneks()
food=foods()
snek_move(snek,food)

window.mainloop()
