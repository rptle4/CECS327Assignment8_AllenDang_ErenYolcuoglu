import socket


def run_server():
    server_port = int(input("Enter the port number for the server: "))

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#create tcp socket

    server_socket.bind(('0.0.0.0', server_port)) #socket binded to port

    server_socket.listen(1)#listening for connections allowing only 1 client to connect
    print(f"Server port: {server_port} is now listening")

    connection, client_address = server_socket.accept() #accepts connection from client
    print(f"Connected to: {client_address}")

    try:
        while True:
            data = connection.recv(1024)#recieve message from client
            if not data:
                break

            print(f"Message received from client: {data.decode()}")
            response = data.decode().upper() #change the client's message to be uppercase

            connection.sendall(response.encode()) #encodes and sends message back to client

    except Exception as error:
        print(f"ERROR: {error}")

    finally:
        connection.close() #closes socket
        print("Connection with client closed. Exiting program.")

if __name__ == "__main__":
    run_server()
