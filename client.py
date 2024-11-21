import socket
import threading
import random
from rsa import generate_rsa_keys, rsa_encrypt, rsa_decrypt
from des.des import encryption_text as des_encrypt, decryption_text as des_decrypt

# RSA keys
public_key, private_key = generate_rsa_keys()

# DES sederhana
# def des_encrypt(key, plaintext):
#     while len(plaintext) % 8 != 0:
#         plaintext += " "
#     ciphertext = ""
#     for i in range(len(plaintext)):
#         ciphertext += chr(ord(plaintext[i]) ^ ord(key[i % len(key)]))
#     return ciphertext

# def des_decrypt(key, ciphertext):
#     plaintext = ""
#     for i in range(len(ciphertext)):
#         plaintext += chr(ord(ciphertext[i]) ^ ord(key[i % len(key)]))
#     return plaintext.strip()

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
        pka_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Koneksi baru
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
    buffer = ""  # Buffer untuk menyimpan data yang diterima
    while True:
        try:
            data = client_socket.recv(1024).decode()
            buffer += data  # Tambahkan data ke buffer
            while "|END|" in buffer:  # Cek apakah ada pesan lengkap
                message, buffer = buffer.split("|END|", 1)  # Pisahkan pesan lengkap dari buffer
                if "KEY:" in message and "MSG:" in message:
                    try:
                        parts = message.split(";")
                        if len(parts) == 2:
                            encrypted_key = parts[0][4:]  # Hilangkan "KEY:"
                            encrypted_message = parts[1][4:]  # Hilangkan "MSG:"
                            sender, encrypted_message = encrypted_message.split(":", 1)  # Pisahkan sender dan pesan
                            encrypted_key = list(map(int, encrypted_key.split(',')))
                            des_key = rsa_decrypt(private_key, encrypted_key)
                            decrypted_message = des_decrypt(encrypted_message, des_key)
                            print(f"{sender}: {decrypted_message}")
                        else:
                            print("Format data tidak valid.")
                    except Exception as e:
                        print(f"Error dalam memproses data: {e}")
        except Exception as e:
            print(f"Error dalam menerima pesan: {e}")
            client_socket.close()
            break

def send_messages(client_socket, recipient):
    """Mengirim pesan ke server."""
    while True:
        message = input("")
        sender = recipient  # Ambil username pengirim
        des_key = ''.join(random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(8))
        recipient_public_key = get_public_key_from_pka(recipient)
        if not recipient_public_key:
            continue
        encrypted_key = rsa_encrypt(recipient_public_key, des_key)
        encrypted_message = des_encrypt(message, des_key)
        
        # Menambahkan username pengirim ke dalam format pesan
        data = f"KEY:{','.join(map(str, encrypted_key))};MSG:{sender}:{encrypted_message}|END|"
        client_socket.send(data.encode())

def main():
    username = input("Masukkan username Anda: ")
    register_to_pka(username)

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("127.0.0.1", 5555))
    print("Terhubung ke server. Anda dapat mengirim dan menerima pesan.")
    
    recipient = input("Masukkan username penerima: ")

    thread_receive = threading.Thread(target=receive_messages, args=(client_socket,))
    thread_receive.start()

    thread_send = threading.Thread(target=send_messages, args=(client_socket, recipient))
    thread_send.start()

if __name__ == "__main__":
    main()
