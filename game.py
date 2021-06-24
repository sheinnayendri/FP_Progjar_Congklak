from typing import Counter
import pygame
from network import Network
import time 

class Player:

	def __init__(self, color):
		self.color = color
		self.biji = [7, 7, 7, 7, 7, 7, 7]
		self.poin = 0
		self.lubang = []
		self.tanda = [False, False, False, False, False, False, False]

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

	def animasi_biji(self, banyak_biji, start_pos):
		cur_pos = start_pos
		self.biji[cur_pos] = 0
		cur_pos += 1
		cur_pos %= 7
		for i in range(banyak_biji):
			self.biji[cur_pos] += 1
			cur_pos += 1
			if(cur_pos == 6):
				self.poin += 1
				self.pindah_ke_rival()



class Game:

	def __init__(self, w, h):
		self.net = Network()
		self.width = w
		self.height = h
		self.canvas = Canvas(self.width, self.height, "Congklak")
		self.image = pygame.image.load(r'D:\Sheinna\Kuliah\Semester 6\Progjar - C\FP_Progjar_Congklak\congklak.jpg')
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

			self.me.check_collision()

			# Send Network Stuff
			# self.rival.x, self.rival.y = self.parse_data(self.send_data())

			# Update Canvas
			self.canvas.draw_background()
			self.canvas.draw_image(pygame.transform.scale(self.image, (500, 150)), (0, 175))
			for i in range(7):
				self.canvas.draw_text(str(self.me.biji[i]), 32, 90 + (i * 52), 270, self.me.color)
			for i in range(7):
				self.canvas.draw_text(str(self.rival.biji[i]), 32, 90 + (i * 52), 210, self.rival.color)
				
			self.canvas.draw_text(str(self.me.poin), 32, 455, 240, self.me.color)
			self.canvas.draw_text(str(self.rival.poin), 32, 35, 240, self.rival.color)

			if(event.type == pygame.MOUSEBUTTONDOWN):
				if(self.me.lubang[0].collidepoint(event.pos) and self.me.tanda[0] == False and self.me.biji[0] > 0):
					self.ambil_biji(0)
					self.me.tanda[0] = True
				elif(self.me.lubang[1].collidepoint(event.pos) and self.me.tanda[1] == False and self.me.biji[1] > 0):
					self.ambil_biji(1)
					self.me.tanda[1] = True
				elif(self.me.lubang[2].collidepoint(event.pos) and self.me.tanda[2] == False and self.me.biji[2] > 0):
					self.ambil_biji(2)
					self.me.tanda[2] = True
				elif(self.me.lubang[3].collidepoint(event.pos) and self.me.tanda[3] == False and self.me.biji[3] > 0):
					self.ambil_biji(3)
					self.me.tanda[3] = True
				elif(self.me.lubang[4].collidepoint(event.pos) and self.me.tanda[4] == False and self.me.biji[4] > 0):
					self.ambil_biji(4)
					self.me.tanda[4] = True
				elif(self.me.lubang[5].collidepoint(event.pos) and self.me.tanda[5] == False and self.me.biji[5] > 0):
					self.ambil_biji(5)
					self.me.tanda[5] = True
				elif(self.me.lubang[6].collidepoint(event.pos) and self.me.tanda[6] == False and self.me.biji[6] > 0):
					self.ambil_biji(6)
					self.me.tanda[6] = True

			if(event.type == pygame.MOUSEBUTTONUP):
				if(self.me.lubang[0].collidepoint(event.pos)):
					self.me.tanda[0] = False
				elif(self.me.lubang[1].collidepoint(event.pos)):
					self.me.tanda[1] = False
				elif(self.me.lubang[2].collidepoint(event.pos)):
					self.me.tanda[2] = False
				elif(self.me.lubang[3].collidepoint(event.pos)):
					self.me.tanda[3] = False
				elif(self.me.lubang[4].collidepoint(event.pos)):
					self.me.tanda[4] = False
				elif(self.me.lubang[5].collidepoint(event.pos)):
					self.me.tanda[5] = False
				elif(self.me.lubang[6].collidepoint(event.pos)):
					self.me.tanda[6] = False

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
			self.canvas.update()

		pygame.quit()

	def send_data(self):
		data = str(self.net.id) + ":" + str(self.player.x) + "," + str(self.player.y)
		reply = self.net.send(data)
		return reply

	def ambil_biji(self, start_pos):
		banyak_biji = self.me.biji[start_pos]
		self.me.biji[start_pos] = 0
		print('ambil me', banyak_biji, start_pos + 1)
		sisa_biji, cur_pos, player = self.animasi_biji_me(banyak_biji, start_pos + 1)
		print('back to home', player, cur_pos)
		if(cur_pos == 7): #reach home
			print('finish animasi me back to home')
		elif(player == 'me'):
			if(self.me.biji[cur_pos] == 0):
				print('finish animasi me', cur_pos)
			else:
				self.ambil_biji(cur_pos)
		else:
			if(self.rival.biji[cur_pos] == 0):
				print('finish animasi rival', cur_pos)
			else:
				self.ambil_biji_rival(cur_pos)

	def ambil_biji_rival(self, start_pos):
		banyak_biji = self.rival.biji[start_pos]
		self.rival.biji[start_pos] = 0
		print('ambil rival', banyak_biji, start_pos - 1)
		sisa_biji, cur_pos, player = self.animasi_biji_rival(banyak_biji, start_pos - 1)
		print('back to rival', player, cur_pos)
		if(cur_pos == 7): #reach home
			print('finish animasi rival back to home')
		elif(player == 'me'):
			if(self.me.biji[cur_pos] == 0):
				print('finish animasi me', cur_pos)
			else:
				self.ambil_biji(cur_pos)
		else:
			if(self.rival.biji[cur_pos] == 0):
				print('finish animasi rival', cur_pos)
			else:
				self.ambil_biji_rival(cur_pos)
		

	def animasi_biji_me(self, banyak_biji, start_pos):
		cur_pos = start_pos
		sisa_biji = banyak_biji
		player = 'me'
		if(cur_pos == 7 and sisa_biji > 0):
			self.me.poin += 1
			sisa_biji -= 1
			if(sisa_biji == 0):
				return 0, cur_pos, 'me'
			sisa_biji, cur_pos, player = self.animasi_biji_rival(sisa_biji, 6)
		else:
			while(sisa_biji):
				print('animasi me', cur_pos, sisa_biji)
				self.me.biji[cur_pos] += 1
				sisa_biji -= 1
				if(sisa_biji == 0):
					return 0, cur_pos, 'me'
				cur_pos += 1
				if(cur_pos == 7 and sisa_biji > 0):
					self.me.poin += 1
					sisa_biji -= 1
					sisa_biji, cur_pos, player = self.animasi_biji_rival(sisa_biji, 6)
		return sisa_biji, cur_pos, player

	def animasi_biji_rival(self, banyak_biji, start_pos):
		cur_pos = start_pos
		sisa_biji = banyak_biji
		player = 'rival'
		if(cur_pos == -1 and sisa_biji > 0):
			sisa_biji, cur_pos, player = self.animasi_biji_me(sisa_biji, 0)
		else:
			while(sisa_biji):
				print('animasi rival', cur_pos, sisa_biji)
				self.rival.biji[cur_pos] += 1
				sisa_biji -= 1
				if(sisa_biji == 0):
					return 0, cur_pos, 'rival'
				cur_pos -= 1
				if(cur_pos == -1 and sisa_biji > 0):
					print('oper to me', 0, sisa_biji);
					sisa_biji, cur_pos, player = self.animasi_biji_me(sisa_biji, 0)
		return sisa_biji, cur_pos, player

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