from pygamehelper import PygameHelper
from physicalObjects import *
import time

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class BallWorld(PygameHelper):
	def __init__(self, objects=[], gravity=[0, -10]):
		PygameHelper.__init__(self, (640, 480), WHITE)
		# super(self.__class__, self).__init__()
		self.objects = objects
		self.gravity = gravity
		self.collisions = []
		for o in objects:
			o.fx, o.fy = self.gravity[0], self.gravity[1]
		self.time = True

	def mainLoop(self):
		PygameHelper.mainLoop(self, 40)
		# super(self.__class__, self).mainLoop(40)


	def doPhysics(self):
		self.checkBorderCollisions()
		self.checkBallCollisions()
		for o in self.objects:
			o.move()

	def update(self):
		if self.time:
			for o in self.objects:
				o.fx, o.fy = self.gravity
			self.doPhysics()

		time.sleep(0.1)


	def draw(self):
		self.screen.fill(WHITE)
		for o in self.objects:
			o.draw(self.screen)
		o1 = self.objects[0]
		# o obiekcie nr 1
		sum_m = 0
		sum_ek = 0
		for o in objects:
			sum_m += o.m * (o.vx + o.vy)
			sum_ek += 0.5 * o.m * (o.vx**2 + o.vy**2)
		text = pygame.font.SysFont("serif", 15).render("sum_Ek = " + str(sum_ek), True, BLACK)
		self.screen.blit(text, (10, 330))
		text = pygame.font.SysFont("serif", 15).render("sum_momentum = " + str(sum_m), True, BLACK)
		self.screen.blit(text, (10, 350))
		text = pygame.font.SysFont("serif", 15).render(o1.name + ":", True, BLACK)
		self.screen.blit(text, (10, 370))
		text = pygame.font.SysFont("serif", 15).render("x = (" + str(o1.x) + ", " + str(o1.y) + ")", True, BLACK)
		self.screen.blit(text, (10, 390))
		text = pygame.font.SysFont("serif", 15).render("v = (" + str(o1.vx) + ", " + str(o1.vy) + ")", True, BLACK)
		self.screen.blit(text, (10, 410))
		text = pygame.font.SysFont("serif", 15).render("a = (" + str(o1.ax) + ", " + str(o1.ay) + ")", True, BLACK)
		self.screen.blit(text, (10, 430))
		text = pygame.font.SysFont("serif", 15).render("F = (" + str(o1.fx) + ", " + str(o1.fy) + ")", True, BLACK)
		self.screen.blit(text, (10, 450))

	def keyDown(self, key):
		if key == pygame.K_UP:
			self.gravity[1] += 1
			print "K_UP"
		elif key == pygame.K_DOWN:
			self.gravity[1] -= 1
			print "K_DOWN"
		elif key == pygame.K_LEFT:
			self.gravity[0] -= 1
			print "K_LEFT"
		elif key == pygame.K_RIGHT:
			self.gravity[0] += 1
			print "K_RIGHT"
		elif key == pygame.K_SPACE:
			if self.time:
				self.time = False
				print "TIME: STOP"
			else:
				self.time = True
				print "TIME: START"

	def checkBorderCollisions(self):
		for o in self.objects:
			if o.x - o.radius < 0: # lewa sciana
				o.vx = abs(o.vx)
				o.x = 0 + o.radius
			elif o.x + o.radius > self.size[0]: # prawa sciana
				o.vx = -abs(o.vx)
				o.x = self.size[0] - o.radius
			elif o.y - o.radius < 0: # gorna sciana
				o.vy = -abs(o.vy)
				o.y = 0 + o.radius
			elif o.y + o.radius > self.size[1]: # dolna sciana
				o.vy = abs(o.vy)
				o.y = self.size[1] - o.radius

	def checkBallCollisions(self):
		n = len(self.objects)
		for i, o1 in enumerate(self.objects):
			for o2 in self.objects[(i+1):]:
				if distance(o1.xy(), o2.xy()) <= o1.radius + o2.radius:
					# self.time = False
					self.countBallCollision(o1, o2)

	def countBallCollision_easy(self, o1, o2):	# STABILNE, ale troche bledne
		print "easy"
		# u - predkosci po zderzeniu
		u1x = ((o1.m - o2.m)*o1.vx + 2*o2.m*o2.vx) / (o1.m + o2.m)
		u1y = ((o1.m - o2.m)*o1.vy + 2*o2.m*o2.vy) / (o1.m + o2.m)
		u2x = ((o2.m - o1.m)*o2.vx + 2*o1.m*o1.vx) / (o1.m + o2.m)
		u2y = ((o2.m - o1.m)*o2.vy + 2*o1.m*o1.vy) / (o1.m + o2.m)
		o1.vx, o1.vy, o2.vx, o2.vy = u1x, u1y, u2x, u2y
		# # odsuniecie od siebie kul
		# o1.move()
		# o2.move()

	def countBallCollision_hard(self, o1, o2):
		print "hard"
		dist = distance(o1.xy(), o2.xy())
		dx = o1.x - o2.x
		dy = o1.y - o2.y
		# kat nowego ukladu wsp w stosunku do starego
		sin_alfa = dx / dist
		cos_alfa = dy / dist

		# predkosci w nowym ukl wspl
		w1x = o1.vx * cos_alfa + o1.vy * sin_alfa # o1.vx * cos_alfa - o1.vy * sin_alfa
		w1y = o1.vx * sin_alfa + o1.vy * cos_alfa
		w2x = o2.vx * cos_alfa + o2.vy * sin_alfa # o2.vx * cos_alfa - o2.vy * sin_alfa
		w2y = o2.vx * sin_alfa + o2.vy * cos_alfa
		print "{} = {} * {} + {} * {}".format(w1x, o1.vx, cos_alfa, o1.vy, sin_alfa)
		print "{} = {} * {} + {} * {}".format(w1y, o1.vx, sin_alfa, o1.vy, cos_alfa)
		print "{} = {} * {} + {} * {}".format(w2x, o2.vx, cos_alfa, o2.vy, sin_alfa)
		print "{} = {} * {} + {} * {}".format(w2y, o2.vx, sin_alfa, o2.vy, cos_alfa)
		print w1x, w1y, w2x, w2y

		# w nowym ukladzie zderzenie odbywa sie tylko w jednym wymiarze
		# wiec wy nie zmieniaja sie
		# u1x = ((o1.m - o2.m)*w1x + 2*o2.m*w2x) / (o1.m + o2.m)
		# u2x = ((o2.m - o1.m)*w2x + 2*o1.m*w1x) / (o1.m + o2.m)
		# u1y = w1y
		# u2y = w2y

		# u1x = w1x
		# u2x = w2x
		# u1y = ((o1.m - o2.m)*w1y + 2*o2.m*w2y) / (o1.m + o2.m)
		# u2y = ((o2.m - o1.m)*w2y + 2*o1.m*w1y) / (o1.m + o2.m)


		u1x = -w1x
		u2x = -w2x
		u1y = w1y
		u2y = w2y

		print u1x, u1y, u2x, u2y

		# powrot do poprzedniego ukladu
		o1.vx = u1x * cos_alfa + u1y * sin_alfa
		o1.vy = u1x * sin_alfa + u1y * cos_alfa # - u1x * sin_alfa + u1y * cos_alfa
		o2.vx = u2x * cos_alfa + u2y * sin_alfa
		o2.vy = u2x * sin_alfa + u2y * cos_alfa # - u2x * sin_alfa + u2y * cos_alfa

		print o1.vx, o1.vy, o2.vx, o2.vy


	def countBallCollision(self, o1, o2):
		print "collision:", o1.name, "-", o2.name

		dist = distance(o1.xy(), o2.xy())
		dx = o1.x - o2.x
		dy = o1.y - o2.y

		if dist < min(o1.radius, o2.radius):
			return	# jak kulka wewnatrz drugiej to niech juz nie liczy kolizji

		# if is_almost_zero(dx) or is_almost_zero(dy):
		# 	self.countBallCollision_easy(o1, o2)
		# else:
		# 	self.countBallCollision_hard(o1, o2)

		if False:
			self.countBallCollision_easy(o1, o2)
		else:
			self.countBallCollision_hard(o1, o2)

		# odsuniecie od siebie kul
		o1.move()
		o2.move()

def is_almost_zero(num):
	breakpoint = 0.01
	if num < breakpoint:
		return True
	return False

def _mass(radius):
	# a = 0.001
	# return a * radius**3
	a = 0.04
	return a * radius**2

if __name__ == '__main__':
	gravity = [0, 0]
	objects = []
	# r = 11;	objects.append(Ball("red_ball", r, (215, 20, 20), mass=_mass(r), position=(20,20), velocity=(4.5, 0), force=(0, -10)))
	# r = 13;	objects.append(Ball("green_ball", r, (20, 215, 20), mass=_mass(r), position=(30,70), velocity=(-1.5, 0), force=(0, -10)))
	# r = 16;	objects.append(Ball("blue_ball", r, (20, 20, 215), mass=_mass(r), position=(60,230), velocity=(7.5, 0), force=(0, -10)))
	# r = 19;	objects.append(Ball("yellow_ball", r, (215, 215, 20), mass=_mass(r), position=(350,50), velocity=(-1.5, 0.0)))
	# r = 21; objects.append(Ball("purple_ball", r, (215, 20, 215), mass=_mass(r), position=(240,150), velocity=(7.5, 0.0)))
	# r = 24; objects.append(Ball("skyblue_ball", r, (20, 215, 215), mass=_mass(r), position=(500,90), velocity=(7.5, 0.0)))
	# r = 27; objects.append(Ball("grey_ball", r, (180, 180, 180), mass=_mass(r), position=(140,50), velocity=(7.5, 0.0)))
	# r = 31; objects.append(Ball("black_ball", r, (50, 50, 50), mass=_mass(r), position=(460,320), velocity=(7.5, 0.0)))
	# r = 37; objects.append(Ball("brown_ball", r, (170, 80, 0), mass=_mass(r), position=(190,360), velocity=(7.5, 0.0)))

	r = 31; objects.append(Ball("black_ball", r, (50, 50, 50), mass=_mass(r), position=(460,330), velocity=(-7.5, 0)))
	r = 31; objects.append(Ball("brown_ball", r, (170, 80, 0), mass=_mass(r), position=(190,310), velocity=(0, 0)))


	world = BallWorld(objects, gravity)
	world.mainLoop()
