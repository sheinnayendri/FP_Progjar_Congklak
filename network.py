import socket
import sys
from threading import Thread

class Network:

	def __init__(self):
		self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.host = '127.0.0.1'
		self.port = 5555
		self.addr = (self.host, self.port)
		self.id = self.connect()
		# self.start_thread()

	def connect(self):
		self.client.connect(self.addr)
		return self.client.recv(2048).decode() 

	def send(self, data):
		"""
		:param data: str
		:return: str
		"""
		try:
			self.client.send(str.encode(data))
			reply = self.client.recv(2048).decode()
			return reply.split(':')[0]
		except socket.error as e:
			print(str(e))
			# return str(e)

	# def send_msg(self, sock):
	# 	while True:
	# 		data = sys.stdin.readline()
	# 		sock.send(data.encode())
	# 		# server.send(message.encode())
	# 		sys.stdout.write('<You>')
	# 		sys.stdout.write(data)
	# 		sys.stdout.flush()

	# def recv_msg(self, sock):
	# 	try:
	# 		data = sock.recv(2048).decode().split(':')[0]
	# 		print(data)
	# 		return data
	# 	except socket.error as e:
	# 		return str(e)

	# def start_thread(self):
	# # 	Thread(target=self.send_msg, args=(self.client,)).start()  
	# 	Thread(target=self.recv_msg, args=(self.client,)).start()