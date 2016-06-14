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

		self.y_max = 640

	def mainLoop(self):
		PygameHelper.mainLoop(self, 40)
		# super(self.__class__, self).mainLoop(40)


	def doPhysics(self):
		for obj in self.objects:
			pass

	def update(self):
		for o in self.objects:
			o.fx, o.fy = self.gravity
		for o in self.objects:
			o.move(self.size)


	def draw(self):
		self.screen.fill(WHITE)
		for o in self.objects:
			o.draw(self.screen)
		o1 = self.objects[0]
		if o1.y < self.y_max:
			self.y_max = o1.y
		# o obiekcie nr 1
		text = pygame.font.SysFont("serif", 15).render("y_max = (" + str(640 - self.y_max) + ")", True, BLACK)
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


if __name__ == '__main__':
	o = Ball(mass=10, position=(140,180), velocity=(4.5, 0), force=(0, -10))
	world = World([o])
	world.mainLoop()
