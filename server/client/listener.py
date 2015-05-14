#/usr/bin/env python

# create a socket that listens for incoming connections
import socket


 class Listener:
    def __init__(self,port=0):
        self.HOST = ''
        self.PORT = port

    def startsocket(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.HOST,self.PORT))

    def runsocket(self, num=1):
        while True:
            (client,addr) = self.socket.accept()
            self.handle(client, addr)

    def handle(self, client, addr):
        print "Message received from %s" % str(addr)
        print "Socket used: %s" % str(client)
