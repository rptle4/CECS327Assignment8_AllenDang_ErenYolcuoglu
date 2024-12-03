CECS 327
Assignment 8: Build an End-to-End IoT System
Eren Yolcuoglu and Allen Dang


# Project Overview
This project consists of a TCP Client and Server application that processes 
IoT data from a MongoDB database.It allows users to query IoT device data, 
perform calculations, and display results, leveraging metadata for efficient 
query execution.


# Table of Contents
1. [Prerequisites](#Prerequisites)
2. [Setup Instructions](#Setup-Instructions)
3. [Running the Server](#Running-the-Server)
4. [Running the Client](#Running-the-Client)
5. [Database Configuration](#Database-Configuration)



## Prerequisites
Before running the application, ensure the following are installed:

- Python 3.12+
- MongoDB Atlas Account
- Required Python Packages:
    - pymongo
    - socket
    - datetime

Install the required Python packages using:
"pip install pymongo"


## Setup Instructions
- Clone the repository:
"git clone <https://github.com/rptle4/CECS327Assignment8_AllenDang.git>
cd CECS327Assignment8_AllenDang"

- Update Database Credentials:
Modify the connection string in server.py to include your MongoDB Atlas connection URL.


## Running the Server
- Start the Server: 
    - Navigate to the project directory and run:
    "python server.py"

- Enter Server Configuration:
    - Input the IP address and port to bind the server. Example:
    "Enter the IP address to bind the server: 127.21.80.1
    Enter the port to bind the server: 12345"

- Server Listening: 
    - The server will begin listening for client connections:
    "Server is listening on 127.21.80.1:12345"


## Running the Client
- Start the Client: 
    - Run the client from the project directory:
    "python client.py"

- Input Server Details: 
    - Provide the server's IP address and port when prompted. Example:
    "Enter Server IP Address: 127.21.80.1
    Enter Server Port: 12345"

- Execute Queries: 
    -Select a query from the following options:
    "1. What is the average moisture inside my kitchen fridge in the past three hours?"
    "2. What is the average water consumption per cycle in my smart dishwasher?"
    "3. Which device consumed more electricity among my three IoT devices (two refrigerators and a dishwasher)?"
    "4. Exit the program."

- View Results: The client displays the server's response for valid queries. Invalid inputs will prompt a friendly error message.


## Database Configuration
- MongoDB Collections: 
    - Ensure the following collections are available in your MongoDB Atlas:
    + Assignment7_metadata: Contains metadata for IoT devices.
    + Assignment7_virtual: Contains IoT device data logs.

- Connection String: 
    - Update the following line in server.py with your MongoDB connection string:
    "cluster = pymongo.MongoClient("mongodb+srv://erenyolcuoglu01:2H7kyhOB9VU6SkKI@327-cluster0.jm4f2.mongodb.net/")"

- Data Structure:
    - IoT metadata includes assetUid, parentAssetUid, and device types.
    - IoT logs contain sensor readings, timestamps, and relevant metrics.



# Important Notes
- Use the same IP address and port for both the client and server to establish a connection.
- Ensure the MongoDB Atlas database is accessible and contains the required data.
- If any errors occur, check the connection string, database permissions, and server configurations.