"""
Lucas Terranova - RA: 19059328
Luiz Caiado - RA: 19028422
"""

import socket
import select
import sys
from _thread import *

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# verifica se foram passados argumentos suficientes
if len(sys.argv) != 3:
	print("Argumentos incorretos. Favor informar: script, IP, porta")
	exit()

# pega o primeiro argumento passado como um endereço IP
IP_address = str(sys.argv[1])

# pega o segundo valor passado (porta)
Port = int(sys.argv[2])


# faz a associação do servidor com o endereço IP e a porta informados
server.bind((IP_address, Port))

# ouve 100 conexões ativas, podendo aumentar ou diminuir
server.listen(100)

list_of_clients = []

def clientthread(conn, addr):

    # envia a mensagem para o client (conn)
	conn.send(("Seja bem vindo!").encode())

	while True:
			try:
				message = (conn.recv(2048)).decode()
				if message:
					# printa a messagem e o endereço do usuário que enviou a mensagem no terminal do servidor
					print(f"<{addr[0]}> {message}")

                    # chama função broadcast para enviar a mensagem para todos os clients 
					message_to_send = f"<{addr[0]}> {message}"
					broadcast(message_to_send, conn)

				else:
					#a mensagem pode não ter conteúdo se a conexão for quebrada então a gente remove a conexão aqui
					remove(conn)

			except:
				continue

# envia a mensagem para todos os clients cujo objeto não seja o que enviou a mensagem
def broadcast(message, connection):
	for clients in list_of_clients:
		if clients!=connection:
			try:
				clients.send(message.encode())
			except:
				clients.close()

                # se a conexão com o servidor for interrompida, o cliente é removido
				remove(clients)

# remove um objeto da lista
def remove(connection):
	if connection in list_of_clients:
		list_of_clients.remove(connection)

while True:

    # aceita a conexão e guarda o objeto conn e o IP do client
	conn, addr = server.accept()

	# mantém uma lista dos clientes para faciliatar o broadcasting de mensagem para todas as pessoas no chatroom
	list_of_clients.append(conn)

	# imprime os IPs do usuário recém conectado
	print (addr[0] + " connected")

	# cria uma thread individual para cada usuário que conectar
	start_new_thread(clientthread,(conn,addr))	

conn.close()
server.close()
