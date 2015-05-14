# message

# Fixed message types
class MSGTYPE:
    UNSPECIFIED = 'UNSPECIFIED MESSAGE TYPE'
    REGISTER = 'REGISTER'
    AlIVE = 'ALIVE'
    LOGOFF = 'LOGOFF'
    ACKNOWLEDGE = 'ACK'
    ERROR = 'ERR'
    HOST_GAME = 'HOST_GAME'
    JOIN_GAME = 'JOIN_GAME'
    Q_GENERIC = 'QUERY'
    Q_LIST_GAMES = 'Q_LIST_GAMES'
    Q_GAME_STATUS = 'Q_GAME_STATUS'
    START_GAME = 'START_GAME'



class Message(object):
    def __init__(self,msgtype=MSGTYPE.UNSPECIFIED):
        self.msgtype = msgtype
        self.sender = None

    # this will override existing args of the same name
    def addargs(self, **content):
        for (k,v) in content:
            self.addarg(k,v)

    # this will override existing args with the same key
    def addarg(self, k, v):
        self.__setattr__(k,v)

    def set_sender(self, name):
        self.sender = name

    def __str__(self):
        l = ["Message type: %s" % self.msgtype]
        return l
        # map (lambda (k,v): l.append("  %s: %s" % (k,v)), self.args.items())
        # return '\n'.join(map(lambda x: str(x), l))


class RegisterMessage(Message):
    def __init__(self, name):
        super(RegisterMessage, self).__init__(MSGTYPE.REGISTER)
        self.name = name

class LogoffMessage(Message):
    def __init__(self, name):
        super(LogoffMessage, self).__init__(MSGTYPE.LOGOFF)
        self.name = name

class AckMsg(Message):
    def __init__(self):
        super(AckMsg, self).__init__(MSGTYPE.ACKNOWLEDGE)

class ErrMsg(Message):
    def __init__(self):
        super(ErrMsg, self).__init__(MSGTYPE.ERROR)

class HostMsg(Message):
    def __init__(self, roomname):
        super(HostMsg, self).__init__(MSGTYPE.HOST_GAME)
        self.game_name = roomname

class JoinGameMsg(Message):
    def __init__(self, roomname):
        super(JoinGameMsg, self).__init__(MSGTYPE.JOIN_GAME)
        self.game_name = roomname

class StartGame(Message):
    def __init__(self, roomname):
        super(StartGame, self).__init__(MSGTYPE.START_GAME)
        self.game_name = roomname


class Query(Message):
    def __init__(self, type=MSGTYPE.Q_GENERIC):
        super(Query, self).__init__(type)

class ListGames(Query):
    def __init__(self):
        super(ListGames, self).__init__(MSGTYPE.Q_LIST_GAMES)

class GameStatusMsg(Query):
    def __init__(self, game_name):
        super(GameStatusMsg, self).__init__(MSGTYPE.Q_GAME_STATUS)
        self.game_name = game_name


class SubmitMove(Message):
     def __init__(self, type=MSGTYPE.SUBMIT_MOVE):
        super(SubmitMove, self).__init__(type)



if __name__ == "__main__":
    r = RegisterMessage("philip")
    l = LogoffMessage("Philip")
    j = JoinGame('Destroyer')

    print j.game_name
