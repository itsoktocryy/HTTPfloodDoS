import socket

def get_all_ips(domain):
    try:
        ip_addresses = socket.gethostbyname_ex(domain)
        return ip_addresses[2]
    except socket.gaierror as e:
        return []

if __name__ == "__main__":
    domain = input("Enter the domain (e.g., example.com): ")
    ips = get_all_ips(domain)

    if ips:
        print(f"IP addresses for {domain}:")
        for ip in ips:
            print(ip)
    else:
        print(f"Failed to resolve IP addresses for {domain}")

