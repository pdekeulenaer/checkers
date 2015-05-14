# /usr/bin/env/python
import logic
import gui
import utilities
import sys

from multiprocessing import Process

class Master:
    def __init__(self,size):
        self.state = 'INIT'
        self.handlers = []

    def landingpage(self):
        #state
        self.state = 'INIT'
        self.game = None
        self.ctrl = None

        #guis
        lp = gui.LandingPage()
        op = lp.run()

        if op == gui.RETURN_2PGAME :
            self.start_2p_game()
        elif op == gui.RETURN_AIGAME:
            self.start_ai_game()


    def handle_events(self):
        if self.state == 'GAME':
            for handlr in self.handlers:
                if self.finished():
                    return
                handlr.make_move()
                self.gui.render()


    def setup_game(self):
        self.game = logic.Checkers()
        self.ctrl = logic.Controller(self.game, [logic.players.WHITE, logic.players.BLACK])
        self.state = 'GAME'

    def setup_gamegui(self):
        print self
        self.gui = gui.GameGUI((800,800))
        self.gui.start_game(self.game)

    def start_2p_game(self):
        self.setup_game()
        self.setup_gamegui()
        print self.gui
        # handlers
        self.handlers = [gui.GuiGameInputHandler(self.ctrl,gui=self.gui)]
        print self.gui

    def start_ai_game(self):
        self.setup_game()
        self.setup_gamegui()

        # handlers
        #humanhandler = gui.GuiGameInputHandler(self.ctrl, logic.players.WHITE, self.gui)
        ai2handler = logic.BasicAI(self.ctrl, logic.players.WHITE)
        aihandler = logic.BasicAI(self.ctrl,logic.players.BLACK)
        self.handlers = [ai2handler, aihandler]

    def finished(self):
        if self.state == 'GAME': return self.game.done
        return False

    def get_winner(self):
        if self.finished():
            return self.game.winner

    def cleanup(self):
        self.gui.close()
        self.gui = None
        self.game = None
        self.ctrl = None


# main code
if __name__ == "__main__":

    size = width, height = 600,600

    master = Master(size)
    master.landingpage()

    while True:
        master.handle_events()
        if master.finished():
            print "Congratulations %s" % master.get_winner().col
            master.cleanup()
            master.landingpage()
        master.gui.render()

