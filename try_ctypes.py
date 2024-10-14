__Author__ = "OphirH"

import sys, subprocess, os, ctypes
import socket, protocol
from multiprocessing import Process, Queue, Array

IP_INDEX = 0
PORT_INDEX = 1

MD5_UINT8_T_ARR_SIZE = 32
search_lib = ctypes.CDLL('./C/search.dll')
# search_lib.searchRange.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_int]
# target = ''
search_lib.searchRange.argtypes = [ctypes.POINTER(ctypes.c_uint8), ctypes.c_int, ctypes.c_int]
target_uint8_t = Array(ctypes.c_uint8, MD5_UINT8_T_ARR_SIZE)

found = False
answer = None


def set_target(t: bytes):

    for i in range(len(target_uint8_t)):
        target_uint8_t[i] = t[i]


class Client:
    def __init__(self, server_ip, port) -> None:
        self.server_ip = server_ip
        self.port = port
        self.sock = None
        self.initialize_connection()

    def initialize_connection(self):
        """Initialize TCP connection with server."""
        self.sock = socket.socket()
        try:
            self.sock.connect((self.server_ip, self.port))
        except:
            protocol.ErrorMsg.connection_failed(self.server_ip, self.port)
            exit(1)

    def handle_server_response(self, response: list[str]):

        global _target

        code = response[0]
        args = response[1:]

        if code == protocol.TARGET:
            return args[0]

        if code == protocol.TASK:
            return args[0], args[1]

    def get_target(self, cpu_num, load_precent):
        protocol.send(self.sock, protocol.build_msg_protocol(protocol.GET_TARGET, cpu_num, load_precent))
        return self.handle_server_response(protocol.recv(self.sock))

    def get_ranges(self, portions_num: int | None = '') -> list[tuple]:
        """Gets list ranges (portions) from server."""
        protocol.send(self.sock, protocol.build_msg_protocol(protocol.GET_TASK, portions_num))
        portion_size, portion_starts = self.handle_server_response(protocol.recv(self.sock))
        portion_size = int(portion_size)
        ev = eval(portion_starts)
        if type(ev) == tuple:
            return [(start, start+portion_size-1) for start in ev]
        return [(ev, ev+portion_size-1)]

    def notify_find(self, answer: str) -> None:
        protocol.send(self.sock, protocol.build_msg_protocol(protocol.FOUND, answer))


def check_range(q: Queue, r: tuple[int, int], target):
    result = search_lib.searchRange(target.get_obj(), r[0], r[1])
    q.put(result)


def start_process(task, results, target):
    p = Process(target=check_range, args=(results, task, target))
    p.start()


def main(server_ip, port, cpu_num, load_precent):
    global found, answer, target_uint8_t
    """
    Client main:
    1 Get target - MD5 hash to find
    2. Get ranges of numbers to work on
    3. Go through ranges - divide work to multiprocessing
    4. If found - update server, else - go back to 2
    """
    client = Client(server_ip, int(port))

    # Get target from server
    target = client.get_target(cpu_num, load_precent).encode()
    
    print(f"Got target: '{target}'")

    set_target(target)

    # list of ranges for each task (portion)
    tasks = client.get_ranges()
    print(f"Tasks: {tasks}")
    
    results = Queue()

    for task in tasks:
        start_process(task, results, target_uint8_t)

    print("Processes running...")
    
    while True:
        
        output = results.get()
        if output == -1:
            task = client.get_ranges(portions_num=1)[0]
            start_process(task, results, target_uint8_t)
        else:
            answer = str(output).zfill(10)
            found = True

        if found:
            client.notify_find(answer)
            break

    print("Result: " + answer)

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Arguments not passed correctly. Should be like so:\npython distributed_calc_client.py <server_ip> <server_port> <number of cpu> <load percent>")
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])