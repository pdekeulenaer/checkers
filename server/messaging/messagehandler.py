#!/usr/bin/python

# Handle incoming messages
import message

class MessageHandler():
    def __init__(self, lobby):
        self.lobby = lobby

    def handle(self, msg):
        global _FDICT
        msgtype = msg.msgtype
        return self._FDICT[msgtype](self,msg)

    def register(self, msg):
        # get address
        self.lobby.addplayer(msg.name)


    def host(self, msg):
        print 'creating a room'
        print msg.game_name
        self.lobby.create_game(msg.sender, msg.game_name)


    def join_game(self, msg):
        gamename = msg.game_name
        game = self.lobby.games[gamename]
        resp = game.join(msg.sender)
        return resp

    def start_game(self, msg):
        print 'starting game'
        game = self.lobby.games[msg.game_name]
        resp = game.start(msg.sender)
        print resp
        print msg.sender

    ##########################
    #    SYNCHRONOUS CALLS   #
    ##########################
    def list_rooms(self, msg):
        resp = self.lobby.games.keys()
        return resp

    def game_status(self, msg):
        state = self.lobby.games[msg.game_name].get_status()
        return state

    def nop(self, msg):
        pass

    _FDICT = {
        'UNSPECIFIED MESSAGE TYPE' : nop,
        'REGISTER' : register,
        'ALIVE': nop,
        'LOGOFF': nop,
        'ACK' : nop,
        'ERR': nop,
        'HOST_GAME': host,
        'Q_LIST_GAMES': list_rooms,
        'JOIN_GAME': join_game,
        'START_GAME': start_game,
        'Q_GAME_STATUS': game_status,
    }


if __name__ == "__main__":

    hndlr = MessageHandler()
    hndlr.handle(message.AckMsg())
    hndlr.handle(message.ErrMsg())
    hndlr.handle(message.RegisterMessage("Philip"))