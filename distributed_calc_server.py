import sys, socket, threading
import protocol

IP = "127.0.0.1"
PORT = 1234

MAX_OPTION = 9999999999
PORTION_SIZE = 1000000

# Clients tid dict keys
CPU_NUM = 'cpu_num'
LOAD_PRECENT = 'load_precent'
PORTIONS = 'portions'

target = ''
all_to_die = False
found = False

class Server:
    def __init__(self, max_clients=20) -> None:
        self.max_clients: int = max_clients
        self.server_sock: socket.socket = None
        self.clients_connected = 0
        self.clients: dict[int, dict[str, int]] = {}  # {tid : {cpu_num: 2, load_precent: 75}}
        self.starts_covered = []
        self.ranges = self.__ranges()

    def initialize_connection(self) -> None:
        self.server_sock = socket.socket()
        self.server_sock.bind((IP, PORT))
        self.server_sock.listen(20)

    def __ranges(self):
        while True:
            _next = len(self.starts_covered) * PORTION_SIZE
            if _next > MAX_OPTION:
                break
            self.starts_covered.append(_next)
            yield _next

    def calc_portions_num(cpu_num, load_precent):
        return cpu_num * (load_precent) // 100 * 2

    def get_ranges(self, tid):
        return [str(next(self.ranges)) for i in range(self.clients[tid][PORTIONS])]

    def handle_request(self, request: list[str], tid=None):
        
        global target

        code = request[0]
        args = request[1:]

        if code == protocol.GET_TARGET:
            self.clients[tid] = {CPU_NUM: int(args[0]), LOAD_PRECENT: int(args[1]), PORTIONS: Server.calc_portions_num(int(args[0]), int(args[1]))}
            return protocol.build_msg_protocol(protocol.TARGET, target)
        elif code == protocol.GET_TASK:
            return protocol.build_msg_protocol(protocol.TASK, PORTION_SIZE, f"({','.join(self.get_ranges(tid))})")

        return ''
            

    def handle_client(self, sock, tid, address):
        
        while True:

            client_request = protocol.recv(sock)
            print(client_request, type(client_request))
            to_send = self.handle_request(client_request)

            if to_send != '':
                protocol.send(sock, to_send)
            


    def main(self):
        global all_to_die, found

        threads = []

        self.initialize_connection()

        while True:
            if len(threads) < self.max_clients:
                client_sock, address = self.server_sock.accept()
                t = threading.Thread(target=self.handle_client, args=(client_sock, self.clients_connected, address))
                t.start()
                self.clients_connected += 1
                threads.append(t)
            if found:
                break
            
        print('Main thread: waiting for all clients to die')
        for t in threads:
            t.join()
        self.server_sock.close()
        print('Bye...')


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Arguments not passed correctly. Should be like so:\npython distributed_calc_server.py <MD5 Hashed Password>")
    else:
        target = sys.argv[1]
        server = Server()
        server.main()