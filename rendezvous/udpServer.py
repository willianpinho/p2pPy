import socket
import thread
from rendezvous import *

def newThread(message, client):
    if message == 'hello':
        idDHT = rendezvous.pickRandomEmptyID(client[0], client[1])

        ipThread = ''                                                       # Enderecos que podem se conectar ao servidor
        portThread = 50000 + idDHT                                                   # porta que o servidor esta escutando
        udpThread = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)              # Define o tipo da familia do protocolo e o tipo de Socket, nesse caso, UDP
        origenThread = (ipThread, portThread)                                                 # Tupla contendo o host e a porta do servidor
        udpThread.bind(origenThread)                                                    # Esperara conexoes no endereco e porta fornecidos

        if idDHT >= 0:
            print client, message
            udpThread.sendto('ID = ' + str(idDHT) , client)

            # recebeu ACK entao aloca pro carinha
            rendezvous.allocIDForCliente(idDHT, client)
        else:
            udpThread.sendto('no slot avaiable', client)

    elif message == 'root node':
        root = rendezvous.getRootNodeIPAndPort()
        if root == client[0] + ':' + str(client[1]):
            udpThread.sendto('you are the root', client)
        else:
            udpThread.sendto(root, client)

    elif message == 'disconnect':
        rendezvous.disconnectNode(client[0], client[1])
        udpThread.sendto('disconnected', client)

    else:
        udpThread.sendto('unknown message, try again', client)


    thread.exit()

rendezvous = Rendezvous(5)

ip = ''                                                             # Enderecos que podem se conectar ao servidor
port = 5000                                                         # porta que o servidor esta escutando

udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)              # Define o tipo da familia do protocolo e o tipo de Socket, nesse caso, UDP
origen = (ip, port)                                                 # Tupla contendo o host e a porta do servidor
udp.bind(origen)                                                    # Esperara conexoes no endereco e porta fornecidos

while True:
    message, client = udp.recvfrom(1024)                            # Recebe um dado de ate 1024 bytes retorna tambem o endereco de quem enviou
    thread.start_new_thread(newThread, (message, client))

udp.close()                                                         # Encerra a conexao
