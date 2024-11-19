import socket
import threading 

def encrypt_message(message, e, n):
    return ','.join(str(pow(ord(char), e, n)) for char in message)

def rsa_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 12345))

    public_key = client_socket.recv(1024).decode('utf-8')
    e, n = map(int, public_key.split(','))

    shared_key = 12345  # Example shared key
    encrypted_key = pow(shared_key, e, n)
    client_socket.sendall(str(encrypted_key).encode('utf-8'))

    print(f"Sent encrypted shared key: {encrypted_key}")

    def receive_messages():
        while True:
            try:
                message = client_socket.recv(1024).decode('utf-8')
                if message:
                    print(f"Received: {message}")
            except:
                break

    threading.Thread(target=receive_messages).start()

    while True:
        message = input("Enter message: ")
        encrypted_message = encrypt_message(message, e, n)
        client_socket.sendall(encrypted_message.encode('utf-8'))
        print(f"Sent encrypted message: {encrypted_message}")


if __name__ == "__main__":
    rsa_client()
