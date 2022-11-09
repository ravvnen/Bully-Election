import logging, threading, sys, socket, struct, time
import subprocess
import random
from enum import Enum

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
            print("node",n,": ID =", nodeList[n].ID, ", Port =", nodeList[n].myPort, ", State =", nodeList[n].state, "\n")

            if n + 1 == len(nodeList):
                print("portList : ", nodeList[n].portList)

class Bully():
    # each node is initialized with these given attributes
    def __init__(self, ID, myPort, portList, state):
        threading.Thread.__init__(self)
        self.ID = ID
        self.myPort = myPort
        self.portList = portList
        self.state = state
    	
    
    def create_network(N):
        nodeList = []

        #initialization of nodes in the network
        for n in range(N):        
            nodeList.append(Bully(ID = ID_generator(idList), myPort = port_generator(portList), portList= portList, state = "Follower"))

        # setting a random node as the first leader
        index = random.randint(0,N)
        nodeList[index].state = "Leader"
            
        return nodeList


if __name__ == "__main__":
    idList = []
    portList = []
    nodeList = Bully.create_network(20)
    visualize(nodeList)
