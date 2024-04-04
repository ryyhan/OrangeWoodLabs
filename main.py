import socket
import struct
import collections
import time
import json
import paho.mqtt.client as mqtt
import threading
import os, time
from influxdb_client_3 import InfluxDBClient3, Point

#importing self defined files
from influx import influx_connection
from mqtt import *
from preprocessing import *



HOST = "192.168.1.200" #HOST ID
PORT = 8056   #Port Id 
PACKET_SIZE = 1024 #Data Packet Size 
SLEEP_INTERVAL = 0.10 #Default Sleep Inetrval



# Global variable to store unpacked data this Dictionary will store the Unpacked Data.
global unpacked_data
unpacked_data = {}

#variable to store start time
cycle_start_time = None
RTT = None
ping_start_time = None
CycleTime = None
PowerOnTime = None


def mqtt_worker():
    """
    This function establishes an MQTT connection, sets up callback functions 
    for message received, connection events, and (optionally) message published,
    and then starts the network loop to handle communication with the broker.

    The function performs the following steps:

    1. Initializes an MQTT client object.
    2. Assigns callback functions for:
      - `on_message`: Handles incoming messages on subscribed topics.
      - `on_connect`: Handles successful or failed connection attempts.
      - `on_publish` (optional): Handles successful or failed message publishing 
                         (uncomment the line to enable).
    3. Connects to the specified MQTT broker (address, port, and keep-alive interval).
    4. Starts the network loop to continuously process incoming and outgoing messages,
     handle reconnection attempts (if configured), and maintain the connection with the broker.
    """
    # Initialize MQTT client
    mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    mqttc.on_message = on_mqtt_message
    mqttc.on_connect = on_mqtt_connect
    mqttc.on_publish = on_mqtt_publish
    # Uncomment to enable debug messages
    # mqttc.on_log = on_mqtt_log
    mqttc.connect("broker.hivemq.com", 1883, 60) #Address of HOST,IP and Time Interval in seconds
    mqttc.loop_start()

    while True:

        # Publish data to MQTT broker
        print("Data for mqtt")
        decoded_data = {key: value.decode() if isinstance(value, bytes) else value for key, value in unpacked_data.items()}
        print(json.dumps(decoded_data))
        mqttc.publish("demo", json.dumps(decoded_data)) #MQTTC Published Data On the Basis of Unpacked Data
        time.sleep(1) #Defined Sleep Interval
        
        #########
        
        write_unpacked_data_to_influxdb(unpacked_data)

        ##recording time
        
        if unpacked_data["RobotState"] == 3:
            cycle_start_time = time.time()
        elif unpacked_data["RobotState"] == 1:
            pass
        elif unpacked_data["RobotState"] == 0:  
            if cycle_start_time is not None:
                cycle_end_time = time.time()  # Stop recording time
                CycleTime = cycle_end_time - cycle_start_time
                print("Time", CycleTime)
        
        RobotUtilisation = (CycleTime/PowerOnTime)*100



def socket_worker():
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:  #Created Server
                s.settimeout(8)  #Time Trigger TIME

                socket_start_time = time.time() #logging time to calculate RTT
                s.connect((HOST, PORT))
                socket_end_time = time.time() #logging time to calculate RTT

                RTT = ((socket_end_time - socket_start_time) * 1000) #in milliseconds
                
                if RTT is not None:
                    if ping_start_time is None:  
                        ping_start_time = time.time()
                        print(f"Machine {host}:{PORT} responded in {RTT:.2f} milliseconds")
                else:  
                    if ping_start_time is not None:  # Machine just became unreachable
                        ping_end_time = time.time()
                    else:
                        print(f"Machine {host}:{PORT} is currently unreachable.")

                PowerOnTime = ping_end_time - ping_start_time
                print(PowerOnTime)


                index = 0
                lost = 0

                while True:  #Upto True Entire Function Under loop
                    data = s.recv(PACKET_SIZE)
                    if len(data) != PACKET_SIZE:
                        lost += 1
                        # print("Lost:", lost)
                        continue

                    # Unpack data
                    unpacked_data = unpack_data(data)

                    # Print data every 10 iterations
                    #if index % 10 == 0:
                       # print_data()

                    index += 1
                    # time.sleep(SLEEP_INTERVAL)

        except (socket.timeout, ConnectionError) as e:
            print("Error:", e)
            continue


def write_unpacked_data_to_influxdb(unpacked_data1,database="data_testing"):
    point = Point("machine_data")
    tags = {}  # Separate dictionary for tags
    fields = {}  # Separate dictionary for fields

    print(type(unpacked_data1))
    # Separate tags and fields based on data types
    for key, value in unpacked_data1.items():
        if isinstance(value, str):
            tags[key] = value
        else:
            fields[key] = value
      
    # Add tags
    for key, value in tags.items():
        point.tag(key, value)

    # Add fields 
    for key, value in fields.items():
        point.field(key, value)


    try:
        #print(*(str(point).split(",")),sep="\n")
        influx_client.write(database=database, record=point)
    except Exception as e:
        print(f"Error writing data to InfluxDB: {e}")

def main():


    global influx_client
    influx_client = influx_connection()
    mqtt_thread = threading.Thread(target=mqtt_worker)  #Each thread is initialized with a target function (mqtt_worker and socket_worker), which represents the function that the thread will execute.
    socket_thread = threading.Thread(target=socket_worker) #They are Thraeds

    mqtt_thread.start()
    socket_thread.start()

    mqtt_thread.join()
    socket_thread.join()

if __name__ == "__main__":  #conditional block ensures that the main() function is executed only if the script is run directly
    main()