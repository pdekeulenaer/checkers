from players import BLACK,WHITE
from gamestate import Checkers, Square, Piece
from utilities import Logger

class Controller:
    def __init__(self, checkers, plyrs, starting=0):
        self.game = checkers
        self.players = plyrs
        self.turn = self.players[starting]
        self.player_id = starting
        self.logger = Logger("CTRL")


    def move(self, origin, target):
        self.log("moving")

        # check if there is a mandatory move
        mandatory = self.mandatory_moves(self.turn)
        move = (origin,target)

        if mandatory and not move in mandatory:
            self.log("Mandatory move exists")
            self.log("please select a new piece and try again")
            res = ('NOK','mandatory move exists')
            return res

        # check if move is in valid moves
        if ((origin,target) in self.valid_moves(self.turn)):
            self.game.move(origin, target)
            #obligatory move
            res = ('CON','Additional move available')
            if not (Checkers.isjump(origin, target) and self.game.possible_jumps(target,self.turn)):
                self._switch_player()
                res = ('OK','move executed, turn switched')

        else:
            # not a valid move, please try again
            res = ('NOK','Invalid move')
            self.log("Invalid move")

        return res


    def get_player(self, cell):
        return self.game.get_player(cell)

    def mandatory_moves(self,player):
        return self.game.mandatory_moves(player)

    def valid_moves(self, player):
        moves = self.game.all_valid_moves(player)
        return moves

    def view_board(self):
        return self.game.board

    def _switch_player(self):
        self.player_id += 1
        self.player_id %= len(self.players)
        self.turn = self.players[self.player_id]
        self.log("Updated player to %s" % (str(self.turn)))

    def log(self,msg):
        #self.log.write(msg)
        pass

