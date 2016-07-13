import math
import pygame

# TROCHE NA WYROST - na razie i tak tylko kule
class PhysicalObject(object):
	def __init__(self, name, mass, position, velocity=(0, 0), force=(0, 0), friction=None, drawVelocity=False):
		self.name = name
		self.m = float(mass)
		self.x, self.y = [float(a) for a in position]	# (x,y)
		self.vx, self.vy = [float(a) for a in velocity]
		self.fx, self.fy = [float(a) for a in force]
		self.friction = friction
		self.drawVelocity = drawVelocity

	# Czas jest dyskretny, wiec odliczany w klatkach
	# (chociaz teoretycznie mozna poruszyc o czas ciagly, np przy wyliczani punktu zderzenia)
	def move(self, frames=1):
		self.countPhysics()
		self.x += time * self.vx
		self.y -= time * self.vy	# WAZNE: bo na wyswietlaniu y jest odwrocony

	def countPhysics(self):
		self.ax = float(self.fx) / float(self.m)
		self.ay = float(self.fy) / float(self.m)
		self.vx += self.ax
		self.vy += self.ay
		if self.friction:
			self.vx *= (1.0 - self.friction)
			self.vy *= (1.0 - self.friction)

	# PhysicalObject moze rysowac tylko wektor predkosci, wyglad zalezy od podklasy
	def draw(self, screen):
		if self.drawVelocity:
			self.drawVeclocityVector(screen)

	def xy(self):
		return self.x, self.y

	def drawVeclocityVector(self, screen):
		A = 0.2
		start = (self.x, self.y)
		end = (self.x + 10*self.vx, self.y - 10*self.vy)
		points = [start, end]
		pygame.draw.lines(screen, (255, 0, 0), False, points, 2)

		fi = math.pi / 6
		xl = end[0] + A * ((start[0] - end[0]) * math.cos(fi) + (start[1] - end[1]) * math.sin(fi))
		yl = end[1] + A * ((start[1] - end[1]) * math.cos(fi) - (start[0] - end[0]) * math.sin(fi))
		xp = end[0] + A * ((start[0] - end[0]) * math.cos(fi) - (start[1] - end[1]) * math.sin(fi))
		yp = end[1] + A * ((start[1] - end[1]) * math.cos(fi) + (start[0] - end[0]) * math.sin(fi))
		left = (xl, yl)
		right = (xp, yp)
		points = [end, left, right]
		pygame.draw.polygon(screen, (255, 0, 0), points)



class Ball(PhysicalObject):
	def __init__(self, name, radius, color, mass, position, velocity=(0, 0), force=(0, 0), friction=None, drawVelocity=False):
		PhysicalObject.__init__(self, name, mass, position, velocity, force, friction, drawVelocity)
		self.radius = float(radius)
		self.color = color

	def draw(self, screen):
		x, y = int(self.x), int(self.y)
		pygame.draw.circle(screen, self.color, (x, y), int(self.radius))
		PhysicalObject.draw(self, screen)





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
