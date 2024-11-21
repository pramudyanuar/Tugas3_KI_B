import socket
import threading

clients = {}  # Dictionary untuk menyimpan {username: client_socket}
groups = {}  # Dictionary untuk menyimpan {group_name: [usernames]}
is_running = True  # Flag untuk menjalankan atau menghentikan server

def broadcast_group(group_name, sender, message):
    """Mengirim pesan ke semua anggota grup tertentu."""
    if group_name in groups:
        for username in groups[group_name]:
            if username != sender and username in clients:
                client_socket = clients[username]
                try:
                    client_socket.send(f"[Grup {group_name}] {sender}: {message}\n".encode())
                except:
                    continue

def handle_client(client_socket, client_address):
    """Menangani komunikasi dengan client."""
    try:
        # Terima username dari client
        username = client_socket.recv(1024).decode()
        if username:
            clients[username] = client_socket
            print(f"User '{username}' terhubung dari {client_address}")
            # Kirim notifikasi ke semua client
            broadcast_group("global", username, f"{username} telah bergabung.")

        while True:
            message = client_socket.recv(1024).decode()
            if message.startswith("LIST_USERS"):
                # Kirim daftar user ke client
                user_list = ", ".join(clients.keys())
                client_socket.send(f"Daftar pengguna: {user_list}\n".encode())
            elif message.startswith("CREATE_GROUP:"):
                # Membuat grup baru
                _, group_name = message.split(":")
                if group_name in groups:
                    client_socket.send(f"Grup '{group_name}' sudah ada.\n".encode())
                else:
                    groups[group_name] = [username]
                    client_socket.send(f"Grup '{group_name}' berhasil dibuat.\n".encode())
            elif message.startswith("JOIN_GROUP:"):
                # Menambahkan user ke grup
                _, group_name = message.split(":")
                if group_name in groups:
                    if username not in groups[group_name]:
                        groups[group_name].append(username)
                        client_socket.send(f"Berhasil bergabung ke grup '{group_name}'.\n".encode())
                    else:
                        client_socket.send(f"Kamu sudah menjadi anggota grup '{group_name}'.\n".encode())
                else:
                    client_socket.send(f"Grup '{group_name}' tidak ditemukan.\n".encode())
            elif message.startswith("SEND_GROUP:"):
                # Mengirim pesan ke grup
                _, group_name, group_message = message.split(":", 2)
                if group_name in groups and username in groups[group_name]:
                    broadcast_group(group_name, username, group_message)
                else:
                    client_socket.send(f"Kamu bukan anggota grup '{group_name}'.\n".encode())
            elif message.startswith("LIST_GROUPS"):
                # Kirim daftar grup ke client
                group_list = ", ".join(groups.keys())
                client_socket.send(f"Daftar grup: {group_list}\n".encode())
            else:
                # Siarkan pesan ke semua user
                broadcast_group("global", username, message)
    except:
        pass
    finally:
        # Hapus user dari daftar jika koneksi terputus
        if username in clients:
            del clients[username]
            print(f"User '{username}' telah terputus.")
            broadcast_group("global", username, f"{username} telah keluar.")
        client_socket.close()

def main():
    global is_running
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", 5555))  # IP dan port server
    server.listen(5)
    print("Server sedang berjalan... (Ketik 'STOP' untuk menghentikan server)")

    def accept_connections():
        """Loop untuk menerima koneksi client."""
        while is_running:
            try:
                server.settimeout(1)  # Timeout 1 detik agar dapat memeriksa flag `is_running`
                client_socket, client_address = server.accept()
                thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
                thread.start()
            except socket.timeout:
                continue

    # Thread untuk menerima koneksi
    thread = threading.Thread(target=accept_connections)
    thread.start()

    # Monitor input untuk menghentikan server
    while is_running:
        command = input()
        if command.strip().lower() == "stop":
            is_running = False
            print("Server sedang dihentikan...")
            break

    thread.join()  # Tunggu hingga thread selesai
    server.close()  # Tutup socket server
    print("Server telah dihentikan.")

if __name__ == "__main__":
    main()
