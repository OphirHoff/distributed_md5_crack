__author__ = "OphirH YB-3"

import os, sys, socket, threading, time
import psutil
import protocol

IP = "0.0.0.0"
PORT = 1234

MAX_OPTION = 9999999999
PORTION_SIZE = 10000000

# Clients tid dict keys
CPU_NUM = 'cpu_num'
LOAD_PRECENT = 'load_precent'
PORTIONS = 'portions'
SOCK = 'sock'

target = ''
all_to_die = False
found = False
answer = ''

def set_high_proirity():
    psutil.Process(os.getpid()).nice(psutil.REALTIME_PRIORITY_CLASS)

class Server:
    def __init__(self, max_clients=20) -> None:
        self.max_clients: int = max_clients
        self.server_sock: socket.socket = None
        self.clients_connected = 0
        self.clients: dict[int, dict[str, int]] = {}  # {tid : {sock: <client_sock>, cpu_num: 2, load_precent: 75}}
        self.starts_covered = []
        self.ranges = self.__ranges()

        # To count total crack time
        self.t1 = None
        self.t2 = None

    def initialize_connection(self) -> None:
        self.server_sock = socket.socket()
        self.server_sock.bind((IP, PORT))
        self.server_sock.listen(20)
        self.server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_sock.settimeout(0.1)

    def __ranges(self):
        while True:
            _next = len(self.starts_covered) * PORTION_SIZE
            if _next > MAX_OPTION:
                break
            self.starts_covered.append(_next)
            yield _next

    def calc_portions_num(cpu_num, load_precent):
        return cpu_num * load_precent // 100 * 2

    def get_ranges(self, tid=None, portions_num=None):
        if portions_num:
            return [str(next(self.ranges)) for i in range(portions_num)]
        return [str(next(self.ranges)) for i in range(self.clients[tid][PORTIONS])]

    def notify_found(self, tid):
        to_send = protocol.build_msg_protocol(protocol.DISCONNECT)
        protocol.send(self.clients[tid][SOCK], to_send)

    def notify_all_found(self):
        for client in self.clients.items():
            self.notify_found(client[0])

    def handle_request(self, request: list[str], tid=None):
        
        global target, found, answer

        code = request[0]
        args = request[1:]

        if code == protocol.GET_TARGET:
            self.clients[tid][CPU_NUM] = int(args[0])
            self.clients[tid][LOAD_PRECENT] = int(args[1])
            self.clients[tid][PORTIONS] = Server.calc_portions_num(int(args[0]), int(args[1]))
            return protocol.build_msg_protocol(protocol.TARGET, target)
        elif code == protocol.GET_TASK:
            if args[0]:
                return protocol.build_msg_protocol(protocol.TASK, PORTION_SIZE, f"({','.join(self.get_ranges(portions_num=int(args[0])))})")
            return protocol.build_msg_protocol(protocol.TASK, PORTION_SIZE, f"({','.join(self.get_ranges(tid=tid))})")
        elif code == protocol.FOUND:
            self.t2 = time.time()
            found = True
            answer = args[0]
            
        return ''
            

    def handle_client(self, sock, tid, address):
        
        global found, all_to_die

        while not all_to_die:

            client_request = protocol.recv(sock)
            to_send = self.handle_request(client_request, tid=tid)

            if to_send != '':
                protocol.send(sock, to_send)
            
            if found:
                all_to_die = True
                self.notify_found(tid)
                break


    def main(self):
        global all_to_die, found

        threads = []

        self.initialize_connection()

        while True:
            if len(threads) < self.max_clients:
                try:
                    client_sock, address = self.server_sock.accept()
                    if not self.t1:
                        self.t1 = time.time()
                    t = threading.Thread(target=self.handle_client, args=(client_sock, self.clients_connected, address))
                    self.clients[self.clients_connected] = {SOCK: client_sock}
                    t.start()
                    
                    print(f"Main Thread: New Client connected {address} tid={self.clients_connected}")
                    self.clients_connected += 1
                    threads.append(t)
                    
                except socket.timeout:
                    pass
            if found:
                break
            
        print(f"""
###############################################
                    FOUND!
          The password is: {answer.zfill(10)}

           Crack time: {round(self.t2 - self.t1, 3)} sec.
###############################################
            """)

        print('Main thread: waiting for all clients to die')
        for t in threads:
            t.join()
        self.server_sock.close()
        print('Bye...')

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Arguments not passed correctly. Should be like so:\npython distributed_calc_server.py <MD5 Hashed Password>")
    else:
        target = sys.argv[1].upper()
        server = Server()
        server.main()