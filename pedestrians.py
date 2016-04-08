#! /usr/bin/python
from visual import box, color, rate, scene, sphere, vector

INFINITY = float('infinity')

LENGTH = 1000
WIDTH = LENGTH

RADIUS = 10
DIAMETER = RADIUS + RADIUS

scene.title = 'Pedestrians'
scene.fullscreen = True
scene.forward = (0, -0.25, -0.5)
scene.center = vector(WIDTH / 2, 0, LENGTH / 2)

box(pos = vector(WIDTH / 2, 0, LENGTH  / 2), width = WIDTH, height = 0.1,
	length = LENGTH, color = color.white)

def generate_pedestrians(n):
	from random import randint

	pedestrians = []
	goals = ((WIDTH, LENGTH, color.red), (WIDTH, 0, color.blue),
			 (0, LENGTH, color.green), (0, 0, color.yellow))

	for xgoal, ygoal, clr in goals:
		for i in range(n):
			x = abs(abs(xgoal - WIDTH) - randint(0, WIDTH / 10))
			y = abs(abs(ygoal - LENGTH) - randint(0, LENGTH / 10))
			image = sphere(pos = vector(x, RADIUS, y), radius = RADIUS,
						   color = clr)
			pedestrians.append( ((x, y), (xgoal, ygoal), image) )

	return pedestrians

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

	R = 3 * DIAMETER

	if distance == 0:
		return INFINITY

	elif distance <= R:
		return R * log(R / distance)

	else:
		return 0

def draw(pedestrians):
	for current, goal, image in pedestrians:
		x, y = current
		image.pos = (x, RADIUS, y)

def main(n):
	pedestrians = generate_pedestrians(n)
	aux = [False] * n * 4
	minimizers = []
	done = False
	i = 0

	draw(pedestrians)
	for i, p in enumerate(pedestrians):
		start, end, img = p
		control = map(lambda p: p[0], pedestrians[:i] + pedestrians[i + 1:])
		minimizers.append( (minimize(start, end, control), control) )

	while not done:
		for i, p in enumerate(pedestrians):
			try:
				rate(WIDTH / 5)
				pedestrians[i] = (minimizers[i][0].next(), p[1], p[2])
				draw(pedestrians)
				for j, m in enumerate(minimizers):
					minimizer, control = m

					if j > i:
						control[i] = pedestrians[i][0]

					elif j < i:
						control[-i] = pedestrians[i][0]


			except StopIteration:
				aux[i] = True
				done = reduce(lambda x, y: x and y, aux)

if __name__ == '__main__':
	from sys import argv

	if len(argv) > 1:
		main( int(argv[1]) )

	else:
		main(1)