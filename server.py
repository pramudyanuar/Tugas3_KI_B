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

    while True:
        client_socket, client_address = server.accept()
        print(f"Koneksi dari {client_address}")
        clients.append(client_socket)
        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()

if __name__ == "__main__":
    main()
