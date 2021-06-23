from math import fabs
import socket
from _thread import *
import random
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server = 'localhost'
port = 5555

list_of_clients = []
server_ip = socket.gethostbyname(server)

try:
	s.bind((server, port))

except socket.error as e:
	print(str(e))

s.listen(2)
print("Waiting for a connection")

def check_status():
	if (len(list_of_clients) == 1):
		return 'waiting:'
	elif (len(list_of_clients) == 2):
		return 'start:'


pesan = ['0:', '1:']
# random_done = False
# warna = []

# def check_player(id):
# 	if(random_done == False):
# 		cur = random.randint(0, 1)
# 		warna.append(cur)
# 		warna.append(cur ^ 1)
# 		random_done = True
# 	return warna[id]


currentId = "0"
pos = ["0:50,50", "1:100,100"]
def clientthread(conn, addr):
	global currentId, pos
	conn.send(str.encode(currentId))
	currentId = "1"
	reply = ''
	while True:
		try:
			data = conn.recv(2048)
			reply = data.decode('utf-8')
			print('Received:', reply)
			if not data:
				conn.send(str.encode("Goodbye"))
				break
			else:
				if(reply == 'status'):
					reply = check_status()
					print(reply)
					conn.send(reply.encode())
					if(reply == 'start:'):
						if(conn == list_of_clients[0]):
							conn.send(pesan[0].encode())
						else:
							conn.send(pesan[1].encode())
						# print(cur)
						# conn.send(pesan[cur].encode())
						# broadcast(pesan[cur ^ 1], conn)
				# print("Recieved: " + reply)
				# arr = reply.split(":")
				# id = int(arr[0])
				# pos[id] = reply

				# if id == 0: nid = 1
				# if id == 1: nid = 0

				# reply = pos[nid][:]
				# print("Sending: " + reply)

			# conn.sendall(str.encode(reply))
		except:
			break

	print("Connection Closed")
	conn.close()

def broadcast(message, connection):
	for clients in list_of_clients:
		if clients != connection:
			try:
				clients.send(message.encode())
			except:
				clients.close()
				remove(clients)

def remove(connection):
	if connection in list_of_clients:
		list_of_clients.remove(connection)

while True:
	conn, addr = s.accept()
	list_of_clients.append(conn)
	print("Connected to: ", addr)

	start_new_thread(clientthread, (conn, addr))

	# threading.Thread(target=clientthread, args=(conn, addr)).start()
	# if(len(list_of_clients) == 1):
	# 	pesan = 'menunggu pemain kedua...\n'
	# 	print(pesan)
	# 	conn.send(pesan.encode())
	# elif(len(list_of_clients) == 2):
	# 	pertama = random.randint(0,1)
	# 	first_player = pertama
	# 	pesan1 = 'kamu merupakan pemain pertama: MERAH\nsilahkan pilih petak\n'
	# 	list_of_clients[pertama].send(pesan1.encode())
	# 	pesan1 = 'id 0\n'
	# 	list_of_clients[pertama].send(pesan1.encode())
		
	# 	pesan2 = 'kamu merupakan pemain kedua: BIRU\nmenunggu langkah pemain pertama\n'
	# 	list_of_clients[pertama ^ 1].send(pesan2.encode())
	# 	pesan2 = 'id 1\n'
	# 	list_of_clients[pertama ^ 1].send(pesan2.encode())