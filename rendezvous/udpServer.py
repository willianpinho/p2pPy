import socket
from rendezvous import *

rendezvous = Rendezvous(5)

ip = ''                                                             # Enderecos que podem se conectar ao servidor
port = 5000                                                         # porta que o servidor esta escutando

udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)              # Define o tipo da familia do protocolo e o tipo de Socket, nesse caso, UDP
origen = (ip, port)                                                 # Tupla contendo o host e a porta do servidor
udp.bind(origen)                                                    # Esperara conexoes no endereco e porta fornecidos

while True:
    message, client = udp.recvfrom(1024)                            # Recebe um dado de ate 1024 bytes retorna tambem o endereco de quem enviou

    if message == 'hello':
        idDHT = rendezvous.pickRandomEmptyID()

        if idDHT >= 0:
            print client, message
            udp.sendto('ID = ' + str(idDHT) , client)

            # recebeu ACK entao aloca pro carinha
            rendezvous.allocIDForCliente(idDHT, client)
        else:
            udp.sendto('no slot avaiable', client)

    elif message == 'root node':
        root = rendezvous.getRootNodeIPAndPort()
        if root == client[0] + ':' + str(client[1]):
            udp.sendto('you are the root', client)
        else:
            udp.sendto(root, client)

    elif message == 'disconnect':
        rendezvous.disconnectNode(client[0], client[1])
        udp.sendto('disconnected', client)

    else:
        udp.sendto('unknown message, try again', client)

udp.close()                                                         # Encerra a conexao
