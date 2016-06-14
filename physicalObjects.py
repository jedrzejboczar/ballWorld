import math
import pygame

class PhysicalObject(object):
	def __init__(self, name, mass, position, velocity=(0, 0), force=(0, 0)):
		self.name = name
		self.m = mass
		self.x, self.y = position	# (x,y)
		self.vx, self.vy = velocity
		self.fx, self.fy = force

	def move(self, borders):
		self.countPhysics()
		self.x += self.vx
		self.y -= self.vy	# WAZNE: bo na wyswietlaniu y jest odwrocony
		self.checkBorderCollisions(borders)

	def checkBorderCollisions(self, borders):
		pass

	def countPhysics(self):
		self.ax = float(self.fx) / float(self.m)
		self.ay = float(self.fy) / float(self.m)
		self.vx += self.ax
		self.vy += self.ay

	def draw(self):
		pass



class Ball(PhysicalObject):
	def __init__(self, name, radius, color, mass, position, velocity=(0, 0), force=(0, 0)):
		PhysicalObject.__init__(self, name, mass, position, velocity, force)
		self.radius = radius
		self.color = color

	def draw(self, paintScreen):
		x, y = int(self.x), int(self.y)
		pygame.draw.circle(paintScreen, self.color, (x, y), self.radius)

	def checkBorderCollisions(self, borders):
		if self.x - self.radius < 0: # lewa sciana
			self.vx = abs(self.vx)
			self.x = 0 + self.radius
		elif self.x + self.radius > borders[0]: # prawa sciana
			self.vx = -abs(self.vx)
			self.x = borders[0] - self.radius
		elif self.y - self.radius < 0: # gorna sciana
			self.vy = -abs(self.vy)
			self.y = 0 + self.radius
		elif self.y + self.radius > borders[1]: # dolna sciana
			self.vy = abs(self.vy)
			self.y = borders[1] - self.radius



def distance((x1,y1), (x2, y2)):
	d = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
	return d

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
