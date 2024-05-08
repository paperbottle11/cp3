import socket
import threading
import datetime
import time

multiple = 0
chunk_size = 50000000
total_time = 0
factors = []
clients = 0
max_clients = 16

composite = 3125269804025662091

ips =  {"34.71.161.175": False,
        "34.136.161.195": False,
        "34.135.157.79": False,
        "34.123.103.25": False,
        "34.133.158.119": False,
        "34.29.234.137": False,
        "34.41.144.62": False,
        "34.30.207.159": False,
        "35.223.112.97": False,
        "35.238.11.71": False,
        "34.42.177.36": False,
        "34.171.165.99": False,
        "34.123.34.89": False,
        "34.30.17.221": False,
        "35.202.247.41": False,
        "34.134.18.205": False}

class FactorizationClient(threading.Thread):
    def __init__(self, ip, port, id):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.id = id

    def run(self):
        global multiple, total_time, factors, clients, ips
        while 1:
            start_range = multiple * chunk_size
            multiple += 1
            stop_range = multiple * chunk_size

            try:
            # Establish connection to the server
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.connect((self.ip, self.port))

                    # Sending composite number and the range to the server
                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    log = f"[{timestamp}] CLIENT{self.id}, SENDING, {self.ip}, {composite}, {multiple * chunk_size}, {(multiple + 1) * chunk_size}\n"
                    with open('log.txt', 'a') as f:
                        f.write(log)

                    sock.sendall(f"{composite} {start_range} {stop_range}\n".encode())
                    start = time.perf_counter()
                    
                    # Receiving and printing server response
                    response = sock.recv(1024).decode().strip()
                    end = time.perf_counter()
                    total_time += end - start
                    # print(f"Server response: {response}")
                    print(f"Total Time: {total_time}", end="\r")

                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    log = f"[{timestamp}] CLIENT{self.id}, RECIEVING, {self.ip}, {composite}, {multiple * chunk_size}, {(multiple + 1) * chunk_size}, {response}, {end - start}\n"
                    with open('log.txt', 'a') as f:
                        f.write(log)

                    # If the response is a factor of the composite number, print the factor
                    if response != "" and int(response) != -1:
                        factors.append(int(response))
                        print(f"\nFactor found: {response}")
                    if composite**.5 < stop_range:
                        print(f"\nFactors: {factors}")
                        print(f"Total Time: {total_time}")
                        clients -= 1
                        ips[self.ip] = False
                        return

            except Exception as e:
                print(f"Error connecting to server: {e}")

def getOpenIP():
    for ip in ips:
        if not ips[ip]:
            ips[ip] = True
            return ip

if __name__ == "__main__":
    # with open("log.txt", "r") as f:
    #     log = f.readlines()
    # nums = {}
    # for line in log:
    #     if line.strip() == "":
    #         continue
    #     words = line.strip().split(",")
    #     words = [word.strip() for word in words]
    #     if len(words) < 6 or len(words) > 8:
    #         continue
    #     if words[1] == "RECIEVING":
    #         if words[3] not in nums:
    #             nums[words[3]] = 0
    #         nums[words[3]] += float(words[7])
    # print("composite,time")
    # for num in nums:
    #     print(f"{num},{nums[num]}")
    
    with open("composites.txt", "r") as f:
        composites = f.readlines()
    while composites:
        composite = composites.pop(0).strip()
        if composite == "":
            continue
        print("Factoring: ", composite)
        multiple = 0
        factors = []
        clients = 0
        composite = int(composite)
        for i in range(max_clients):
            client = FactorizationClient(getOpenIP(), 4321, i)
            client.start()
            clients += 1
        while clients > 0:
            pass

    
    # # Example usage
    # client1 = FactorizationClient('34.71.161.175', 4321, 1)
    # # client1 = FactorizationClient('192.168.56.1', 4000, 1)
    # client1.start()