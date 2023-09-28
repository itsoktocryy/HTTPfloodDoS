import socket

def check_raw_socket_access():
    try:
        raw_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
        
        print("Raw socket access is allowed on your system.")
        
        raw_socket.close()
    except PermissionError as e:
        print(f"PermissionError: {e}")
        print("Raw socket access is not allowed. You may need administrative privileges.")
    except socket.error as e:
        print(f"SocketError: {e}")
        print("An error occurred while creating the socket.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    check_raw_socket_access()

