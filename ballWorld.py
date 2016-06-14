from pygamehelper import PygameHelper
from physicalObjects import *

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
		for o in self.objects:
			o.move()
		self.checkBallCollisions()
		self.checkBorderCollisions()

	def update(self):
		if self.time:
			for o in self.objects:
				o.fx, o.fy = self.gravity
			self.doPhysics()


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
				print "STOP TIME"
			else:
				self.time = True
				print "START TIME"

	def checkBallCollisions(self):
		n = len(self.objects)
		for i in range(n):
			o1 = self.objects[i]
			for j in range(n-i-1):
				o2 = self.objects[i+j+1]
				if distance(o1.xy(), o2.xy()) <= o1.radius + o2.radius:
					self.countBallCollision(o1, o2)

	def countBallCollision(self, o1, o2):
		print "collision:", o1.name, "-", o2.name
		# punkt kolizji do wizualizacji
		dist = distance(o1.xy(), o2.xy())

		# cos_alfa = dist / (o1.x - o2.x) # chyba zle
		# sin_alfa = dist / (o1.y - o2.y)
		# cx = cos_alfa * (o1.x + o1.radius)
		# cy = sin_alfa * (o1.y + o1.radius)
		# pygame.draw.circle(self.screen, BLACK, (int(cx), int(cy)), 8)
		# print cx, cy

		# # przeniesienie ukladu wspolrzednych, alfa - kat linii pomiedzy srodkami
		# cos_alfa = dist / (o1.x - o2.x)

		# u - predkosci po zderzeniu
		u1x = ((o1.m - o2.m)*o1.vx + 2*o2.m*o2.vx) / (o1.m + o2.m)
		u1y = ((o1.m - o2.m)*o1.vy + 2*o2.m*o2.vy) / (o1.m + o2.m)
		u2x = ((o2.m - o1.m)*o2.vx + 2*o1.m*o1.vx) / (o1.m + o2.m)
		u2y = ((o2.m - o1.m)*o2.vy + 2*o1.m*o1.vy) / (o1.m + o2.m)
		o1.vx, o1.vy, o2.vx, o2.vy = u1x, u1y, u2x, u2y

		# # powrot do poprzedniego ukladu
		# o1.vx, o1.vy, o2.vx, o2.vy = o1.vx*cos_alfa, o1.vy*sin_alfa, o2.vx*cos_alfa, o2.vy*sin_alfa


		# odsuniecie od siebie kul
		o1.move()
		o2.move()


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


def _mass(radius):
	# a = 0.001
	# return a * radius**3
	a = 0.04
	return a * radius**2

if __name__ == '__main__':
	gravity = [0, 0]
	objects = []
	r = 13;	objects.append(Ball("red_ball", r, (215, 20, 20), mass=_mass(r), position=(140,180), velocity=(4.5, 0), force=(0, -10)))
	r = 18;	objects.append(Ball("green_ball", r, (20, 215, 20), mass=_mass(r), position=(240,110), velocity=(-1.5, 0), force=(0, -10)))
	r = 24;	objects.append(Ball("blue_ball", r, (20, 20, 215), mass=_mass(r), position=(160,90), velocity=(7.5, 0), force=(0, -10)))
	r = 31;	objects.append(Ball("yellow_ball", r, (215, 215, 20), mass=_mass(r), position=(60,60), velocity=(-1.5, 0.0)))
	r = 37; objects.append(Ball("purple_ball", r, (215, 20, 215), mass=_mass(r), position=(190,260), velocity=(7.5, 0.0)))
	world = BallWorld(objects, gravity)
	world.mainLoop()
