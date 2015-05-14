# !usr/bin/env python

# Encode and Decode messages
import cPickle as pickle


class Parser:

    _DEADCODE = str(0xDEADC0DE)

    @staticmethod
    def encode(msg):

        bytestring = pickle.dumps(msg) + Parser._DEADCODE
        return bytestring

    @staticmethod
    def decode(msg):
        cutmsg = msg[:-len(Parser._DEADCODE)]
        return pickle.loads(cutmsg)
