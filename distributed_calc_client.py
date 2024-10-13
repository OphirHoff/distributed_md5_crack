__Author__ = "OphirH"

import sys, subprocess, os
import socket, protocol

IP_INDEX = 0
PORT_INDEX = 1

# SEARCH_TOOL = f"D:\\Cyber\\OS\\md5_crack\\C\\search.exe"
SEARCH_TOOL = f"{os.path.dirname(os.path.abspath(__file__))}\\C\\search.exe"

target = ''

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

    def handle_server_response(self, response: list[str]):

        global target

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
        # return [(start, start+portion_size-1) for start in range(ev)]
        return [(ev, ev+portion_size-1)]

    def notify_find(self, answer: str) -> None:
        protocol.send(self.sock, protocol.build_msg_protocol(protocol.FOUND, answer))


def check_range(target: str, r: tuple[int, int]):
    return subprocess.Popen(f"{SEARCH_TOOL} {target} {r[0]} {r[1]}", stdout=subprocess.PIPE, shell=True)
        

def check_output(processes: list[subprocess.Popen]) -> bool | None:
    global found, answer
    """
    Iterate through processes:
    1. Check output to determine if answer was found
    2. Remove process from list if finished with no result

    RETURN:
    True -> Found answer
    False -> Process finished and died
    None -> Neither
    """
    for p in processes:

        output = p.stdout.readline()
        if b"Found" in output:
            answer = output.replace(b'Found!', b'').strip()
            found = True
            return True

        if p.poll() is not None:
            processes.remove(p)
            return False


def main(server_ip, port, cpu_num, load_precent):
    """
    Client main:
    1. Get target - MD5 hash to find
    2. Get ranges of numbers to work on
    3. Go through ranges - divide work to multiprocessing
    """

    client = Client(server_ip, int(port))

    # Get target from server
    target = client.get_target(cpu_num, load_precent)
    print(f"Got target: '{target}'")

    # list of ranges for each task (portion)
    tasks = client.get_ranges()
    print(f"Tasks: {tasks}")
    
    processes = []

    for task in tasks:
        p = check_range(target, task)
        processes.append(p)

    print("Processes running...")
    
    while True:
        result = check_output(processes)

        if result == False:  
            task = client.get_ranges(portions_num=1)[0]  # ask for more work
            if task:
                processes.append(check_range(target, task))
            
        if found:
            client.notify_find(answer)

    print("Result: " + answer.decode())

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Arguments not passed correctly. Should be like so:\npython distributed_calc_client.py <server_ip> <server_port> <number of cpu> <load percent>")
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])