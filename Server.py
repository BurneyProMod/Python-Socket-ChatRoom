#Server.py
import socket 
import select 
import sys 
from threading import *
import json
  
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
  
# checks whether sufficient arguments have been provided 
if len(sys.argv) != 3: 
    print("File, IP, Port")
    exit() 
# takes the first argument from command prompt as IP address 
IP_address = str(sys.argv[1]) 
# takes second argument from command prompt as port number 
Port = int(sys.argv[2]) 
server.bind((IP_address, Port)) 
#listens for 10 active connections.
server.listen(10) 
 
# Make a list for connected clients and their respective threads
clientlist=[]
threads = []

def clientthread(conn, addr):
    conn.send("Welcome to Nicholas Burney's CMPS 413 Final Project.")
    while True:
            try:     
                message = conn.recv(2048)    
                #prints the message and address of the user who just sent the message on the server terminal
                if message:
                    print("<" + addr[0] + "> " + message)
                    message_to_send = "<" + addr[0] + "> " + message
                    broadcast(message_to_send,conn)
                else:
                    remove(conn)
            except:
                continue

#Send message to all clients in client list
def broadcast(message,connection):
    for clients in clientlist:
        if clients!=connection:
            try:
                clients.send(message)
            except:
                clients.close()
                remove(clients)

''' Remove client from client list '''
def remove(connection):
    if connection in clientlist:
        clientlist.remove(connection)

while True:
    """
    Accepts a connection request and stores two parameters, conn which is a socket object for that user, and addr which contains
    the IP address of the client that just connected
    """
    conn, addr = server.accept()
    #maintains a list of clients for ease of broadcasting a message to all available people in the chatroom
    clientlist.append(conn)

    #Prints the address of the person who just connected
    print(addr[0] + " connected")

    #creates and individual thread for every user that connects
    newthread = (clientthread,(conn,addr))
    newthread[0].start()
    threads.append(newthread)
conn.close()
server.close()
