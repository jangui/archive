import math
import turtle

def drawCircle(x, y, r):
	""""Draws a cirlce using the turtle module"""
	#move to start of circle
	turtle.up()
	turtle.setpos(x + r, y)
	turtle.down()

	#draw the circle
	for i in range(0, 365, 5):
		a = math.radians(i)
		turtle.setpos(x + r*math.cos(a), y + r*math.sin(a))

drawCircle(100, 100, 200)
turtle.mainloop()