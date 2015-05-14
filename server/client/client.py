#!/usr/bin/python

# A basic client setup using sockets

import socket
from messaging.messageparser import Parser
import messaging.message as message


class Client():
    def __init__(self, name, ip, port):
        self.name = name
        self.target_ip = ip
        self.target_port = port

    def register(self):
        msg = message.RegisterMessage(self.name)
        self._send(msg)

    def host(self, roomname):
        msg = message.HostMsg(roomname)
        self._send(msg)


    def get_game_status(self, game_name):
        msg = message.GameStatusMsg(game_name)
        resp = self._send(msg, False)
        print resp

    def start_game(self,name):
        msg = message.StartGame(name)
        self._send(msg)

    def list_games(self):
        msg = message.ListGames()
        resp = self._send(msg,False)
        print resp

    def join_game(self, roomname):
        msg = message.JoinGameMsg(roomname)
        resp = self._send(msg, False)
        print resp

    def _send(self, msg, async=True):
        msg.set_sender(self.name)
        if async: self._send_async(msg)
        else: return self._send_sync(msg)


    def _send_sync(self, msg):
        print self.name, 'sending a synced message'
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.target_ip, self.target_port))
        try:
            # send data
            outbytes = Parser.encode(msg)
            numbytes = len(outbytes)

            sock.sendall(outbytes)

            inbytes = []
            data = sock.recv(1024)
            while data:
                inbytes.append(data)
                data = sock.recv(1024)

            # decode the message
            resp = Parser.decode(''.join(inbytes))

        finally:
            sock.close()
        return resp

    def _send_async(self, msg):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((self.target_ip, self.target_port))
            try:
                # send data
                outbytes = Parser.encode(msg)
                sock.sendall(outbytes)

            finally:
                sock.close()
