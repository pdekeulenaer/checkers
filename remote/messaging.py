from Queue import Queue


#global MSG_SYNC, MSG_ASYNC
MSG_SYNC = 0
MSG_ASYNC = 1

def getMessageQueue():
    global _MSG_QUEUE
    try :
        _MSG_QUEUE
    except NameError:
        print 'MSG_QUEUE not defined, defining now'
        _MSG_QUEUE = MessageQueue()
    else:
        print 'MSG_QUEUE alreadyd efined, returning'

    return _MSG_QUEUE

class MessageQueue(Queue):
    def __init__(self):
        Queue.__init__(self)


class Message():
    def __init__(self, content):
        self.type = MSG_ASYNC
        self.content = content

