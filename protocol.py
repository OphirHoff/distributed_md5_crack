import socket

DEBUG = True

# MSG CODES
GET_TARGET = 'GETT'
TARGET = 'TRGT'
GET_TASK = 'WORK'
TASK = 'TASK'

IN = 0
OUT = 1

def recv(sock: socket.socket, size=1024):

    _len = int(sock.recv(4).decode())
    data = sock.recv(_len)
    if DEBUG:
        print(f"<<<{str(_len).zfill(4)}~{data.decode()}")
    return data.decode().split('~')[1:]


def send(sock: socket.socket, to_send=b''):

    if type(to_send) != bytes:
        to_send = to_send.encode()

    sock.send(to_send)

    if DEBUG:
        print(f">>>{to_send.decode()}")


def build_msg_protocol(code, *args):
    '''Creates message content according to protocol.'''

    msg = code + '~' + '~'.join([str(arg) for arg in args])
    to_send = f"{str(len(msg)+1).zfill(4)}~{msg}"
    return to_send

class ErrorMsg:
    def connection_failed(ip, port):
        print(f"Connection Failed to ({ip}, {port})")