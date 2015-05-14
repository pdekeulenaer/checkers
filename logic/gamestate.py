from players import BLACK,WHITE
from utilities import Util

class Checkers:
    def __init__(self):
        self._createboard()
        self.setup_pieces()
        self.done = False

    @staticmethod
    def isjump((xa,ya),(xb,yb)):
        return abs(xa-xb) > 1

    # setup functions
    def _createboard(self):
        self.board = [None]*8
        for x in range(0,8):
            self.board[x] = [None]*8
            for y in range(0,8):
                self.board[x][y] = Square(x,y)

    def setup_pieces(self):
        for x in range(0,8):
            for y in range(0,8):
                if (y < 3 and (x+y) % 2 == 0):
                    self.board[x][y].setpiece(Piece(BLACK))
                elif (y > 4 and (x+y)%2 == 0):
                    self.board[x][y].setpiece(Piece(WHITE))


    # game is in a valid state
    def validate_state(self):
        for x in range(0,8):
            if self.board[x][0].piece:
                if self.board[x][0].piece.player == WHITE:
                    self.promote((x,0))

            if self.board[x][7].piece:
                if self.board[x][7].piece.player == BLACK:
                    self.promote((x,7))


        # alternative
        pieces = filter(lambda x: x.piece,Util.flatten(self.board))
        black = len(filter(lambda x: x.piece.player == BLACK,pieces))
        white = len(filter(lambda x: x.piece.player == WHITE,pieces))

        if black == 0: self.win(WHITE)
        if white == 0: self.win(BLACK)


    def win(self, winner):
        self.done = True
        self.winner = winner


    ##########################
    #                        #
    #   MOVEMENT FUNCTIONS   #
    #                        #
    ##########################

    def possible_jumps(self, (x,y), player,source=None):
        # filter enemy neigbhours to jump over
        d = self.board[x][y].piece.dir
        n = self.board[x][y].getneighbours(d)
        enemies = filter(lambda (a,b): not(self.is_free_square((a,b))) and self.board[a][b].piece.player != player, n)

        jumps = []
        # list of enemies
        for (xE,yE) in enemies:
            xnew = xE + (xE - x)
            ynew = yE + (yE- y)
            if Square.valid_coords((xnew,ynew)):
                if self.is_free_square((xnew,ynew)):
                    jumps.append((xnew,ynew))

        return jumps


    def mandatory_moves(self, player):
        # for each cell
        # if there are valid jumps, add these to the list
        mandatory = []
        # flatten board
        flatlist = reduce(lambda x,y:x+y,self.board)
        flatlist = filter(lambda x:x.piece, flatlist)
        flatlist = filter(lambda x:x.piece.player == player, flatlist)

        for square in flatlist:
            jumps = self.possible_jumps((square.x, square.y), player)
            if jumps:
                l = map(lambda x: ((square.x,square.y), x),self.possible_jumps((square.x, square.y), player))
                mandatory += l

        return mandatory

    def empty_neighbours(self, (x, y), d=0):
        n = self.board[x][y].getneighbours(d)
        n = filter(lambda l: self.is_free_square(l),n)
        return n

    def all_valid_moves(self,player):
        flatlist = reduce(lambda x,y:x+y,self.board)
        flatlist = filter(lambda x:x.piece, flatlist)
        flatlist = filter(lambda x:x.piece.player == player, flatlist)
        valid = []

        for square in flatlist:
            valid += map(lambda x: ((square.x,square.y),x), self.valid_moves((square.x,square.y)))

        return valid


    def valid_moves(self,(x,y)):
        if self.is_free_square((x,y)):
            return None

        player = self.board[x][y].piece.player
        d = self.board[x][y].piece.dir

        empty = self.empty_neighbours((x,y),d)
        jumps = self.possible_jumps((x,y),player,d)
        return empty + jumps

    def is_free_square(self, (x, y)):
        return self.board[x][y].is_free()

    def get_player(self, (x,y)):
        sq = self.board[x][y]
        if sq.piece is None:
            return None
        return sq.piece.player


    ##########################
    #                        #
    #   ACTION FUNCTIONS     #
    #                        #
    ##########################

    def move(self, (xa,ya),(xb,yb)):
        piece = self.board[xa][ya].piece
        self.board[xa][ya].setpiece(None)
        self.board[xb][yb].setpiece(piece)
        if (abs(xa-xb) > 1):
            self.beat((xa,ya),(xb,yb))

        self.validate_state()


    def beat(self,(xa,ya),(xb,yb)):
        self.board[int((xa+xb)/2)][int((ya+yb)/2)].setpiece(None)

    def promote(self, (x,y)):
        self.board[x][y].piece.promote()


class Square:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.piece = None

    def setpiece(self,piece):
        self.piece = piece

    def getneighbours(self, ns = 0, we = 0):
        neighbours = []
        if (we == 0):
            if (ns == 0):
                return self._northneighbours() + self._southneighbours()
            elif (ns == 1):
                return self._northneighbours()
            elif (ns == -1):
                return self._southneighbours()
        else:
            if (ns == 0):
                if we == 1 : self._eastneighbours()
                if we == -1: self._westneighbours()
            else:
                return [(self.x+we,self.y+ns)]


    def _northneighbours(self):
        l = [(self.x+1,self.y+1),(self.x-1,self.y+1)]
        return filter(lambda m: self.valid_coords(m), l)

    def _southneighbours(self):
        l = [(self.x+1,self.y-1),(self.x-1,self.y-1)]
        return filter(lambda m: self.valid_coords(m), l)

    def _eastneighbours(self):
        l = [(self.x+1,self.y+1),(self.x+1,self.y-1)]
        return filter(lambda m: self.valid_coords(m), l)

    def _westneighbours(self):
        l = [(self.x-1,self.y+1),(self.x-1,self.y-1)]
        return filter(lambda m: self.valid_coords(m), l)

    def is_free(self):
        return (self.piece is None)

    @staticmethod
    def valid_coords((x,y)):
        return (0 <= x <= 7) and (0 <= y <= 7)

class Piece:
    def __init__(self, player, queen=False):
        self.queen = queen
        self.player = player
        self.dir = player.dir
        self.col = player.col

    def promote(self):
        self.queen = True
        self.dir = 0
