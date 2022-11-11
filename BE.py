import logging
import random
import socket
import struct
import subprocess
import sys
import threading
import time
from enum import Enum
from multiprocessing import Process


def port_generator(portList):
    port = random.randint(5000,6000)
    if port not in portList:
        portList.append(port)
    else:
        port_generator(portList)

def ID_generator(idList):
    ID = random.randint(0,50)

    if ID not in idList:
        idList.append(ID)
    else:
        ID_generator(idList)

def IP_generator(ipList):
    n = len(ipList)
    IP = socket.inet_ntoa(struct.pack('>I', 0x7f000010+n)) #0.0.0.0, 127.000.000.000 255.255.255.255
    ipList.append(IP)

# THIS NEEDS TO BE UPDATED 
def update_state(node):
        if node.state != "Candidate" and "Leader":
            node.state = "Follower"
        return node.state

# print function to show the network
def visualize(nodeList):
        for n in range(len(nodeList)):
            print("node",n,": ip =", nodeList[n].IP,"ID =", nodeList[n].ID, ", Port =", nodeList[n].myPort, ", State =", nodeList[n].state, "\n")

            if n + 1 == len(nodeList):
                print("portList : ", nodeList[n].portList)

def create_network(N):
        portList = []
        nodeList = []
        ipList = []
        idList = []

        for n in range(N):
            port_generator(portList)
            ID_generator(idList)
            IP_generator(ipList)


        print(len(portList))
        print(len(idList))
        print(len(ipList))

        #initialization of nodes in the network
        for n in range(N):
            nodeList.append(Node(IP = ipList[n],ipList = ipList ,ID = idList[n], idList = idList, myPort = portList[n], portList = portList, state = "Follower"))
            print(len(portList[n]))
            print(len(idList[n]))
            print(len(ipList[n]))
            nodeList[n].start()

            

        # setting a random node as the first leader
        index = random.randint(0,N-1)
        nodeList[index].state = "Leader"
            
        return nodeList

def join(nodeList):
    for n in range(len(nodeList)):
        nodeList[n].join()

class Node(Process):
    # each node is initialized with these given attributes
    def __init__(self, IP, ipList , ID, idList, myPort, portList, state):
        #threading.Thread.__init__(self)
        Process.__init__(self)
        self.listener_thread = threading.Thread(target=self.receive_message,args=())
        self.responder_thread = threading.Thread(target=self.loopSending,args=())
        
        self.IP = IP
        self.ipList = ipList
        self.ID = ID
        self.idList = idList
        self.myPort = myPort
        self.portList = portList
        self.state = state

        #Setting up sockets
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) #kan være socket skal have en andet navn?
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        #Binding
        self.socket.bind((self.IP,self.myPort))

    def __del__(self):
        #Process.__del__(self)
        print('Destructor called, Closes socket')
        self.socket.close()
        #self.listener_thread.join()
        #self.responder_thread.join()
    
    def send(self,ID):
        msg = "Message"
        byteToSend = str.encode(msg)
        print(self.portList)
        self.socket.sendto(byteToSend, (self.ipList[ID-1],self.portList[ID-1]))#test
        print("message send")

    def receive_message(self):
        bytesAddressPair = self.socket.recv(1024) #bufferSize  = 1024
        address = bytesAddressPair[1]
        receiveMsg = bytesAddressPair[0]
        print("Besked fået",receiveMsg)

    def loopSending(self):
        c = 0
        while True:
            if c == 3:
                break
            self.send(c)
            c += 1


if __name__ == "__main__":
    idList = []
    portList = []
    nodeList = create_network(3)
    visualize(nodeList)
    #print(nodeList)
    #join(nodeList)