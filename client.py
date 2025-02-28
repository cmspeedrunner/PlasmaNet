import socket

HOST, PORT = "192.168.1.68", 8888  # IPv4 address of the computer hosting the server.py file goes here.

def pttpGET(domain, page=None):
    
    if page:
        request = f"GET {domain}/{page}\n"
        
        
        
    else:
        request = f"GET {domain}\n"  # Request list of pages if no specific page

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client_socket.connect((HOST, PORT))
        client_socket.sendall(request.encode("utf-8"))

        response = ""
        while True:
            chunk = client_socket.recv(4096).decode("utf-8")
            if not chunk:
                break
            response += chunk
        
        return response

    except ConnectionRefusedError:
        print("Error: Could not connect to the PTTP server.")
    finally:
        client_socket.close()