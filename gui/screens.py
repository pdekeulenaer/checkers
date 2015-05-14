import sys,pygame
import math


black = 0,0,0
brown = 139,69,19
white = 255,255,255
blue = 0,0,255

pieces = 12

COLOURS = {'BLACK':black, 'WHITE':white}


class GameGUI():
    def __init__(self, (width,height)):
        pygame.init()
        self.size = (width,height)
        self.screen = pygame.display.set_mode((width,height))

    def start_game(self, game):
        self.game = game
        self.activepage = BoardGUI(self)

    def render(self,delay=10):
        self.activepage.render()
        pygame.display.flip()
        pygame.time.delay(delay)

    def get_cell(self, (x,y)):
        xc = int(math.floor(x / (self.size[0]/8)))
        yc = int(math.floor(y / (self.size[1]/8)))
        return (xc, yc)

    def close(self):
        pygame.display.quit()
        pygame.quit()

class BoardGUI():
    def __init__(self, gui):
        self.gui = gui
        self.width = self.gui.size[0]
        self.height = self.gui.size[1]


    def render(self):
        self.draw_board(self.width, self.height)
        self.draw_pieces()

    def draw_board(self, w, h ):
        square = pygame.Rect(0,0,self.width/8,self.height/8)
        for x in range(0,8):
            for y in range (0,8):
                if ((x+y) % 2 == 0):
                    pygame.draw.rect(self.gui.screen, brown, square.copy().move(x*(w/8),y*(h/8)))
                else:
                    pygame.draw.rect(self.gui.screen, white, square.copy().move(x*(w/8),y*(h/8)))

    def draw_pieces(self):
        for x in range(0,8):
            for y in range(0,8):
                if self.gui.game.board[x][y]:
                        self.draw_piece(self.gui.game.board[x][y].piece,x,y)

    def draw_piece(self, piece, x,y):
        if piece :
            r = 0.65
            if piece.queen : r = 0.85

            radius = int ((min(self.width/8,self.height/8)/2) * r)
            pos = (int((x+0.5) * self.width/8), int((y+0.5)*self.height/8))
            pygame.draw.circle(self.gui.screen,COLOURS[piece.col],pos,radius)
