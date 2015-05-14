#!/usr/bin/python

# A basic server setup using sockets
# core libraries
import SocketServer

# custom imports
import serverconfig as cfg
from messaging.messageparser import Parser
from messaging.messagehandler import MessageHandler


# define a handler that can accept basic requests, containing standard messages
# this handler receives a message and sends an ACK if the message is known, otherwise an ERR
class RequestHandler(SocketServer.BaseRequestHandler):
    def setup(self):
        self.msghandler = MessageHandler(self.server.lobby)

    def handle(self):

        buffer = []
        bytes = self.request.recv(1024)
        while bytes:
            if (Parser._DEADCODE in bytes):
                break
            data = self.request.recv(1024)
            bytes += str(data)

        # decode the message
        msg = Parser.decode(bytes)

        # handle message
        resp = self.msghandler.handle(msg)

        # send response
        out = Parser.encode(resp)
        self.request.sendall(out)

    def finish(self):
        pass


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    def setLobby(self, lobby):
        self.lobby = lobby


def create(lobby):
    s = ThreadedTCPServer((cfg.HOST, cfg.PORT),RequestHandler)
    s.setLobby(lobby)

    return s

#st = threading.Thread(target=server.serve_forever)
#st.daemon = True
#st.start()
#print "Server thread started in", st.name
#time.sleep(10)
#server.shutdown()
