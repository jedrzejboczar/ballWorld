import math
import pygame

class PhysicalObject(object):
	def __init__(self, name, mass, position, velocity=(0, 0), force=(0, 0), friction=None):
		self.name = name
		self.m = float(mass)
		self.x, self.y = [float(a) for a in position]	# (x,y)
		self.vx, self.vy = [float(a) for a in velocity]
		self.fx, self.fy = [float(a) for a in force]
		self.friction = friction

	def move(self):
		self.countPhysics()
		self.x += self.vx
		self.y -= self.vy	# WAZNE: bo na wyswietlaniu y jest odwrocony

	def checkBorderCollisions(self, borders):
		pass

	def countPhysics(self):
		self.ax = float(self.fx) / float(self.m)
		self.ay = float(self.fy) / float(self.m)
		self.vx += self.ax
		self.vy += self.ay
		if self.friction:
			self.vx *= (1.0 - self.friction)
			self.vy *= (1.0 - self.friction)

	def draw(self):
		pass

	def xy(self):
		return self.x, self.y



class Ball(PhysicalObject):
	def __init__(self, name, radius, color, mass, position, velocity=(0, 0), force=(0, 0)):
		PhysicalObject.__init__(self, name, mass, position, velocity, force)
		self.radius = float(radius)
		self.color = color

	def draw(self, paintScreen):
		x, y = int(self.x), int(self.y)
		pygame.draw.circle(paintScreen, self.color, (x, y), int(self.radius))





def distance((x1, y1), (x2, y2)):
	d = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
	return d

def dot((x1, y1), (x2, y2)):
	return x1*x2 + y1*y2

if __name__ == '__main__':
	pass
	# o = PhysicalObject(10, (2,2), (0.1, 0.3))
	# print o.x, o.y
	# o.move(1)
	# print o.x, o.y
	# o.move(3)
	# print o.x, o.y
	# o.move(10)
	# o.v = -0.3
	# print o.x, o.y
	# o.move(5)
	# print o.x, o.y
