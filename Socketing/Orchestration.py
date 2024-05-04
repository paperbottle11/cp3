import socket
import threading
import datetime
import time

multiple = 0
chunk_size = 50000000
total_time = 0
factors = []

class FactorizationClient(threading.Thread):
    def __init__(self, ip, port, id):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.id = id

    def run(self):
        global multiple, total_time, factors
        while 1:
            composite_number = 3125269804025662091
            start_range = multiple * chunk_size
            multiple += 1
            stop_range = multiple * chunk_size

            try:
            # Establish connection to the server
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.connect((self.ip, self.port))

                    # Sending composite number and the range to the server
                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    log = f"[{timestamp}] CLIENT{self.id}, SENDING, {self.ip}, {composite_number}, {multiple * chunk_size}, {(multiple + 1) * chunk_size}\n"
                    with open('log.txt', 'a') as f:
                        f.write(log)

                    sock.sendall(f"{composite_number} {start_range} {stop_range}\n".encode())
                    start = time.perf_counter()
                    
                    # Receiving and printing server response
                    response = sock.recv(1024).decode().strip()
                    end = time.perf_counter()
                    total_time += end - start
                    # print(f"Server response: {response}")
                    print(f"Total Time: {total_time}", end="\r")

                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    log = f"[{timestamp}] CLIENT{self.id}, RECIEVING, {self.ip}, {composite_number}, {multiple * chunk_size}, {(multiple + 1) * chunk_size}, {response}, {end - start}\n"
                    with open('log.txt', 'a') as f:
                        f.write(log)

                    # If the response is a factor of the composite number, print the factor
                    if response != "" and int(response) != -1:
                        factors.append(int(response))
                        print(f"\nFactor found: {response}")
                    if composite_number**.5 < stop_range:
                        print(f"Factors: {factors}")
                        print(f"Total Time: {total_time}")
                        return

            except Exception as e:
                print(f"Error connecting to server: {e}")

if __name__ == "__main__":
    # Example usage
    client1 = FactorizationClient('34.71.161.175', 4321, 1)
    # client1 = FactorizationClient('192.168.56.1', 4000, 1)
    client1.start()

    # 34.71.161.175 4321