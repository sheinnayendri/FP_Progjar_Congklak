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

class Game:

	def __init__(self, w, h):
		self.net = Network()
		self.width = w
		self.height = h
		self.animate = False
		self.bg_color = (0, 0, 0)
		self.bg_contrast = (255, 255, 255)
		self.on_color = (0, 255, 0)
		self.canvas = Canvas(self.width, self.height, "Congklak")
		self.image = pygame.image.load(r'congklak.jpg')
		self.me = Player((255, 0, 0))
		self.rival = Player((0, 0, 255))
		self.rival_move = -1
		self.turn = 'me'
		self.me.draw(self.canvas.get_canvas(), self.me.color, 95, 280, 52, 25, 3)
		self.rival.draw(self.canvas.get_canvas(), self.rival.color, 95, 220, 52, 25, 3)

	def run(self):
		clock = pygame.time.Clock()
		run = True
		flag = 1
		warna = ''
		cek = 0
		while run:
			clock.tick(30)

			for event in pygame.event.get():
				if event.type == pygame.MOUSEBUTTONUP:
					None

				if event.type == pygame.QUIT:
					run = False

				if event.type == pygame.K_ESCAPE:
					run = False

			self.me.check_collision()

			# Update Canvas
			self.canvas.draw_background()
			# self.canvas.draw_image(pygame.transform.scale(self.image, (505, 155)), (0, 175))

			# menggambar lingkaran
			# menggambar jumlah biji
			if(self.animate == False):
				self.me.draw(self.canvas.get_canvas(), self.me.color, 95, 280, 52, 25, 3)
				self.rival.draw(self.canvas.get_canvas(), self.rival.color, 95, 220, 52, 25, 3)
				for i in range(7):
					self.canvas.draw_text(str(self.me.biji[i]), 32, 85 + (i * 52), 270, self.me.color)
				for i in range(7):
					self.canvas.draw_text(str(self.rival.biji[i]), 32, 85 + (i * 52), 210, self.rival.color)
				self.canvas.draw_text(str(self.me.poin), 32, 450, 240, self.me.color)
				self.canvas.draw_text(str(self.rival.poin), 32, 30, 240, self.rival.color)
				pygame.draw.circle(self.canvas.get_canvas(), self.me.color, (460, 250), 30, 3)
				pygame.draw.circle(self.canvas.get_canvas(), self.rival.color, (40, 250), 30, 3)

			if(flag):
				pesan = self.net.send('status')
				self.canvas.draw_text('Waiting for other player 2 to join', 32, 0, 0, self.bg_contrast)
				print(pesan)
				if(pesan == 'start'):
					print('done')
					flag = 0
					pesan = self.net.client.recv(2048).decode().split(':')[0]
					if(pesan == '0'):
						warna = 'You are the First Player - Red'
						self.turn = 'me'
						self.me.color = ((255, 0, 0))
						self.rival.color = ((0, 0, 255))
					else:
						warna = 'You are the Second Player - Blue'
						self.turn = 'rival'
						self.rival.color = ((255, 0, 0))
						self.me.color = ((0, 0, 255))
					self.canvas.draw_text(pesan, 32, 0, 0, self.bg_contrast)
			else:
				self.canvas.draw_text(warna, 32, 0, 0, self.bg_contrast)
				print('running')
				if(self.turn == 'rival'):
					print('waiting rival')
					self.canvas.draw_text("Waiting rival's turn..", 25, 0, 25, self.bg_contrast)
					self.rival_move = self.parse_data(self.send_data('ask'))
					print('from server', self.rival_move)
					if(self.rival_move != -1):
						self.animate = True
						ganti = self.ambil_biji_rival(self.rival_move, 'rival')
						# check giliran
						if(ganti):
							self.turn = 'me'
				else:
					print('do ur move')
					if (cek):
						self.canvas.draw_text("You reached home, it's your turn again, do your move..", 25, 0, 25, self.bg_contrast)
					else:
						self.canvas.draw_text("It's your turn, make your move..", 25, 0, 25, self.bg_contrast)
					if(event.type == pygame.MOUSEBUTTONDOWN):
						if(self.me.lubang[0].collidepoint(event.pos) and self.me.biji[0] > 0 and self.animate == False):
							self.animate = True
							self.send_data('move:0')
							ganti = self.ambil_biji(0, 'me')
							#check giliran
							cek = 1
							if(ganti):
								self.turn = 'rival'
								cek = 0
							pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
						elif(self.me.lubang[1].collidepoint(event.pos) and self.me.biji[1] > 0 and self.animate == False):
							self.animate = True
							self.send_data('move:1')
							ganti = self.ambil_biji(1, 'me')
							#check giliran
							cek = 1
							if(ganti):
								self.turn = 'rival'
								cek = 0
							pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
						elif(self.me.lubang[2].collidepoint(event.pos) and self.me.biji[2] > 0 and self.animate == False):
							self.animate = True
							self.send_data('move:2')
							ganti = self.ambil_biji(2, 'me')
							#check giliran
							cek = 1
							if(ganti):
								self.turn = 'rival'
								cek = 0
							pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
						elif(self.me.lubang[3].collidepoint(event.pos) and self.me.biji[3] > 0 and self.animate == False):
							self.animate = True
							self.send_data('move:3')
							ganti = self.ambil_biji(3, 'me')
							#check giliran
							cek = 1
							if(ganti):
								self.turn = 'rival'
								cek = 0
							pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
						elif(self.me.lubang[4].collidepoint(event.pos) and self.me.biji[4] > 0 and self.animate == False):
							self.animate = True
							self.send_data('move:4')
							ganti = self.ambil_biji(4, 'me')
							#check giliran
							cek = 1
							if(ganti):
								self.turn = 'rival'
								cek = 0
							pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
						elif(self.me.lubang[5].collidepoint(event.pos) and self.me.biji[5] > 0 and self.animate == False):
							self.animate = True
							self.send_data('move:5')
							ganti = self.ambil_biji(5, 'me')
							#check giliran
							cek = 1
							if(ganti):
								self.turn = 'rival'
								cek = 0
							pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
						elif(self.me.lubang[6].collidepoint(event.pos) and self.me.biji[6] > 0 and self.animate == False):
							self.animate = True
							self.send_data('move:6')
							ganti = self.ambil_biji(6, 'me')
							#check giliran
							cek = 1
							if(ganti):
								self.turn = 'rival'
								cek = 0
							pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

			self.canvas.update()

		pygame.quit()

	def send_data(self, pesan):
		data = str(self.net.id) + ":" + pesan
		reply = self.net.send(data)
		return reply

	def ambil_biji(self, start_pos, giliran):

		# clear biji before
		self.me.draw(self.canvas.get_canvas(), self.bg_color, 95, 280, 52, 22, 0)
		self.rival.draw(self.canvas.get_canvas(), self.bg_color, 95, 220, 52, 22, 0)
		pygame.draw.circle(self.canvas.get_canvas(), self.bg_color, (460, 250), 27, 0)
		pygame.draw.circle(self.canvas.get_canvas(), self.bg_color, (40, 250), 27, 0)

		# gambar kondisi awal
		self.me.draw(self.canvas.get_canvas(), self.me.color, 95, 280, 52, 25, 3)
		self.rival.draw(self.canvas.get_canvas(), self.rival.color, 95, 220, 52, 25, 3)
		for i in range(7):
			self.canvas.draw_text(str(self.me.biji[i]), 32, 85 + (i * 52), 270, self.me.color)
		for i in range(7):
			self.canvas.draw_text(str(self.rival.biji[i]), 32, 85 + (i * 52), 210, self.rival.color)
		self.canvas.draw_text(str(self.me.poin), 32, 450, 240, self.me.color)
		self.canvas.draw_text(str(self.rival.poin), 32, 30, 240, self.rival.color)
		pygame.draw.circle(self.canvas.get_canvas(), self.me.color, (460, 250), 30, 3)
		pygame.draw.circle(self.canvas.get_canvas(), self.rival.color, (40, 250), 30, 3)
		self.canvas.update()

		banyak_biji = self.me.biji[start_pos]
		self.me.biji[start_pos] = 0
		self.add_delay('me biji', start_pos, str(self.me.biji[start_pos]), 'Ambil')

		print('ambil me', banyak_biji, start_pos + 1)
		sisa_biji, cur_pos, player = self.animasi_biji_me(banyak_biji, start_pos + 1, giliran)
		print('back to home', player, cur_pos)
		if(giliran == 'me'):
			if(cur_pos == 7): #reach home
				print('finish animasi me back to home')
				self.animate = False
				return 0 #giliran tetap ketika biji terakhir sampai di home/rumah sendiri
			elif(player == 'me'):
				if(self.me.biji[cur_pos] == 1): #tembak
					self.me.poin += self.rival.biji[cur_pos] + self.me.biji[cur_pos]
					self.add_delay('me poin', cur_pos, str(self.me.poin), str(sisa_biji))
					self.rival.biji[cur_pos] = 0
					self.me.biji[cur_pos] = 0
					print('finish animasi me', cur_pos)
					self.animate = False
				else:
					ganti = self.ambil_biji(cur_pos, giliran)
					return ganti
			else:
				if(self.rival.biji[cur_pos] == 1): #mati
					print('finish animasi rival', cur_pos)
					self.animate = False
				else:
					ganti = self.ambil_biji_rival(cur_pos, giliran)
					return ganti
		else:
			if(cur_pos == -1): #reach home
				print('finish animasi me back to home rival')
				self.animate = False
				return 0 #giliran tetap ke rival ketika biji terakhir sampai di home rival
			elif(player == 'rival'):
				if(self.rival.biji[cur_pos] == 1): #tembak
					self.rival.poin += self.rival.biji[cur_pos] + self.me.biji[cur_pos]
					self.add_delay('rival poin', cur_pos, str(self.rival.poin), str(sisa_biji))
					self.rival.biji[cur_pos] = 0
					self.me.biji[cur_pos] = 0
					print('finish animasi me - rival', cur_pos)
					self.animate = False
				else:
					ganti = self.ambil_biji_rival(cur_pos, giliran)
					return ganti
			else:
				if(self.me.biji[cur_pos] == 1): #mati
					print('finish animasi rival - rival', cur_pos)
					self.animate = False
				else:
					ganti = self.ambil_biji(cur_pos, giliran)
					return ganti
		return 1 #ganti giliran ke lawan

	def ambil_biji_rival(self, start_pos, giliran):

		# clear biji before
		self.me.draw(self.canvas.get_canvas(), self.bg_color, 95, 280, 52, 22, 0)
		self.rival.draw(self.canvas.get_canvas(), self.bg_color, 95, 220, 52, 22, 0)
		pygame.draw.circle(self.canvas.get_canvas(), self.bg_color, (460, 250), 27, 0)
		pygame.draw.circle(self.canvas.get_canvas(), self.bg_color, (40, 250), 27, 0)

		# gambar kondisi awal
		self.me.draw(self.canvas.get_canvas(), self.me.color, 95, 280, 52, 25, 3)
		self.rival.draw(self.canvas.get_canvas(), self.rival.color, 95, 220, 52, 25, 3)
		for i in range(7):
			self.canvas.draw_text(str(self.me.biji[i]), 32, 85 + (i * 52), 270, self.me.color)
		for i in range(7):
			self.canvas.draw_text(str(self.rival.biji[i]), 32, 85 + (i * 52), 210, self.rival.color)
		self.canvas.draw_text(str(self.me.poin), 32, 450, 240, self.me.color)
		self.canvas.draw_text(str(self.rival.poin), 32, 30, 240, self.rival.color)
		pygame.draw.circle(self.canvas.get_canvas(), self.me.color, (460, 250), 30, 3)
		pygame.draw.circle(self.canvas.get_canvas(), self.rival.color, (40, 250), 30, 3)
		self.canvas.update()

		banyak_biji = self.rival.biji[start_pos]
		self.rival.biji[start_pos] = 0
		self.add_delay('rival biji', start_pos, str(self.rival.biji[start_pos]), 'Ambil')
		print('ambil rival', banyak_biji, start_pos - 1)
		sisa_biji, cur_pos, player = self.animasi_biji_rival(banyak_biji, start_pos - 1, giliran)
		print('back to rival', player, cur_pos)
		if(giliran == 'me'):
			if(cur_pos == 7): #reach home
				print('finish animasi me back to home')
				self.animate = False
				return 0 #giliran tetap ketika biji terakhir sampai ke home/rumah sendiri
			elif(player == 'me'):
				if(self.me.biji[cur_pos] == 1): #tembak
					self.me.poin += self.rival.biji[cur_pos] + self.me.biji[cur_pos]
					self.add_delay('me poin', cur_pos, str(self.me.poin), str(sisa_biji))
					self.rival.biji[cur_pos] = 0
					self.me.biji[cur_pos] = 0
					print('finish animasi me', cur_pos)
					self.animate = False
				else:
					ganti = self.ambil_biji(cur_pos, giliran)
					return ganti
			else:
				if(self.rival.biji[cur_pos] == 1): #mati
					print('finish animasi rival', cur_pos)
					self.animate = False
				else:
					ganti = self.ambil_biji_rival(cur_pos, giliran)
					return ganti
		else:
			if(cur_pos == -1): #reach home
				print('finish animasi me back to home rival')
				self.animate = False
				return 0 #giliran tetap ke rival ketika biji terakhir sampai ke home rival
			elif(player == 'rival'):
				if(self.rival.biji[cur_pos] == 1): #tembak
					self.rival.poin += self.rival.biji[cur_pos] + self.me.biji[cur_pos]
					self.add_delay('rival poin', cur_pos, str(self.rival.poin), str(sisa_biji))
					self.rival.biji[cur_pos] = 0
					self.me.biji[cur_pos] = 0
					print('finish animasi me - rival', cur_pos)
					self.animate = False
				else:
					ganti = self.ambil_biji_rival(cur_pos, giliran)
					return ganti
			else:
				if(self.me.biji[cur_pos] == 1): #mati
					print('finish animasi rival - rival', cur_pos)
					self.animate = False
				else:
					ganti = self.ambil_biji(cur_pos, giliran)
					return ganti
		return 1 #giliran ganti ke lawan


	def animasi_biji_me(self, banyak_biji, start_pos, giliran):
		cur_pos = start_pos
		sisa_biji = banyak_biji
		player = 'me'
		if(cur_pos == 7 and sisa_biji > 0):
			if(giliran == 'me'):
				self.me.poin += 1
				sisa_biji -= 1
				self.add_delay('me poin', cur_pos, str(self.me.poin), str(sisa_biji))
				if(sisa_biji == 0):
					return 0, cur_pos, 'me'
			sisa_biji, cur_pos, player = self.animasi_biji_rival(sisa_biji, 6, giliran)
		else:
			while(sisa_biji):
				print('animasi me', cur_pos, sisa_biji)
				self.me.biji[cur_pos] += 1
				sisa_biji -= 1
				self.add_delay('me biji', cur_pos, str(self.me.biji[cur_pos]), str(sisa_biji))
				if(sisa_biji == 0):
					return 0, cur_pos, 'me'
				cur_pos += 1
				if(cur_pos == 7 and sisa_biji > 0):
					if(giliran == 'me'):
						self.me.poin += 1
						sisa_biji -= 1
						self.add_delay('me poin', cur_pos, str(self.me.poin), str(sisa_biji))
						if(sisa_biji == 0):
							return 0, cur_pos, 'me'
						print('mau pindah ke rival', sisa_biji, cur_pos)
					sisa_biji, cur_pos, player = self.animasi_biji_rival(sisa_biji, 6, giliran)
		return sisa_biji, cur_pos, player

	def animasi_biji_rival(self, banyak_biji, start_pos, giliran):
		cur_pos = start_pos
		sisa_biji = banyak_biji
		player = 'rival'
		if(cur_pos == -1 and sisa_biji > 0):
			if(giliran == 'rival'):
				self.rival.poin += 1
				sisa_biji -= 1
				self.add_delay('rival poin', cur_pos, str(self.rival.poin), str(sisa_biji))
				if(sisa_biji == 0):
					return 0, cur_pos, 'rival'
			sisa_biji, cur_pos, player = self.animasi_biji_me(sisa_biji, 0, giliran)
		else:
			while(sisa_biji):
				print('animasi rival', cur_pos, sisa_biji)
				self.rival.biji[cur_pos] += 1
				sisa_biji -= 1
				self.add_delay('rival biji', cur_pos, str(self.rival.biji[cur_pos]), str(sisa_biji))
				if(sisa_biji == 0):
					return 0, cur_pos, 'rival'
				cur_pos -= 1
				if(cur_pos == -1 and sisa_biji > 0):
					if(giliran == 'rival'):
						self.rival.poin += 1
						sisa_biji -= 1
						self.add_delay('rival poin', cur_pos, str(self.rival.poin), str(sisa_biji))
						if(sisa_biji == 0):
							return 0, cur_pos, 'rival'
						print('oper to me', 0, sisa_biji);
					sisa_biji, cur_pos, player = self.animasi_biji_me(sisa_biji, 0, giliran)
		return sisa_biji, cur_pos, player

	def add_delay(self, player, pos, text, sisa_biji):
		# time.sleep(1)
		# using pygame.time.delay will make Pygame not responding, better use ticks
		# pygame.time.delay(250)
		ticks = pygame.time.get_ticks()
		delay_ticks = ticks + 10000
		while(ticks > delay_ticks):
			ticks = pygame.time.get_ticks()
		self.canvas.screen.fill(self.bg_color, (0, 0, 500, 100))
		self.canvas.update_text(sisa_biji, 32, 0, 0, (self.bg_contrast))
		if(player == 'me biji'):
			pygame.draw.circle(self.canvas.get_canvas(), self.on_color, ((95 + pos * 52), 280), 22)
			self.canvas.update_text(text, 32, 85 + (pos * 52), 270, self.me.color)
		elif(player == 'me poin'):
			pygame.draw.circle(self.canvas.get_canvas(), self.on_color, (460, 250), 27)
			self.canvas.update_text(text, 32, 450, 240, self.me.color)
		elif(player == 'rival biji'):
			pygame.draw.circle(self.canvas.get_canvas(), self.on_color, ((95 + pos * 52), 220), 22)
			self.canvas.update_text(text, 32, 85 + (pos * 52), 210, self.rival.color)
		else:
			pygame.draw.circle(self.canvas.get_canvas(), self.on_color, (40, 250), 27)
			self.canvas.update_text(text, 32, 30, 240, self.rival.color)

		self.canvas.update()

	@staticmethod
	def parse_data(data):
		try:
			d = data.split(":")[0]
			return int(d)
		except:
			return -1


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
		if(len(text) == 1):
			x += 5
		font = pygame.font.SysFont("comicsans", size)
		render = font.render(text, 1, color)

		self.screen.blit(render, (x,y))

	def update_text(self, text, size, x, y, color):
		pygame.font.init()
		if(len(text) == 1):
			x += 5
		font = pygame.font.SysFont("comicsans", size)
		# self.screen.fill(pygame.Color("white"), ((x-5), (y-1), 29, 26))
		render = font.render(text, 1, color)

		self.screen.blit(render, (x,y))

	def get_canvas(self):
		return self.screen

	def draw_background(self):
		self.screen.fill((0,0,0))

	def draw_image(self, image, position):
		self.screen.blit(image, position)