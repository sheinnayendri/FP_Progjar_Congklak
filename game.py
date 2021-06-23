import pygame
from network import Network
import time 

class Player:

	def __init__(self, color):
		self.color = color
		self.biji = [7, 7, 7, 7, 7, 7, 7]
		self.poin = 0
		self.lubang = []

	def draw(self, g, color, x, y, gap, radius, border):
		for i in range(7):
			xx = x + (i * gap)
			yy = y
			self.lubang.append(pygame.draw.circle(g, color, (xx, yy), radius, border))

	def check_collision(self):
		if self.lubang[0].collidepoint(pygame.mouse.get_pos()) or self.lubang[1].collidepoint(pygame.mouse.get_pos()) or \
			self.lubang[2].collidepoint(pygame.mouse.get_pos()) or self.lubang[3].collidepoint(pygame.mouse.get_pos()) or \
			self.lubang[4].collidepoint(pygame.mouse.get_pos()) or self.lubang[5].collidepoint(pygame.mouse.get_pos()) or \
			self.lubang[6].collidepoint(pygame.mouse.get_pos()):
			pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
		else:
			pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

class Game:

	def __init__(self, w, h):
		self.net = Network()
		self.width = w
		self.height = h
		self.canvas = Canvas(self.width, self.height, "Congklak")
		self.image = pygame.image.load(r'D:\Sheinna\Kuliah\Semester 6\Progjar - C\fp\congklak.jpg')
		self.me = Player((255, 0, 0))
		self.rival = Player((0, 0, 255))
		self.me.draw(self.canvas.get_canvas(), self.me.color, 95, 280, 52, 25, 3)
		self.rival.draw(self.canvas.get_canvas(), self.rival.color, 95, 220, 52, 25, 3)

	def run(self):
		clock = pygame.time.Clock()
		run = True
		flag = 1
		warna = ''
		while run:
			clock.tick(60)

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					run = False

				if event.type == pygame.K_ESCAPE:
					run = False

			keys = pygame.key.get_pressed()

			if keys[pygame.K_0]:
				if self.me.biji[0] > 0:
					self.me.biji[0] -= 1

			self.me.check_collision()

			# if event.type == pygame.MOUSEBUTTONDOWN:
			# 	if self.rect.collidepoint(event.pos):
			# 		self.clicked = not self.clicked

			# Send Network Stuff
			# self.rival.x, self.rival.y = self.parse_data(self.send_data())

			# Update Canvas
			self.canvas.draw_background()
			self.canvas.draw_image(pygame.transform.scale(self.image, (500, 150)), (0, 175))
			for i in range(7):
				self.canvas.draw_text(str(self.me.biji[i]), 32, 90 + (i * 52), 270, self.me.color)
				# pygame.draw.circle(self.canvas.get_canvas(), self.me.color, (95, 280), 52, 25, 3)
			for i in range(7):
				self.canvas.draw_text(str(self.rival.biji[i]), 32, 90 + (i * 52), 210, self.rival.color)
				
			self.canvas.draw_text(str(self.me.poin), 32, 35, 240, self.rival.color)
			self.canvas.draw_text(str(self.rival.poin), 32, 455, 240, self.me.color)

			if(flag):
				pesan = self.net.send('status')
				self.canvas.draw_text('Waiting for other player 2 to join', 32, 0, 0, (255,255,255))
				print(pesan)
				if(pesan == 'start'):
					print('done')
					flag = 0
					pesan = self.net.client.recv(2048).decode().split(':')[0]
					if(pesan == '0'):
						warna = 'You are the First Player - Red'
						self.me.color = ((255, 0, 0))
						self.rival.color = ((0, 0, 255))
					else:
						warna = 'You are the Second Player - Blue'
						self.rival.color = ((255, 0, 0))
						self.me.color = ((0, 0, 255))
					self.canvas.draw_text(pesan, 32, 0, 0, (255,255,255))
			else:
				self.canvas.draw_text(warna, 32, 0, 0, (255,255,255))
			# self.canvas.draw_text(str(self.net.recv_msg(self.net.client)), 32, 0, 0, self.me.color)
			self.canvas.update()

		pygame.quit()

	def send_data(self):
		"""
		Send position to server
		:return: None
		"""
		data = str(self.net.id) + ":" + str(self.player.x) + "," + str(self.player.y)
		reply = self.net.send(data)
		return reply

	@staticmethod
	def parse_data(data):
		try:
			d = data.split(":")[1].split(",")
			return int(d[0]), int(d[1])
		except:
			return 0,0


class Canvas:

	def __init__(self, w, h, name="None"):
		self.width = w
		self.height = h
		self.screen = pygame.display.set_mode((w,h))
		pygame.display.set_caption(name)

	@staticmethod
	def update():
		pygame.display.update()

	def draw_text(self, text, size, x, y, color):
		pygame.font.init()
		font = pygame.font.SysFont("comicsans", size)
		render = font.render(text, 1, color)

		self.screen.blit(render, (x,y))

	def get_canvas(self):
		return self.screen

	def draw_background(self):
		self.screen.fill((0,0,0))

	def draw_image(self, image, position):
		self.screen.blit(image, position)