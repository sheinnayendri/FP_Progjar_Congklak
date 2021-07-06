from math import fabs
import socket
from _thread import *
import random
import sys
import os

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server = 'localhost'
port = 5555

list_of_clients = []
username = {}
poin = {}
leaderboard = {}
server_ip = socket.gethostbyname(server)

try:
	s.bind((server, port))

except socket.error as e:
	print(str(e))

s.listen(2)
print("Waiting for a connection")

def registered():
	for i in range(len(list_of_clients)):
		if i not in username.keys():
			return False
	return True


def check_status():
	if (len(list_of_clients) == 1):
		return 'waiting:'
	elif (len(list_of_clients) == 2 and registered()):
		partner = username[0] + ':' + username[1] + ':'
		return 'start:' + partner
	else:
		return 'waiting:'


cur = random.randint(0, 1)
if(cur == 0):
	pesan = ['0:', '1:']
else:
	pesan = ['1:', '0:']

filename = 'leaderboard.txt'
with open(filename, "r") as in_file:
	if os.stat(filename).st_size == 0:
		cek = 1
	else:
		buf = in_file.readlines()
		for line in buf:
			lines = line.strip()
			poin_now = int(lines.split(':')[1].strip())
			user_now = lines.split(':')[0]
			leaderboard[user_now] = poin_now
in_file.close()


currentId = "0"
cur_pos = [-1, -1]
ack = [0, 0]
update = [0, 0]
def clientthread(conn, addr):
	global currentId, pos
	conn.send(str.encode(currentId))
	currentId = "1"
	reply = ''
	while True:
		try:
			data = conn.recv(2048)
			reply = data.decode()
			print('Received:', reply)
			if (reply == ''):
				print('goodbye')
				conn.send(str.encode("Goodbye"))
				break
			else:
				print('else')
				if(reply == 'status'):
					print('statussss')
					reply = check_status()
					print(reply)
					conn.send(reply.encode())
					if(reply.split(':')[0] == 'start'):
						if(conn == list_of_clients[0]):
							msg = pesan[0] + reply[6:]
							conn.send(msg.encode())
						else:
							msg = pesan[1] + reply[6:]
							conn.send(msg.encode())
				elif(reply.split(':')[1] == 'move'):
					print('moveeeeeeeee')
					id = int(reply.split(':')[0])
					cur_pos[id] = 6 - int(reply.split(':')[2])
					ack[id] = 1
					msg = 'ack:'
					conn.send(msg.encode())
				elif(reply.split(':')[1] == 'ask'):
					print('askkkkkk')
					id = int(reply.split(':')[0])
					ack[id] = 0
					print('ask', id)
					if(ack[id ^ 1]):
						msg = str(cur_pos[id ^ 1]) + ':'
						ack[id ^ 1] = 0
					else:
						msg = '-1:'
					conn.send(msg.encode())
				elif(reply.split(':')[1] == 'register'):
					print('registering username')
					id = int(reply.split(':')[0])
					username[id] = reply.split(':')[2]
					msg = 'ack:'
					conn.send(msg.encode())
				elif(reply.split(':')[1] == 'score'):
					print('scoring')
					id = int(reply.split(':')[0])
					poin[id] = reply.split(':')[2]
					msg = 'ack:'
					conn.send(msg.encode())
					print(username[id] + ': ' + poin[id] + '\n')
					filename = "leaderboard.txt"
					cek = 0
					find = 0

					for key, value in leaderboard.items():
						print(key, value, 'unsorted')
						if(key == username[id]):
							find = 1
							if(int(poin[id]) > value):
								other_dict = {}
								other_dict[username[id]] = int(poin[id])
								leaderboard.update(other_dict)
								print('updated')
					# add new username on leaderboard
					if(find == 0):
						other_dict = {}
						other_dict[username[id]] = int(poin[id])
						leaderboard.update(other_dict)
						
					update[id] = 1

					if(update[0] == 1 and update[1] == 1):
						print('updated both')
						sorted_leaderboard = dict(sorted(leaderboard.items(), key=lambda x: x[1], reverse=True))
						print('sorted')
						for key, value in sorted_leaderboard.items():
							print(key, value, 'sorted')
						with open(filename, "w") as out_file:
							if(cek):
								out_file.write(username[id] + ': ' + poin[id] + '\n')
							else:
								for key, value in sorted_leaderboard.items():
									text = key + ': ' + str(value) + '\n'
									print(key, str(value), 'sorted write')
									out_file.write(text)
						out_file.close()
				else:
					print('hehehehe')
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