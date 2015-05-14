# /usr/bin/env/python
from abc import ABCMeta, abstractmethod
from remote import BasicTransmitter

class PlayerHandler():

    __metaclass__ = ABCMeta


    def __init__(self, control, player,transmitter=None):
        self.control = control
        self.player = player
        if transmitter is None:
            self.transmitter = BasicTransmitter()
        else:
            self.transmitter = transmitter

    @abstractmethod
    def make_move(self):
        pass

    def submit_move(self, origin, target):
        resp,descr = self.control.move(origin, target)
        self.transmitter.send_move(origin, target)

        return (resp, descr)
