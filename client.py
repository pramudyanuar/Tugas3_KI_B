import socket
from rsa import generate_rsa_keys, encrypt_rsa

# Generate RSA keys for the client
client_public_key, client_private_key = generate_rsa_keys()

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 5555))  # Connect to the server (localhost)

    # Receive server's public key and store it
    try:
        server_public_key = client.recv(1024).decode()
        print(f"Received server's public key: {server_public_key}")
    except Exception as e:
        print(f"Failed to receive server's public key: {e}")
        return

    # Register client with encrypted ID
    client_id = input("Enter your client ID: ")
    encrypted_client_id = encrypt_rsa(client_id, eval(server_public_key))
    client.send(encrypted_client_id.encode())
    print("Encrypted client ID sent to server.")

    # Send public key to the server
    client.send(str(client_public_key).encode())
    print("Public key sent to server.")

    # Request public keys and addresses
    while True:
        requested_id = input("Enter the ID of the client whose key and address you want (or 'EXIT' to quit): ")
        if requested_id == "EXIT":
            client.send("EXIT".encode())
            print("Exiting...")
            break

        # Encrypt the requester_id and requested_id
        encrypted_request = encrypt_rsa(f"{client_id}:{requested_id}", eval(server_public_key))
        client.send(encrypted_request.encode())

        response = client.recv(1024).decode()
        if response == "Client not found":
            print("Requested client ID not found.")
        elif response == "Unauthorized requester":
            print("You are not authorized to request client info.")
        elif response == "Invalid request format":
            print("The request format is invalid.")
        else:
            print(f"Received client info: {response}")
    
    client.close()

if __name__ == "__main__":
    print(f"Your Public Key: {client_public_key}")
    start_client()
