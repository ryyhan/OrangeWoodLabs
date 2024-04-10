import socket
import json
import time
from influx import influx_connection, Point


def connectETController(ip, port=8055):
    """
    Establishes a connection with the ET controller.

    Parameters:
    - ip (str): IP address of the controller.
    - port (int): Port number for the connection (default is 8055).

    Returns:
    - (bool): True if connection is successful, False otherwise.
    - (socket): Socket object for communication.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((ip, port))
        return True, sock
    except Exception as e:
        print("Error connecting to controller:", e)
        return False, None


def disconnect_from_controller(sock):
    """
    Closes the connection with the controller.

    Parameters:
    - sock (socket): Socket object to be closed.
    """
    if(sock):
        sock.close()
        sock = None
    else:
        sock = None

def send_command(sock, cmd, params=None, id=1):
    """
    Sends a command to the controller and receives the response.

    Parameters:
    - sock (socket): Socket object for communication.
    - cmd (str): Command to be sent.
    - params (dict): Parameters for the command (default is None).
    - id (int): ID for the command (default is 1).

    Returns:
    - (bool): True if command is successful, False otherwise.
    - (dict): Result/error of the command.
    - (int): ID of the command.
    """
    if(not params):
        params =[]
    else:
        params=json.dumps(params)
    sendStr = '{{"method": "{}", "params": {}, "jsonrpc": "2.0", "id": {}}}\n'.format(cmd, params, id)

    try:
        sock.sendall(bytes(sendStr, "utf -8"))
        ret=sock.recv(1024)
        jdata=json.loads(str(ret, "utf -8"))
        if("result" in jdata.keys()):
            return (True, json.loads(jdata["result"]), jdata["id"])
        elif("error" in jdata.keys()):
            return (False, jdata["error"], jdata["id"])
        else:
            return (False, None, None)
    except Exception as e:
        return (False, None, None)
        

def create_influxdb_point(timestamp, servoStatus, tcp, cycle_Mode, cycle_time,
                    ellapse_time, cycle_count, robotState):
    point = Point("port8055") \
        .tag("robot_id", "robot_1") \
        .field("timestamp", timestamp) \
        .field("servoStatus", servoStatus[0]) \
        .field("cycle_Mode", cycle_Mode[0]) \
        .field("cycle_time", cycle_time[0]) \
        .field("ellapse_time", ellapse_time[0]) \
        .field("cycle_count", cycle_count[0]) \
        .field("robotState", robotState[0]) \

    return point

if __name__ == "__main__":
# Robot IP address
    robot_ip = "192.168.1.200"

    conSuc, sock = connectETController(robot_ip)
    if (conSuc):
#Get the servo status of the robotic arm
        suc, servoStatus, id = sendCMD(sock, "getServoStatus")
        print("Servo Status is: ",servoStatus)
        suc, tcp, id = sendCMD(sock, "get_tcp_pose", {"tool_num": 0})
        print("Tool Number is: ",tcp)
        suc, cycle_Mode, id = sendCMD(sock, "getCycleMode")
        print("Cycle mode is: ",cycle_Mode)
        suc, cycle_time, id = sendCMD(sock, "setSysVarD",{"addr":6,"value":123})
        print("Cycle_time is: ",cycle_time)
        suc, ellapse_time, id = sendCMD(sock, "getSysVarD",{"addr":7})
        print("ellapse_time is: ",ellapse_time)
        suc, cycle_count, id = sendCMD(sock, "getSysVarD",{"addr":8})
        print("Cycle_count is: ",cycle_count)
        suc, robotState , id = sendCMD(sock, "getRobotState")
        print("Robot Status is: ",robotState)


        # Establish connection to InfluxDB
        influx_client = influx_connection()

        # Create InfluxDB point
        timestamp = datetime.utcnow().isoformat()
        influx_point = create_influxdb_point(timestamp, servoStatus, tcp, cycle_Mode, cycle_time,
                    ellapse_time, cycle_count, robotState)

        # Write data to InfluxDB
        try:
            influx_client.write(database="final", record = influx_point)
            print("Data successfully written to InfluxDB")
        except Exception as e:
            print(f"Error writing data to InfluxDB: {e}")
