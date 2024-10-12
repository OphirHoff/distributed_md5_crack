import socket, threading

IP = "127.0.0.1"
PORT = 1234

all_to_die = False
found = False

class Server:
    def __init__(self, max_clients=20) -> None:
        self.max_clients: int = max_clients
        self.server_sock: socket.socket = None
        self.clients_connected = 0
        self.clients = []

    def initialize_connection(self) -> None:
        self.sock = socket.socket()
        self.sock.bind((IP, PORT))
        self.sock.listen(20)
    
    def handle_client(self, sock, tid, address):
        return

    def main(self):
        global all_to_die, found

        threads = []

        self.initialize_connection()

        while True:
            if len(self.clients_connected) < self.max_clients:
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
    server = Server()
    server.main()