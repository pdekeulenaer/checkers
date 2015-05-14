# /usr/bin/env/python

class RemotePlayer():
    def __init__(self,ctrl, player):
        super(GuiGameInputHandler, self).__init__(ctrl, player)
        self.selected_cell = None
        self.log = utilities.Logger("REMOTE INPUT")

    def make_move(self):
        pass
