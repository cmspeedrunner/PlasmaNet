import socket
import os

HOST, PORT = "0.0.0.0", 8888  

def get_page_list(website):
    
    website_path = os.path.join("pages", website)
    
    if not os.path.exists(website_path):
        return "PTTP/1.0 404 Not Found\n\nWebsite not found."
    
    files = os.listdir(website_path)
    page_list = "\n".join(files)
    
    return f"PTTP/1.0 200 OK\n\nAvailable pages:\n{page_list}"

def get_page(path):
    
    file_path = os.path.join("pages", path)
    
    if not os.path.exists(file_path):
        return "PTTP/1.0 404 Not Found\n\nPage not found."
    
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    return f"PTTP/1.0 200 OK\n\n{content}"

def handle_request(request):
    
    try:
        lines = request.split("\n")
        if len(lines) == 0:
            return "PTTP/1.0 400 Bad Request\n\n"

        first_line = lines[0].strip()
        if not first_line.startswith("GET "):
            return "PTTP/1.0 400 Bad Request\n\n"

        _, path = first_line.split(" ", 1)
        path = path.strip()
        
        website = path.split("/")[0]  # Extract domain
        
        if "/" not in path or path.endswith("/"):
            return get_page_list(website)
        else:
            return get_page(path)
    
    except Exception as e:
        return f"PTTP/1.0 500 Internal Server Error\n\n{str(e)}"

def start_server():
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)

    print(f"PTTP Server running on port {PORT}...")

    while True:
        
            client_connection, client_address = server_socket.accept()
            request_data = client_connection.recv(1024).decode("utf-8")
            print(f"Received request from {client_address}:\n{request_data}")

            response = handle_request(request_data)
            client_connection.sendall(response.encode("utf-8"))
            client_connection.close()
        

if __name__ == "__main__":
    start_server()