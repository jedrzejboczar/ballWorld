from pygamehelper import PygameHelper
from physicalObjects import *

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class World(PygameHelper):
	def __init__(self, objects=[]):
		PygameHelper.__init__(self, (640, 480), WHITE)
		# super(self.__class__, self).__init__()
		self.objects = objects
		self.gravity = [0, -10]
		self.last_gravity = self.gravity

	def mainLoop(self):
		PygameHelper.mainLoop(self, 40)
		# super(self.__class__, self).mainLoop(40)


	def doPhysics(self):
		for o in self.objects:
			o.move(self.size)

	def update(self):
		for o in self.objects:
			o.fx, o.fy = self.gravity
		self.doPhysics()
		self.checkBallCollisions()


	def draw(self):
		self.screen.fill(WHITE)
		for o in self.objects:
			o.draw(self.screen)
		o1 = self.objects[0]
		# o obiekcie nr 1
		text = pygame.font.SysFont("serif", 15).render(o1.name + ":", True, BLACK)
		self.screen.blit(text, (20, 345))
		text = pygame.font.SysFont("serif", 15).render("x = (" + str(o1.x) + ", " + str(o1.y) + ")", True, BLACK)
		self.screen.blit(text, (20, 370))
		text = pygame.font.SysFont("serif", 15).render("v = (" + str(o1.vx) + ", " + str(o1.vy) + ")", True, BLACK)
		self.screen.blit(text, (20, 395))
		text = pygame.font.SysFont("serif", 15).render("a = (" + str(o1.ax) + ", " + str(o1.ay) + ")", True, BLACK)
		self.screen.blit(text, (20, 420))
		text = pygame.font.SysFont("serif", 15).render("F = (" + str(o1.fx) + ", " + str(o1.fy) + ")", True, BLACK)
		self.screen.blit(text, (20, 445))

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

	def checkBallCollisions(self):
		n = len(self.objects)
		for i in range(n):
			o1 = self.objects[i]
			for j in range(n-i-1):
				o2 = self.objects[i+j+1]
				if distance((o1.x, o1.y), (o2.x, o2.y)) <= o1.radius + o2.radius:
					self.countBallCollision(o1, o2)

	def countBallCollision(self, o1, o2):
		print "collision: ", o1.name, " - ", o2.name
		# u - predkosci po zderzeniu
		u1x = ((o1.m - o2.m)*o1.vx + 2*o2.m*o2.vx) / (o1.m + o2.m)
		u1y = ((o1.m - o2.m)*o1.vy + 2*o2.m*o2.vy) / (o1.m + o2.m)
		u2x = ((o2.m - o1.m)*o2.vx + 2*o1.m*o1.vx) / (o1.m + o2.m)
		u2y = ((o2.m - o1.m)*o2.vy + 2*o1.m*o1.vy) / (o1.m + o2.m)
		o1.vx = u1x
		o1.vy = u1y
		o2.vx = u2x
		o2.vy = u2y


if __name__ == '__main__':
	o1 = Ball("red_ball", 18, (215, 20, 20), mass=20, position=(140,180), velocity=(4.5, 0), force=(0, -10))
	o2 = Ball("green_ball", 21, (20, 215, 20), mass=30, position=(240,110), velocity=(-1.5, 0), force=(0, -10))
	o3 = Ball("blue_ball", 13, (20, 20, 215), mass=10, position=(160,90), velocity=(7.5, 0), force=(0, -10))
	world = World([o1, o2, o3])
	world.mainLoop()
