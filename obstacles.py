#! /usr/bin/python
from visual import box, color, rate, scene, sphere, vector

INFINITY = float('infinity')

LENGTH = 1000
WIDTH = LENGTH

RADIUS = 10
DIAMETER = RADIUS + RADIUS

scene.title = 'Obstacles'
scene.fullscreen = True
scene.forward = (0, -0.25, -0.5)
scene.center = vector(WIDTH / 2, 0, LENGTH  / 2)

box(pos = vector(WIDTH / 2, 0, LENGTH  / 2), width = WIDTH, height = 0.1,
	length = LENGTH, color = color.white)
BALL = sphere(pos = vector(0, RADIUS, 0), radius = RADIUS, color = color.blue)

def generate_obstacles(n):
	from random import randint

	obstacles = []

	for i in range(n):
		x = randint(RADIUS, WIDTH - RADIUS)
		y = randint(RADIUS, LENGTH - RADIUS)
		obstacles.append( (x, y) )
		sphere(pos = vector(x, RADIUS, y), radius = RADIUS,
			   color = color.red)

	return obstacles

def minimize(start, end, obstacles):
	count = 0
	minp = start

	while minp != end and count < (WIDTH + LENGTH):
		mincost = INFINITY
		xc, yc = minp
		count += 1

		for x in (xc - 1, xc, xc + 1):
			for y in  (yc - 1, yc, yc + 1):
				p = (x, y)

				if p != (xc, yc):
					repulsions = map(lambda o: field( distance(p, o) ), obstacles)
					cost = distance(p, end) + sum(repulsions)

					if cost < mincost:
						mincost = cost
						minp = p

		yield minp

def distance(p1, p2):
	from math import sqrt

	x1, y1 = p1
	x2, y2 = p2

	return sqrt((x2 - x1) **2 + (y2 - y1) ** 2)

def field(distance):
	from math import log

	R = DIAMETER

	if distance == 0:
		return INFINITY

	elif distance <= R:
		return R * log(R / distance)

	else:
		return 0

def animate(p1, p2):
	BALL.pos = vector(p2[0], RADIUS, p2[1])
	sphere(pos = vector(p1[0], RADIUS, p1[1]), radius = 1,
		   color = color.green)

	return p2

def heatmap(obstacles):
	for i in range(WIDTH):
		for j in range(LENGTH):
			repulsions = map(lambda o: field( distance((i, j), o) ), obstacles)
			heat = sum(repulsions)

			if heat == 0:
				clr = color.blue

			elif 0 < heat <= 3:
				clr = color.green

			elif 3 < heat <= 7:
				clr = color.yellow

			elif 7 < heat <= 13:
				clr = color.orange

			else:
				clr = color.red

			box(pos = vector(i, 0, j), width = 1, 
				height = 1, length = 1, color = clr)

def main(n):
	origin = (0, 0)
	goal = (WIDTH, LENGTH)
	obstacles = generate_obstacles(n)

	# heatmap(obstacles)
	for intermediate in minimize(origin, goal, obstacles):
		rate(LENGTH / 10)
		origin = animate(origin, intermediate)

if __name__ == '__main__':
	from sys import argv

	if len(argv) > 1:
		main( int(argv[1]) )

	else:
		main(LENGTH / RADIUS)