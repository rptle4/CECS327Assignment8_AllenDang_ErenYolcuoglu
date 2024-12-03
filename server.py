import socket
import pymongo
import datetime

# Helper function to get the device UID
def get_device_uid(device_name):
    DEVICE_UIDS = {
        "Smart Refrigerator": "rs4-53t-fqm-n91",
        "Smart Refrigerator 2": "b9392566-1b1d-42e4-9c4e-f393f135f876",
        "Smart Dishwasher": "22066b7d-9880-4364-957c-69c2573806a7"
    }
    return DEVICE_UIDS.get(device_name)

# Query 1: Average Moisture in Fridges
def query_one(meta, virtual):
    fridge1_uid = get_device_uid("Smart Refrigerator")
    fridge2_uid = get_device_uid("Smart Refrigerator 2")

    if not fridge1_uid or not fridge2_uid:
        return "Error: Metadata for one or both refrigerators is missing. Cannot process query."

    current_time = datetime.datetime.now(datetime.timezone.utc)
    three_hours_ago = current_time - datetime.timedelta(hours=3)

    fridge1_query = {
        "payload.parent_asset_uid": fridge1_uid,
        "time": {"$gte": three_hours_ago, "$lte": current_time}
    }
    fridge2_query = {
        "payload.parent_asset_uid": fridge2_uid,
        "time": {"$gte": three_hours_ago, "$lte": current_time}
    }

    fridge1_docs = virtual.find(fridge1_query)
    fridge2_docs = virtual.find(fridge2_query)

    total_docs = 0
    total_moisture = 0

    for doc in fridge1_docs:
        moisture = doc.get("payload", {}).get("Moisture Meter - Sensor1")
        if moisture:
            total_docs += 1
            total_moisture += float(moisture)

    for doc in fridge2_docs:
        moisture = doc.get("payload", {}).get("Moisture Meter - Sensor2")
        if moisture:
            total_docs += 1
            total_moisture += float(moisture)

    if total_docs == 0:
        return "No moisture data found for the past three hours."

    avg_moisture = total_moisture / total_docs
    return f"The average relative humidity (RH%) inside the kitchen fridge in the past three hours is {avg_moisture:.2f}%."

# Query 2: Average Water Usage in Dishwasher
def query_two(meta, virtual):
    # Use the confirmed assetUid for Smart Dishwasher
    dishwasher_uid = "2206b67d-9880-4364-957c-69c2573806a7"

    current_time = datetime.datetime.now(datetime.timezone.utc)
    three_hours_ago = current_time - datetime.timedelta(hours=3)

    # Query dishwasher documents in the last 3 hours
    dishwasher_query = {
        "payload.parent_asset_uid": dishwasher_uid,
        "time": {"$gte": three_hours_ago, "$lte": current_time}
    }

    dishwasher_docs = virtual.find(dishwasher_query)

    total_cycles = 0
    total_water = 0

    for doc in dishwasher_docs:
        # Access the Water Flow Sensor field
        water_usage = doc.get("payload", {}).get("Water Flow Sensor")
        if water_usage:
            total_cycles += 1
            total_water += float(water_usage)

    if total_cycles == 0:
        return "No water usage data found for the past three hours."

    avg_water = total_water / total_cycles
    return f"The average water consumption per cycle in the smart dishwasher is {avg_water:.2f} gallons."

# Query 3: Highest Electricity Consumption
def query_three(meta, virtual):
    devices = ["Smart Refrigerator", "Smart Refrigerator 2", "Smart Dishwasher"]
    max_consumption = 0
    max_device = ""

    current_time = datetime.datetime.now(datetime.timezone.utc)
    three_hours_ago = current_time - datetime.timedelta(hours=3)

    for device in devices:
        device_uid = get_device_uid(device)
        if not device_uid:
            continue

        query = {
            "payload.parent_asset_uid": device_uid,
            "time": {"$gte": three_hours_ago, "$lte": current_time}
        }

        docs = virtual.find(query)

        # Use correct field names for electricity data
        electricity_field = {
            "Smart Refrigerator": "Ammeter",
            "Smart Refrigerator 2": "Ammeter 2",
            "Smart Dishwasher": "Ammeter (dishwasher)"
        }[device]

        total_consumption = sum(float(doc.get("payload", {}).get(electricity_field, 0)) for doc in docs)
        if total_consumption > max_consumption:
            max_consumption = total_consumption
            max_device = device

    if max_device == "":
        return "No electricity usage data found for the past three hours."

    return f"The device that consumed the most electricity is {max_device} with {max_consumption:.2f} kWh."

# Main server logic
if __name__ == "__main__":
    cluster = pymongo.MongoClient("mongodb+srv://erenyolcuoglu01:2H7kyhOB9VU6SkKI@327-cluster0.jm4f2.mongodb.net/")
    database = cluster["test"]
    metadata = database["Assignment7_metadata"]
    virtual = database["Assignment7_virtual"]

    print("Initializing Server")
    server_ip = input("Enter the IP address to bind the server: ")
    server_port = int(input("Enter the port to bind the server: "))
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_ip, server_port))
    server_socket.listen(1)
    print(f"Server is listening on {server_ip}:{server_port}")

    incoming_socket, incoming_address = server_socket.accept()
    max_bytes = 1024

    while True:
        incoming = incoming_socket.recv(max_bytes)
        client_message = incoming.decode()
        print(f"Client message: {client_message}")
        result = ''

        if client_message == '1':
            result = query_one(metadata, virtual)
        elif client_message == '2':
            result = query_two(metadata, virtual)
        elif client_message == '3':
            result = query_three(metadata, virtual)
        else:
            result = "Invalid query. Please try one of the valid queries."

        incoming_socket.send(bytearray(str(result), encoding='utf-8'))

    incoming_socket.close()
    print("Connection with the client is now closed")
