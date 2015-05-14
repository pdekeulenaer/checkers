from connection import *


if __name__ == '__main__':
    conn = GameConnection('CLIENT')
    print HOST_PORT
    conn.connect('127.0.0.1',HOST_PORT)
    conn.host('127.0.0.1',CLIENT_PORT)
    msg = {'type':'SETUP','host':'(127.0.0.1,'+str(CLIENT_PORT)+')','pw':'random'}
    conn.send(msg)

    time.sleep(15)

    conn.terminate()
