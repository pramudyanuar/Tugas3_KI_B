import socket
import threading
import random
from rsa import generate_rsa_keys, rsa_encrypt, rsa_decrypt

# RSA keys
public_key, private_key = generate_rsa_keys()

# DES sederhana
def des_encrypt(key, plaintext):
    while len(plaintext) % 8 != 0:
        plaintext += " "
    ciphertext = ""
    for i in range(len(plaintext)):
        ciphertext += chr(ord(plaintext[i]) ^ ord(key[i % len(key)]))
    return ciphertext

def des_decrypt(key, ciphertext):
    plaintext = ""
    for i in range(len(ciphertext)):
        plaintext += chr(ord(ciphertext[i]) ^ ord(key[i % len(key)]))
    return plaintext.strip()

def register_to_pka(username):
    """Mendaftarkan kunci publik ke PKA."""
    try:
        pka_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        pka_socket.connect(("127.0.0.1", 6000))
        public_key_str = f"{public_key[0]},{public_key[1]}"
        pka_socket.send(f"REGISTER:{username};{public_key_str}".encode())
        response = pka_socket.recv(1024).decode()
        pka_socket.close()  # Tutup koneksi setelah selesai
        if response == "REGISTERED":
            print("Kunci publik berhasil terdaftar di PKA.")
    except Exception as e:
        print(f"Error saat mencoba mendaftar ke PKA: {e}")

def get_public_key_from_pka(username):
    """Mendapatkan kunci publik dari Public Key Authority."""
    try:
        pka_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        pka_socket.connect(("127.0.0.1", 6000))
        pka_socket.send(f"GET:{username}".encode())
        response = pka_socket.recv(1024).decode()
        pka_socket.close()  # Tutup koneksi setelah selesai
        if response != "NOT_FOUND":
            e, n = map(int, response.split(","))
            return (e, n)
        else:
            print(f"Kunci publik untuk '{username}' tidak ditemukan.")
            return None
    except Exception as e:
        print(f"Error saat mencoba mendapatkan kunci publik dari PKA: {e}")
        return None

def receive_messages(client_socket):
    """Menerima pesan dari server."""
    while True:
        try:
            data = client_socket.recv(1024).decode()
            if data:
                print(data)  # Tampilkan pesan dari server
        except:
            print("Koneksi ke server terputus.")
            break

def chat_group_session(client_socket, group_name):
    """Session untuk chat dalam grup."""
    print(f"Masuk ke group chat '{group_name}'. Ketik 'EXIT' untuk keluar.")
    while True:
        message = input(f"[Grup {group_name}] > ")
        if message.strip().upper() == "EXIT":
            print(f"Keluar dari group chat '{group_name}'.")
            break
        client_socket.send(f"SEND_GROUP:{group_name}:{message}".encode())

def chat_private_session(client_socket, target_username):
    """Session untuk chat pribadi dengan pengguna lain."""
    print(f"Masuk ke private chat dengan '{target_username}'. Ketik 'EXIT' untuk keluar.")
    while True:
        message = input(f"[Private to {target_username}] > ")
        if message.strip().upper() == "EXIT":
            print(f"Keluar dari private chat dengan '{target_username}'.")
            break
        # Enkripsi pesan dengan DES
        des_key = ''.join(random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(8))
        recipient_public_key = get_public_key_from_pka(target_username)
        if not recipient_public_key:
            print(f"User '{target_username}' tidak ditemukan.")
            break

        # Enkripsi DES key menggunakan RSA
        encrypted_key = rsa_encrypt(recipient_public_key, des_key)
        
        # Enkripsi pesan
        encrypted_message = des_encrypt(des_key, message)
        
        # Kirim pesan terenkripsi
        client_socket.send(f"CHAT_WITH:{target_username};KEY:{','.join(map(str, encrypted_key))};MSG:{encrypted_message}".encode())

def send_messages(client_socket):
    """Mengirim pesan ke server."""
    while True:
        print("\nPilihan:")
        print("1. Lihat daftar pengguna yang terhubung")
        print("2. Lihat daftar grup")
        print("3. Buat grup baru")
        print("4. Bergabung ke grup")
        print("5. Kirim pesan ke grup")
        print("6. Kirim pesan pribadi")
        print("7. Keluar")

        choice = input("Masukkan pilihan (1/2/3/4/5/6/7): ")

        if choice == "1":
            # Minta daftar pengguna
            client_socket.send("LIST_USERS".encode())
        elif choice == "2":
            # Minta daftar grup
            client_socket.send("LIST_GROUPS".encode())
        elif choice == "3":
            # Buat grup baru
            group_name = input("Masukkan nama grup: ")
            client_socket.send(f"CREATE_GROUP:{group_name}".encode())
        elif choice == "4":
            # Bergabung ke grup
            group_name = input("Masukkan nama grup: ")
            client_socket.send(f"JOIN_GROUP:{group_name}".encode())
        elif choice == "5":
            # Kirim pesan ke grup
            group_name = input("Masukkan nama grup: ")
            chat_group_session(client_socket, group_name)
        elif choice == "6":
            # Kirim pesan pribadi
            target_username = input("Masukkan username penerima: ")
            chat_private_session(client_socket, target_username)
        elif choice == "7":
            # Keluar
            print("Keluar dari aplikasi.")
            client_socket.close()
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

def main():
    username = input("Masukkan username Anda: ")
    register_to_pka(username)

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("127.0.0.1", 5555))
    client_socket.send(username.encode())  # Kirim username ke server

    print("Terhubung ke server.")

    # Thread untuk menerima pesan
    thread_receive = threading.Thread(target=receive_messages, args=(client_socket,))
    thread_receive.start()

    # Fungsi untuk mengirim pesan
    send_messages(client_socket)

    # Tunggu thread penerima selesai
    thread_receive.join()
    print("Client telah dihentikan.")


if __name__ == "__main__":
    main()
