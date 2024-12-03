import socket
import ipaddress
import pymongo
import datetime

def get_device_uid(meta, device_name):
    query = {
        "customAttribute.name": device_name
    }
    doc = meta.find_one(query)
    return doc.get("assetUid")

def query_one(meta, virtual):
    fridge1 = get_device_uid(meta, "Smart Fridge 1")
    fridge2 = get_device_uid(meta, "Smart Fridge 2")
    current_date_time = datetime.datetime.now(datetime.timezone.utc) #utc is just universal time format thing which is what mongo is using
    three_hours_ago = current_date_time - datetime.timedelta(hours=3)

    fridge1_query = {
        {
            "payload.parent_asset_uid": fridge1,
            "time": {
                "$gte": three_hours_ago,
                "$lte": current_date_time
            }
        }
    }

    fridge2_query = {
        {
            "payload.parent_asset_uid": fridge2,
            "time": {
                "$gte": three_hours_ago,
                "$lte": current_date_time
            }
        }
    }

    fridge1_docs = virtual.find(fridge1_query)
    fridge2_docs = virtual.find(fridge2_query)

    total_docs = 0
    total_moisture = 0

    for doc in fridge1_docs:
        moisture1 = doc.get("payload", {}).get("Moisture Meter - Fridge 1 Moisture Sensor")
        if moisture1 is not None:
            total_docs += 1
            total_moisture += float(moisture1)

    for doc in fridge2_docs:
        moisture2 = doc.get("payload", {}).get("Moisture Meter - Fridge 2 Moisture Sensor")
        if moisture2 is not None:
            total_docs += 1
            total_moisture += float(moisture2)

    avg_moisture = total_moisture / total_docs
    return f"The avg moisture inside my kitchen fridge in the past three hours is: {avg_moisture}."



if __name__ == "__main__":
    cluster = pymongo.MongoClient("mongodb+srv://akdang592:!12Reptile592#@cecs327cluster.mcrn6.mongodb.net/")
    database = cluster["test"]
    metadata = database["Assignment7_Metadata"]
    virtual = database["Assignment7_Virtual"]

    print("Initializing Server")
    Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    hostname = socket.gethostname()
    ipaddress = socket.gethostbyname(hostname)
    Socket.bind((ipaddress, 0))
    port = Socket.getsockname()[1]
    Socket.listen(1)
    print("Server is listening...")
    print(f"port is {port}")
    incomingSocket, incomingAddress = Socket.accept()
    maxBytes = 1028


    while True:
        incoming = incomingSocket.recv(maxBytes)
        client_message = incoming.decode()
        print(f"Client message: {client_message}")
        result = ''
        if client_message == '4':
            print("Closing the server...")
            break
        elif client_message == '1':
            result = query_one(metadata, virtual)

        incomingSocket.send(bytearray(str(result), encoding='utf-8'))

    incomingSocket.close()
    print("Connection with the client is now closed")