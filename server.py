import socket
import threading
import random
from math import gcd

# Generate RSA keys
def generate_rsa_keys():
    def is_prime(num):
        if num < 2:
            return False
        for i in range(2, int(num**0.5) + 1):
            if num % i == 0:
                return False
        return True

    def generate_prime():
        while True:
            p = random.randint(100, 999)
            if is_prime(p):
                return p

    p = generate_prime()
    q = generate_prime()
    n = p * q
    phi = (p - 1) * (q - 1)

    e = random.choice([x for x in range(2, phi) if gcd(x, phi) == 1])
    d = pow(e, -1, phi)
    return (e, n), (d, n)

public_key, private_key = generate_rsa_keys()
print(f"Public Key: {public_key}, Private Key: {private_key}")

clients = []  # List of connected clients


def broadcast_message(message, sender_socket=None):
    """Broadcast message to all clients except sender"""
    for client_socket in clients:
        if client_socket != sender_socket:
            try:
                client_socket.sendall(message.encode('utf-8'))
            except Exception as e:
                print(f"[ERROR] Unable to send message to client: {e}")


def handle_client(client_socket):
    clients.append(client_socket)
    client_socket.sendall(f"{public_key[0]},{public_key[1]}".encode('utf-8'))

    encrypted_key = int(client_socket.recv(1024).decode('utf-8'))
    shared_key = pow(encrypted_key, private_key[0], private_key[1])
    print(f"Shared key decrypted: {shared_key}")

    while True:
        try:
            encrypted_message = client_socket.recv(1024).decode('utf-8')
            if encrypted_message:
                print(f"Encrypted message received: {encrypted_message}")
                decrypted_message = ''.join(
                    chr(pow(int(char), private_key[0], private_key[1]))
                    for char in encrypted_message.split(',')
                )
                print(f"Decrypted message: {decrypted_message}")
                broadcast_message(f"Client: {decrypted_message}", sender_socket=client_socket)
            else:
                break
        except Exception as e:
            print(f"[ERROR] Error handling client: {e}")
            break

    client_socket.close()
    clients.remove(client_socket)
    print(f"[INFO] Client disconnected. Remaining clients: {len(clients)}")


def server_program():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 12345))
    server_socket.listen(5)
    print("[START] Server is listening for connections...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"[CONNECTED] New client connected from {client_address}")
        threading.Thread(target=handle_client, args=(client_socket,)).start()


if __name__ == "__main__":
    server_program()
