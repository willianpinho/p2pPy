from random import randint


class Rendezvous(object):
    arrayWithAllocedIDs = []
    arrayWithEmptyIDs = []
    rootNodeID = -1

    def __init__(self, k):
        for i in range(0, k):
            self.arrayWithEmptyIDs.append(i)

    def pickRandomEmptyID(self):
        if len(self.arrayWithEmptyIDs) > 0:
            pos = randint(0, len(self.arrayWithEmptyIDs)-1)
            return self.arrayWithEmptyIDs[pos]
        else:
            return -1

    def allocIDForCliente(self, idDHT, client):  # client = ('IP', porta)
        self.arrayWithEmptyIDs.remove(idDHT)
        self.arrayWithAllocedIDs.append((idDHT, client))

        if len(self.arrayWithAllocedIDs) == 1:
            self.rootNodeID = idDHT

    def getRootNodeIPAndPort(self):
        if len(self.arrayWithAllocedIDs) == 0:
            return 'no root yet'
        for (idDHT, (ip, port)) in self.arrayWithAllocedIDs:
            if idDHT == self.rootNodeID:
                return ip + ':' + str(port)

    def disconnectNode(self, ip, port):
        for (idDHT, (ip2, port2)) in self.arrayWithAllocedIDs:
            if (ip == ip2) and (port == port2) :
                self.arrayWithAllocedIDs.remove((idDHT, (ip2, port2)))
                self.arrayWithEmptyIDs.append(idDHT)

                #check se nao era o root node, se for tem que sortear outro
                if self.rootNodeID == idDHT:
                    if len(self.arrayWithAllocedIDs) > 0:
                        (idDHT, (ip2, port2)) = self.arrayWithAllocedIDs[0]
                        self.rootNodeID = idDHT
                break
