import logging, threading, sys, socket, struct, time

class node(threading.Thread):
    
    def __init__(self,ip, ports, iD, othersId,othersIp):
        #self.host = hosts #andres host
        threading.Thread.__init__(self)
        self.ip = ip
        self.ports = ports
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) #kan være socket skal have en andet navn?
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.iD = iD
        self.othersId = othersId #liste med andres Ids.
        self.othersIp = othersIp
        self.socket.bind((self.ip,self.ports[iD-1]))
        print(iD,self.ports[iD-1])
        #self.send(len(othersId))
    
    #Brug pattern matching til at finde ud af hvilken message man modtager.
    
    
    #Connect to all other nodes
    #def bind(self):
    #    self.socket.bind((self.ip,self.port)) # Bind to address and ip
    
    
    #Send message function
    def send(self,nodeNr):
        msg = "Message"
        byteToSend = str.encode(msg)
        self.socket.sendto(byteToSend, (self.othersIp[nodeNr-1],self.ports[nodeNr-1]))
        print("message send")
    
    def recieve_message(self):
        bytesAddressPair = self.socket.recv(1024) #bufferSize  = 1024
        address = bytesAddressPair[1]
        revieveMsg = bytesAddressPair[0]
        print(revieveMsg)

    def startElection(self): #Kode der starter en election på en node.
        print(3)

    def bullyAlgorithm(self):
        print(2)

    def __del__(self):
        print('Destructor called, Closes socket')
        self.socket.close()
            

if __name__ == "__main__":
    localIPlist = ["127.0.0.1","127.0.0.2"]
    localPorts = [20002,20003]    #0-65535
    
    node1 = node(localIPlist[0],localPorts,1,[2],localIPlist)#threading.Thread(target=node, args=(localIPlist[0],localPort,1,[2],["127.0.0.2"]))
    node2 = node(localIPlist[1],localPorts,2,[1],localIPlist)#threading.Thread(target=node, args=(localIPlist[1],localPort,2,[1],["127.0.0.1"]))
    print("john")
    #make threads
    node1.start()
    node2.start()
    counter = 0
    while True:
        if (counter > 100):
            break
        print("hello")
        #node1.recieve_message()
        print("John2")
        node1.send(2)
        node2.recieve_message()
        counter += 1
    node1.join()
    node2.join()