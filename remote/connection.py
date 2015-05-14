#!/usr/bin/python

from multiprocessing import Process
from multiprocessing.connection import Listener, Client
import time
import messaging

global HOST_PORT, CLIENT_PORT
HOST_PORT = 22158
CLIENT_PORT = 22159

class GameConnection:
    def __init__(self, tag):
        self.tag = tag
        pass

    def host(self, host, port):
        print "Setting up host"
        self._start_server((host,port))

    def connect(self, host, port):
        self._start_client(host,port)

    def send(self,msg):
        self.client.send(msg)

    def get(self,block=True,timeout=None):
        print 'waiting for msg'
        return messaging.getMessageQueue().get(block, timeout)
        print 'message received!!!!'


    def _backup_connect(self,host,port):
        self._start_server(('127.0.0.1',CLIENT_PORT))
        time.sleep(1)
        msg = {'type':'SETUP','host':'(127.0.0.1,'+str(CLIENT_PORT)+')','pw':'random'}
        self.client.send(msg)


    def terminate(self, ):
        self.server_process.terminate()
        self.server_process.join()
        self.client.terminate()
        print "Connection terminated"

    # Internal methods
    def _start_server(self,addr=('127.0.0.1',HOST_PORT),pw='random'):
        self.server_process = LocalServer(addr, pw)
        self.server_process.start()
        print "process started"

    def _start_client(self, host, port, pw='random'):
        self.client = LocalClient((host,port),pw)


class LocalServer():
    def __init__(self, (host, port),pw='random'):
        super(LocalServer, self).__init__()
        self.host = host
        self.port = port
        self.pw = pw

    def run(self):
        print 'Server setup'
        try:
            listener = Listener((self.host, self.port), authkey=self.pw)
            print 'Server address :',listener.address
            conn = listener.accept()
            print 'connection accepted'
            while True:
                msg = conn.recv()
                resp = self.dispatch(msg)
                conn.send(resp)
        except EOFError,IOError:
            conn.close()
            listener.close()
            print "Connection terminated by client"


    def dispatch(self,msg):
        print "Adding msg to queue:", self.q
        self.q.put(msg)

    def finalize(self):
        pass

class LocalClient:
    def __init__(self,(host, port),pw='random'):
        self.address = (host, port)
        self.pw = pw
        self.conn = self.openconnection(self.address,pw)

    def openconnection(self,addr,pw):
        print "opening connection"
        conn = Client(addr,authkey=pw)
        print "found connection"
        return conn

    def send(self, msg):
        self.conn.send(msg)
        print "Message sent"
        #resp = self.conn.recv()
        #print resp

    def terminate(self):
        self.conn.send({'type':'TERMINATE'})
        self.conn.close()


if __name__ == '__main__':
    conn = GameConnection()
    conn.host('localhost',HOST_PORT)

    time.sleep(1)
#    host.terminate_server()
#    print host.server_process.is_alive()
