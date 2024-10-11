__Author__ = "OphirH"

import sys, subprocess
import socket, protocol

IP = 0
PORT = 1

SEARCH_TOOL = f"D:\\Cyber\\OS\\md5_crack\\C\\search.exe"

found = False
answer = None

def md5(target, range_start, range_end):
    return subprocess.run(f"D:\\Cyber\\OS\\md5_crack\\C\\search.exe {target} {range_start} {range_end}", stdout=subprocess.PIPE).stdout.decode()

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
        

    def get_ranges(self):
        """Gets list ranges (portions) from server."""
        pass


def check_range(target: str, range: tuple[int, int]):
    
    global found, answer

    print("Started")
    result = md5(target, range[0], range[1])
    if "Found" in result:
        answer = result.replace('Found!', '').strip()
        found = True
        

def check_output(processes: list[subprocess.Popen]):

    global found, answer

    for p in processes:
        output, _ = p.communicate()
        if b"Found" in output:
            answer = output.replace(b'Found!', b'').strip()
            found = True
            return


def main(server_ip=None, port=None, cpu_num=None, load_precent=None):
    
    # client = Client(server_ip, int(port))
    
    target = "A3FBF22F45DE932EC059D955F3228EB2"

    # list of ranges for each task (portion)
    tasks = [(0, 999999), (1000000, 1999999)]
    
    processes = []

    for task in tasks:
        p = subprocess.Popen(f"{SEARCH_TOOL} {target} {task[0]} {task[1]}", stdout=subprocess.PIPE)
        processes.append(p)
    
    while not found:
        
        check_output(processes)


    while not found:
        check_output(processes)
    
    
    print("Result: " + answer.decode())

if __name__ == "__main__":
    main()
    # if len(sys.argv) < 5:
    #     print("Arguments not passed correctly. Should be like so:\npython distributed_calc_client.py <server_ip> <server_port> <number of cpu> <load percent>")
    # else:
    #     main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])