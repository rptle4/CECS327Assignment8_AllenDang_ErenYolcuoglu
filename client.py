import socket


def run_client():
    server_ip = input("Enter the public IP address of the server: ")
    server_port = int(input("Enter the server port number: "))

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #creates tcp socket
        client_socket.connect((server_ip, server_port)) #connects to server
        print(f"Connected to server: {server_ip} on port: {server_port}")

        while True:
            message = input("Enter a message to send to the server (enter 'exit' to quit): ")
            if not message:
                print("No input, exiting and closing program") #if no input, exits program
                break
            if message.lower() == 'exit':
                print("Exiting and closing program") #exits program
                break

            client_socket.sendall(message.encode()) #encodes and sends the message to the server

            response = client_socket.recv(1024)
            print(f"Server's reply: {response.decode()}") #decodes the response

    except ConnectionError:
        print("Failed to connect to server, try again")
    finally:
        client_socket.close() #closes socket


if __name__ == "__main__":
    run_client()
