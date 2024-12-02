import socket

# Creating a TCP/IP socket to locate
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# taking the user's input to enter the IP address and port number of the server
server_ip = input("Enter the IP address of the server: ") 
server_port = int(input("Enter the port number of the server: "))

# Bind the socket to the specified IP address and port number
server_address = (server_ip, server_port)
server_socket.bind(server_address)

# Listen for incoming connections trying to add the code TCp as professor discussed in the class and in the slides.
server_socket.listen(1)
print("Server is running on IP address {} and port number {}".format(server_ip, server_port))

#creating the while loop so it will keep asking untill we close/.
while True:
    # Wait for a connection untill someone joins from client
    connection, client_address = server_socket.accept()
    print("Connection from", client_address)
    try:#using a try catch error since prof asked if there will be error response error happened.
        

        # Receive the data in small chunks and convert to capital letters
        while True:
            data = connection.recv(16)
            
            if data:
                data = data.upper()
                print("Client: {}".format(data.decode()))
                # Send the capitalized data back to the client we will print the data we recieve from clients.
                connection.sendall(data)

                # havind user type some message to the client once he receives
                message = input("Enter a message to send to the client: ")
                message = message.upper()
                # completing the task to do "UPPER CASE" and then send it to clients.
                connection.sendall(message.encode())

            else:
                break

    except Exception as e:#if we get error it will throw an error while doing try and exception
        print("Error occurred: {}".format(e))

    finally:
        # Cleaning up the connection
        connection.close()