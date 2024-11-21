import socket
import threading

# Penyimpanan kunci publik RSA (username -> public_key)
public_keys = {}

def handle_client(client_socket):
    """Menangani permintaan client."""
    client_socket.settimeout(10)  # Timeout 10 detik untuk koneksi
    try:
        data = client_socket.recv(1024).decode()
        if data.startswith("REGISTER:"):
            username, public_key = data[9:].split(";")
            public_keys[username] = public_key
            print(f"User '{username}' mendaftarkan kunci publik: {public_key}")
            client_socket.send("REGISTERED".encode())
        elif data.startswith("GET:"):
            username = data[4:]
            if username in public_keys:
                print(f"User '{username}' meminta kunci publik.")
                client_socket.send(public_keys[username].encode())
            else:
                print(f"User '{username}' tidak ditemukan.")
                client_socket.send("NOT_FOUND".encode())
    except socket.timeout:
        print("Koneksi timeout.")
    except Exception as e:
        print(f"Error dalam menangani permintaan: {e}")
    finally:
        client_socket.close()  # Tutup koneksi setelah selesai

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", 6000))  # Port untuk PKA
    server.listen(5)
    print("Public Key Authority berjalan...")

    while True:
        client_socket, client_address = server.accept()
        print(f"Client terhubung: {client_address}")
        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()

if __name__ == "__main__":
    main()
