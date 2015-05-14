#!/usr/bin/python
# Master class for the server

import server.server as server
import server.serverconfig as cfg
import threading

# for tests
import client.client as client
import messaging.message as message
import time

class Lobby:
    def __init__(self):
        self.players = []
        self.games = {}

    def addplayer(self, plyr):
        self.players.append(plyr)

    #TODO create into dictionary
    def create_game(self, plyr, roomname, game='Checkers'):
        self.games[roomname] = GameRoom(plyr, roomname, game)

class GameRoom:
    def __init__(self, owner, name, game_type='Checkers'):
        self.players = [owner]
        self.owner = owner
        self.name = name
        self.game_type = game_type
        self.MAX_PLAYERS = 2
        self.MIN_PLAYERS = 2
        self.state = 'Initialization'

    def join(self, plyr):
        if (len(self.players) < self.MAX_PLAYERS):
            self.players.append(plyr)
            return 'ACK'
        else:
            return 'ERR - Room full'

    def start(self, sender):
        if (sender != self.owner):
            return 'ERR - Not allowed'

        if (len(self.players) >= self.MIN_PLAYERS):
            self.state = 'Started'
            return 'OK'
        else:
            self.state = 'Initialization'
            return 'ERR - Not enough players'


    def get_status(self):
        status = {}
        status['players'] = self.players
        status['owner'] = self.owner
        status['name'] = self.name
        status['game_type'] = self.game_type
        status['state'] = self.state
        status['content'] = None
        return status

if __name__ == "__main__":

    # initiate gameroom
    lobby = Lobby()


    # start the server thread
    srvr = server.create(lobby)
    server_thread = threading.Thread(target=srvr.serve_forever)
    server_thread.daemon = True
    server_thread.start()

    # run a few clients
    philip = client.Client("Philip", cfg.HOST, cfg.PORT)
    philip.register()
    philip.host('Destroyer')

    time.sleep(1)

    luke = client.Client("Luke", cfg.HOST, cfg.PORT)
    luke.register()
    luke.list_games()
    luke.join_game('Destroyer')

    philip.start_game('Destroyer')

    philip.get_game_status('Destroyer')

    time.sleep(5)

    luke.get_game_status('Destroyer')

