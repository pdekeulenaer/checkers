from connection import *
import messaging

if __name__ == '__main__':
    q = messaging.getMessageQueue()
    print q

    q2 = messaging.getMessageQueue()
    print q2
