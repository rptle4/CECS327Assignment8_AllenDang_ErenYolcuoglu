import socket
import ipaddress


def run():
    try:

        server_ip = str(ipaddress.ip_address(input("Enter IP Address: ")))
        server_port = int(input("Enter Server port: "))
        Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        Socket.connect((server_ip, server_port))
        print("Connection established\n")

    except (ValueError, TypeError) as e:
        print(f"Error: Could not connect to the server. {e}")

    maxBytes = 1024

    while True:
        query = queries()
        Socket.send(bytearray(str(query), encoding='utf-8'))
        print(f"Message sent: {query}")

        if query == '4':
            print("Exiting the program.")
            break

        server_response = Socket.recv(maxBytes)
        print("Server's reply:", server_response.decode())

    Socket.close()
    print("Connection with the server is now closed")

def queries():
    valid_input = ["1", "2", "3", "4"]
    user_input = None

    while user_input not in valid_input:
        print("Select one of the following three queries:\n",
              "1. What is the average moisture inside my kitchen fridge in the past three hours?\n",
              "2. What is the average water consumption per cycle in my smart dishwasher?\n",
              "3. Which device consumed more electricity among my three IoT devices (two refridgerators and a dishwasher)\n",
              "4. Exit the program.\n")

        user_input = str(input("Select '1', '2', '3', or '4'): "))
        if user_input not in valid_input:
            print("Invalid input. Please try again.\n")

    return user_input

if __name__ == "__main__":
    run()



