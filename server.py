import socket
import threading
from rsa import generate_rsa_keys, decrypt_rsa

# Generate RSA keys for the server
server_public_key, server_private_key = generate_rsa_keys()

# Store client public keys and addresses
client_info = {}

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    try:
        # Send server public key to client
        conn.send(str(server_public_key).encode())
        print("[SERVER] Sent public key to client.")

        # Receive the encrypted client ID
        encrypted_client_id = conn.recv(1024).decode()
        client_id = decrypt_rsa(encrypted_client_id, server_private_key)
        print(f"[CLIENT ID DECRYPTED] {client_id} connected.")

        # Receive the public key of the client
        public_key = conn.recv(1024).decode()
        client_info[client_id] = {"public_key": public_key, "address": addr}
        print(f"[REGISTERED] {client_id} registered with public key: {public_key}")
        
        # Handle key and address requests
        while True:
            data = conn.recv(1024).decode()
            if data == "EXIT":
                break

            try:
                # Data is encrypted; decrypt to get requester_id and requested_id
                decrypted_data = decrypt_rsa(data, server_private_key)
                requester_id, requested_id = decrypted_data.split(":")

                if requester_id not in client_info:
                    conn.send("Unauthorized requester".encode())
                    print(f"[UNAUTHORIZED] {requester_id} attempted to request a key.")
                    continue

                if requested_id in client_info:
                    response = f"{client_info[requested_id]['public_key']}:{client_info[requested_id]['address']}"
                    conn.send(response.encode())
                    print(f"[INFO SENT] Public key and address of {requested_id} sent to {requester_id}")
                else:
                    conn.send("Client not found".encode())
                    print(f"[NOT FOUND] {requested_id} not found for {requester_id}")
            except ValueError:
                conn.send("Invalid request format".encode())
    except Exception as e:
        print(f"[ERROR] {addr}: {e}")
    finally:
        conn.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 5555))
    server.listen(5)
    print(f"[SERVER STARTED] Public Key: {server_public_key}")
    
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

if __name__ == "__main__":
    start_server()
