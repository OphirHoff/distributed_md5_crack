import socket

# MSG CODES
GET_TARGET = 'GETT'
TARGET = 'TRGT'
GET_TASK = 'WORK'
TASK = 'TASK'


def recv(sock: socket.socket, size=1024):

    _len = sock.recv(4)
    data = sock.recv(int(_len))
    return data.decode().split('~')[1:]


def send(sock: socket.socket, to_send=b''):
    
    if type(to_send) != bytes:
        to_send = to_send.encode()

    sock.send(to_send)


def build_msg_protocol(code, *args):
    '''Creates message content according to protocol.'''

    msg = code + '~' + '~'.join([str(arg) for arg in args])
    to_send = f"{str(len(msg)+1).zfill(4)}~{msg}"
    return to_send

class ErrorMsg:
    def connection_failed(ip, port):
        print(f"Connection Failed to ({ip}, {port})")