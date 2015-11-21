import socket
import json

host = 'localhost'                                          # ip do servidor
port = 5000                                                 # porta do servidor

udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)      # conexao UDP

destination = (host, port)                                  # tupla com IP:porta

message = raw_input()

while message != 'end':
    messageJSON = json.dumps(message)
    udp.sendto(message, destination)                       # envia a mensagem para o servidor
    messageFromServer, client = udp.recvfrom(1024)
    print client, messageFromServer
    message = raw_input()

udp.close()
