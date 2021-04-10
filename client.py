"""
Lucas Terranova - RA: 19059328
Luiz Caiado - RA: 19028422
"""

import socket
import select
import sys

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if len(sys.argv) != 3:
	print ("Correct usage: script, IP address, port number")
	exit()
IP_address = str(sys.argv[1])
Port = int(sys.argv[2])
server.connect((IP_address, Port))

while True:

	# mantém uma lista de possívels streams de input
	sockets_list = [sys.stdin, server]

	"""
	Existem duas possibilidades de input. Ou o usuário quer enviar input para outras pessoas,
	ou o servidor está mandando uma mensagem para ser printada na tela. Por exemplo, se o servidor quer enviar a mensagem
	a condição if vai ser true, agora se o usuário quiser mandar mensagem, a condição else vai ser true.
	"""
	read_sockets,write_socket, error_socket = select.select(sockets_list,[],[])

	for socks in read_sockets:
		if socks == server:
			message = (socks.recv(2048)).decode()
			print (message)
		else:
			message = sys.stdin.readline()
			server.send(message.encode())
			sys.stdout.write("<You>")
			sys.stdout.write(message)
			sys.stdout.flush()
server.close()
