import socket
import struct
import collections
import time
import json
import paho.mqtt.client as mqtt
import threading
import os, time
from influxdb_client_3 import InfluxDBClient3, Point
import collections

#importing self defined files
from mqtt import *

token = "SRyXAkm5Ur3PEs6v_g1Qw2Cm64gVZe5sbfhuliQfy5Nlbd-eKidqNjWQ3OERvMIqGZWE6-LzqhYvWpLzC6_7iw=="
org = "VMC_Data_log"
host = "https://us-east-1-1.aws.cloud2.influxdata.com"

influx_client = InfluxDBClient3(host=host, token=token, org=org)

HOST = "192.168.1.200" #HOST ID
PORT = 8056   #Port Id 
PACKET_SIZE = 1024 #Data Packet Size 
SLEEP_INTERVAL = 0.10 #Default Sleep Inetrval



# Global variable to store unpacked data this Dictionary will store the Unpacked Data.
#global unpacked_data
unpacked_data = {}

#variable to store start time
CycleTime = -1
cycle_start_time = -1
RTT = -1
ping_start_time = None
ping_end_time = -1
PowerOnTime = -1

data_format = collections.OrderedDict(
    {
        #"MessageSize": "I",
        #"TimeStamp": "Q",
        "autorun_cycleMode": "B",
        #"machinePos01": "d",
        #"machinePos02": "d",
        #"machinePos03": "d",
        #"machinePos04": "d",
        #"machinePos05": "d",
        #"machinePos06": "d",
        #"machinePos07": "d",
        #"torque04": "d",
        #"torque05": "d",
        #"torque06": "d",
        #"torque07": "d",
        #"torque08": "d",
        "robotState": "d",
        "servoReady": "i",
        #"can_motor_run": "i",
        #"motor_speed01": "i",
        #"motor_speed02": "i",
        #"motor_speed03": "i",
        #"machinePos08": "d",
        #"machinePose01": "d",
        #"machinePose02": "d",
        #"machinePose03": "d",
        #"machinePose04": "d",
        #"machinePose05": "d",
        #"machinePose06": "d",
        #"machineUserPose01": "d",
        #"machineUserPose02": "d",
        #"machineUserPose03": "d",
        #"machineUserPose04": "d",
        #"machineUserPose05": "d",
        #"machineUserPose06": "d",
        #"torque01": "d",
        #"torque02": "d",
        #"torque03": "d",
        #"motor_speed04": "i",
        #"motor_speed05": "i",
        #"motor_speed06": "i",
        #"motor_speed07": "i",
        #"motor_speed08": "i",
        "robotMode": "i",
        #"analog_ioInput01": "d",
        #"analog_ioInput02": "d",
        #"analog_ioInput03": "d",
        #"analog_ioOutput01": "d",
        #"analog_ioOutput02": "d",
        #"analog_ioOutput03": "d",
        #"analog_ioOutput04": "d",
        #"analog_ioOutput05": "d",
        #"digital_ioInput": "Q",
        #"digital_ioOutput": "Q",
        #"collision": "B",
        #"machineFlangePose01": "d",
        #"machineFlangePose02": "d",
        #"machineFlangePose03": "d",
        #"machineFlangePose04": "d",
        #"machineFlangePose05": "d",
        #"machineFlangePose06": "d",
        #"machineUserFlangePose01": "d",
        #"machineUserFlangePose02": "d",
        #"machineUserFlangePose03": "d",
        #"machineUserFlangePose04": "d",
        #"machineUserFlangePose05": "d",
        #"machineUserFlangePose06": "d",
        "emergencyStopState": "B",
        #"tcp_speed": "d",
        "joint_speed01": "d",
        "joint_speed02": "d",
        "joint_speed03": "d",
        "joint_speed04": "d",
        "joint_speed05": "d",
        "joint_speed06": "d",
        #"joint_speed07": "d",
        #"joint_speed08": "d",
        #"tcpacc": "d",
        "jointacc01": "d",
        "jointacc02": "d",
        "jointacc03": "d",
        "jointacc04": "d",
        "jointacc05": "d",
        "jointacc06": "d",
        #"jointacc07": "d",
        #"jointacc08": "d",
        #"joint_temperature01": "d",
        #"joint_temperature02": "d",
        #"joint_temperature03": "d",
        #"joint_temperature04": "d",
        #"joint_temperature05": "d",
        #"joint_temperature06": "d",
        "joint_torque01": "d",
        "joint_torque02": "d",
        "joint_torque03": "d",
        "joint_torque04": "d",
        "joint_torque05": "d",
        "joint_torque06": "d",
        #"extjoint_torques01": "d",
        #"extjoint_torques02": "d",
        #"extjoint_torques03": "d",
        #"extjoint_torques04": "d",
        #"extjoint_torques05": "d",
        #"extjoint_torques06": "d",
        #"exttcpforceintool01": "d",
        #"exttcpforceintool02": "d",
        #"exttcpforceintool03": "d",
        #"exttcpforceintool04": "d",
        #"exttcpforceintool05": "d",
        #"exttcpforceintool06": "d",
        #"dragState": "B",
        #"joint_pos": "d",
        #"tcp_pos": "d",
        #"CurrentCoord": "i",
        #"CycleMode": "i",
        #"CurrentJobLine": "s",
        #"CurrentEncode": "d",
        #"ToolNumber": "i",
        #"UserNumber": "B",
        #"motor_torque": "d",
        #"PathPointIndex": "i",
        #"teach_switch": "i",
        #"set_tcp": "d",
        #"UserFrame": "i",
        #"CycleMode": "i",
        #"UserFrame": "i",
        #"TcpPos": "d",
        #"Payload": "d",
        #"CentreMass": "i",
        #"RobotType": "i",
        #"DH": "i",
        "CollisionEnable": "i",
        #"CollisionSensitivity": "i",
        #"remote_sys_password": "I",
        #"SafetyParams": "I",
        #"CollisionState": "B",
        #"Speed": "i",
    }
)

def unpack_data(data):
    """
    Unpacks data from a byte stream using the provided data_format dictionary.

    Args:
        data: A byte stream containing the data to unpack.

    Returns:
       A dictionary containing the unpacked data.
   """
    global unpacked_data
    unpacked_data = {}
    for key, fmt in data_format.items():
        fmt_size = struct.calcsize(fmt)   #calculates the size of the data chunk based on the format string using
        data_chunk, data = data[:fmt_size], data[fmt_size:] #Then slices data into a chunk of data (data_chunk) according to the calculated size and removes that chunk from the original data.
        unpacked_data[key] = struct.unpack(f"!{fmt}", data_chunk)[0] #Returns a tuple even if there's only one value, so [0] is used to extract that single value and store it in the unpacked_data dictionary       
       

def print_data():
    """
    Prints the contents of the unpacked_data dictionary.
    """

    print(unpacked_data)
    
    

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
        global CycleTime
        
        if unpacked_data["robotState"] == 3:
            cycle_start_time = time.time()
        elif unpacked_data["robotState"] == 1:
            pass
        elif unpacked_data["robotState"] == 0:  
            if cycle_start_time is not None:
                cycle_end_time = time.time()  # Stop recording time
                CycleTime = cycle_end_time - cycle_start_time
                print("Time", CycleTime)
        
        RobotUtilisation = (CycleTime/PowerOnTime)*100
        print("RobotUtilisation",RobotUtilisation)
        




def socket_worker():
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:  #Created Server
                s.settimeout(8)  #Time Trigger TIME

                socket_start_time = time.time() #logging time to calculate RTT
                s.connect((HOST, PORT))
                socket_end_time = time.time() #logging time to calculate RTT
                
                RTT = ((socket_end_time - socket_start_time) * 1000) #in milliseconds
                
                global ping_start_time
                global ping_end_time
                
                if RTT is not None:
                    if ping_start_time is None:  
                        ping_start_time = time.time()
                        print(f"Machine {HOST}:{PORT} responded in {RTT:.2f} milliseconds")
                else:  
                    if ping_start_time is not None:  # Machine just became unreachable
                        ping_end_time = time.time()
                    else:
                        print(f"Machine {HOST}:{PORT} is currently unreachable.")

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
                    unpack_data(data)

                    # Print data every 10 iterations
                    #if index % 10 == 0:
                       # print_data()

                    index += 1
                    # time.sleep(SLEEP_INTERVAL)

        except (socket.timeout, ConnectionError) as e:
            print("Error:", e)
            continue


def write_unpacked_data_to_influxdb(unpacked_data1,database="final"):
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


    mqtt_thread = threading.Thread(target=mqtt_worker)  #Each thread is initialized with a target function (mqtt_worker and socket_worker), which represents the function that the thread will execute.
    socket_thread = threading.Thread(target=socket_worker) #They are Thraeds

    mqtt_thread.start()
    socket_thread.start()

    mqtt_thread.join()
    socket_thread.join()

if __name__ == "__main__":  #conditional block ensures that the main() function is executed only if the script is run directly
    main()