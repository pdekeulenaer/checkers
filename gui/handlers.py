import pygame
import utilities
from playerhandler import PlayerHandler
import sys

class GuiGameInputHandler(PlayerHandler):
    def __init__(self,ctrl, player=None,gui=None):
        super(GuiGameInputHandler, self).__init__(ctrl, player)
        self.gui = gui
        self.selected_cell = None
        self.log = utilities.Logger("GUI INPUT")


    def select_cell(self, cell):
        if self.selected_cell is None:
            owner = self.control.get_player(cell)
            if owner is None:
                self.log.write("empty cell")
            elif owner != self.control.turn:
                self.log.write("not your turn")
            else:
                self.selected_cell = cell
        else:
            self.submit_move(self.selected_cell, cell)

    def unselect_cell(self):
        self.selected_cell = None

    def submit_move(self, origin, target):
        resp,descr = super(GuiGameInputHandler,self).submit_move(origin, target)

        if resp == 'OK':
            self.unselect_cell()
        elif resp == 'CON':
            self.unselect_cell()
            self.select_cell(target)
        self.log.write(descr)


    # handle input events
    def mouseclick(self, button, pos):
        cell = self.gui.get_cell(pos)
        self.select_cell(cell)


    def keypress(self, key):
        if key == pygame.K_ESCAPE:
            self.unselect_cell()
        elif key == pygame.K_DOWN:
            self.log.write(self.control.mandatory_moves())
        else:
            self.log.write(key)

    def make_move(self):
        if self.isblocked():
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
            return

        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN: self.mouseclick(event.button, event.pos)
            if event.type == pygame.KEYDOWN: self.keypress(event.key)

    def isblocked(self):
        if self.player is None:
            return False
        else:
            if self.player == self.control.turn:
                return False

        self.unselect_cell()
        return True
