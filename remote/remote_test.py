from connection import *

if __name__ == '__main__':
    conn = GameConnection('HOST')
    conn.host('localhost',HOST_PORT)

    time.sleep(10)
    q = messaging.getMessageQueue()
    print q

    print q.get()

    print "time is up"
    conn.terminate()

