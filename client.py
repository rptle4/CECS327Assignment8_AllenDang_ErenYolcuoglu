import socket

# Prompt the user to enter the IP address and port number of the server
server_ip = input("Enter the IP address of the server: ") #this will take input from comman line as prompted in the assignment 
server_port = int(input("Enter the port number of the server: ")) #will take port number

while True: #as requested doing the while loop so it will keep asking untill we exit
    # Creating a TCP/IP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:#using a try catch error since prof asked if there will be error response error happened.
        # Connect the socket to the server's IP address and port number
        server_address = (server_ip, server_port)
        client_socket.connect(server_address)

        # # havind user type some message to the server once he connects
        message = input("Enter a message to send to the server: ")

        # Sending message in to the serever
        client_socket.sendall(message.encode())

        # Receive the response from the server and print it
        data = client_socket.recv(1024)
        # print("Server response: {}".format(data.decode()))

        # gets the message from the server and will decode and print 
        data = client_socket.recv(1024)
        print("Server: {}".format(data.decode()))

    except Exception as e: #this will throw an error as i told earlier 
        print("Error occurred: {}".format(e))

    finally:
        # Clean up the socket
        client_socket.close()