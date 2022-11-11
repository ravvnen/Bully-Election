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
    return port

def ID_generator(idList):
    ID = random.randint(0,50)

    if ID not in idList:
        idList.append(ID)
    else:
        ID_generator(idList)
    return ID

# THIS NEEDS TO BE UPDATED 
def update_state(node):
        if node.state != "Candidate" and "Leader":
            node.state = "Follower"
        return node.state

# print function to show the network
def visualize(nodeList):
        for n in range(len(nodeList)):
            print("node",n,": ip =", nodeList[n].iP,"ID =", nodeList[n].ID, ", Port =", nodeList[n].myPort, ", State =", nodeList[n].state, "\n")

            if n + 1 == len(nodeList):
                print("portList : ", nodeList[n].portList)

def create_network(N):
        nodeList = []
        iPList = []
        for n in range(N):
            iPList.append(socket.inet_ntoa(struct.pack('>I', 0x7f000001+n))) #0.0.0.0, 127.000.000.000 255.255.255.255
        #initialization of nodes in the network
        for n in range(N):
            nodeList.append(Node(iPList[n],iPList ,ID = ID_generator(idList), myPort = port_generator(portList), portList = portList, state = "Follower"))
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
    def __init__(self, iP, iPList , ID, myPort, portList, state):
        #threading.Thread.__init__(self)
        Process.__init__(self)
        self.listener_thread = threading.Thread(target=self.recieve_message,args=())
        self.responser_tread = threading.Thread(target=self.loopSending,args=())
        
        self.iP = iP
        self.iPList = iPList
        self.ID = ID
        self.myPort = myPort
        self.portList = portList
        self.state = state

        #Setting up sockets
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) #kan være socket skal have en andet navn?
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        #Binding
        self.socket.bind((self.iP,self.myPort))

        self.listener_thread.start()
        self.responser_tread.start()

    def __del__(self):
        #Process.__del__(self)
        print('Destructor called, Closes socket')
        self.socket.close()
        self.listener_thread.join()
        self.responser_tread.join()
    
    def send(self,Id):
        msg = "Message"
        byteToSend = str.encode(msg)
        print(self.portList)
        self.socket.sendto(byteToSend, (self.iPList[Id-1],self.portList[Id-1]))#test
        print("message send")

    def recieve_message(self):
        bytesAddressPair = self.socket.recv(1024) #bufferSize  = 1024
        address = bytesAddressPair[1]
        revieveMsg = bytesAddressPair[0]
        print("Besked fået",revieveMsg)

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
    #print(nodeList)
    #join(nodeList)
    visualize(nodeList)