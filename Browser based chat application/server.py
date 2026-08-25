import socket
import threading

SERVER_IP = '127.0.0.1'
SERVER_PORT = 1489
MAX_CONNECTIONS = 10

connected_users = []

def broadcast(message):
    for user_info in connected_users:
        sock = user_info[1]
        try:
            sock.sendall(message.encode('utf-8'))
        except Exception:
            pass

def handle_incoming_messages(client_socket, handle):
    while True:
        try:
            payload = client_socket.recv(2048).decode('utf-8')
            if payload:
                formatted_payload = handle + "~" + payload
                broadcast(formatted_payload)
            else:
                break
        except Exception:
            break

def process_client_connection(client_socket):
    handle = ""
    while True:
        try:
            raw_name = client_socket.recv(2048).decode('utf-8')
            if raw_name:
                handle = raw_name
                connected_users.append((handle, client_socket))
                notification = "CHATBOT ~" + handle + " joined the chat"
                broadcast(notification)
                break
        except Exception:
            return

    msg_thread = threading.Thread(
        target=handle_incoming_messages, 
        args=(client_socket, handle)
    )
    msg_thread.daemon = True
    msg_thread.start()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        server_socket.bind((SERVER_IP, SERVER_PORT))
        print(f"Running the server on {SERVER_IP} {SERVER_PORT}")
    except Exception as err:
        print(f"Unable to bind to Host {SERVER_IP} and port {SERVER_PORT}: {err}")
        return

    server_socket.listen(MAX_CONNECTIONS)
    
    while True:
        client_sock, client_addr = server_socket.accept()
        print(f"Successfully connected to client {client_addr[0]} {client_addr[1]}")
        
        handler_thread = threading.Thread(
            target=process_client_connection, 
            args=(client_sock,)
        )
        handler_thread.daemon = True
        handler_thread.start()

if __name__ == '__main__':
    start_server()