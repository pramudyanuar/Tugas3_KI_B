import socket
import threading

clients = []  # Untuk menyimpan koneksi client

def broadcast(sender_socket, message):
    """Mengirim pesan ke semua client kecuali pengirim."""
    try:
        for client in clients:
            if client != sender_socket:
                client.send(message)
    except Exception as e:
        print(f"Error saat broadcast: {e}")


def handle_client(client_socket):
    """Menangani komunikasi dengan client."""
    while True:
        try:
            message = client_socket.recv(1024)
            if message:
                print(f"Pesan diterima: {message}")
                broadcast(client_socket, message)
        except:
            clients.remove(client_socket)
            client_socket.close()
            break

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", 5555))  # IP dan port server
    server.listen(5)
    print("Server sedang berjalan...")

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
        client_socket, client_address = server.accept()
        print(f"Koneksi dari {client_address}")
        clients.append(client_socket)
        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()

if __name__ == "__main__":
    main()
