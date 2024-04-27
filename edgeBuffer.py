import socket
import json
import time
import datetime
from influx import influx_connection, Point
import sqlite3

conn = sqlite3.connect('robot_data.db')
cursor = conn.cursor()

#robot functions
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
        sock.settimeout(1)
        sock.connect((ip, port))
        return True, sock
    except Exception as e:
        print("Error connecting to controller:", e)
        return False, None

def disconnect_from_controller(sock) -> object:
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
        
#functions to get values from controller
def get_servo_status(sock):
    suc, servoStatus, id = send_command(sock, "getServoStatus")
    print("Servo Status is: ", servoStatus)
    return servoStatus

def get_tcp_pose(sock):
    suc, tcp, id = send_command(sock, "get_tcp_pose", {"tool_num": 0})
    print("Tool Number is: ", tcp)
    return tcp

def get_cycle_mode(sock):
    suc, cycle_Mode, id = send_command(sock, "getCycleMode")
    print("Cycle mode is: ", cycle_Mode)
    return cycle_Mode

def get_ellapse_time(sock):
    suc, ellapse_time, id = send_command(sock, "getSysVarD", {"addr": 7})
    print("ellapse_time is: ", ellapse_time)
    return ellapse_time

def get_cycle_count(sock):
    suc, cycle_count, id = send_command(sock, "getSysVarD", {"addr": 8})
    print("Cycle_count is: ", cycle_count)
    return cycle_count

def get_robot_state(sock):
    suc, robotState, id = send_command(sock, "getRobotState")
    print("Robot Status is: ", robotState)
    return robotState

def get_emergency_stop_state(sock):
    suc, emergencyStopState, id = send_command(sock, "get_estop_status")
    print("EmergencyStopState of robot state is : ", emergencyStopState)
    return emergencyStopState

def get_joint_speed(sock):
    suc, joint_speed, id = send_command(sock, "get_joint_speed")
    print("Joint Speed of robot state is : ", joint_speed)
    return joint_speed

def get_robot_mode(sock):
    suc, RobotMode, id = send_command(sock, "getRobotMode")
    print("RobotMode is : ", RobotMode)
    return RobotMode

def get_joint_torques(sock):
    suc, joint_torques, id = send_command(sock, "get_joint_torques")
    print("joint_torque is : ", joint_torques)
    return joint_torques

def get_joint_acc(sock):
    suc, joint_acc, id = send_command(sock, "get_joint_acc")
    print("joint_torque is : ", joint_acc)
    return joint_acc

def get_software_version(sock):
    suc, SoftVersion, id = send_command(sock, "getSoftVersion")
    print("Software_version is : ", SoftVersion)
    return SoftVersion

def get_joint_version(sock):
    suc, jointVersion, id = send_command(sock, "getJointVersion", {"axis": 0})
    print("getJointVersion is : ", jointVersion)
    return jointVersion

def get_collision_status(sock):
    suc, collisionStatus, id = send_command(sock, "getCollisionState")
    print("collisionStatys is : ", collisionStatus)
    return collisionStatus

#database connectivity
def create_influxdb_point(servoStatus, tcp, cycle_Mode,
                    ellapse_time, cycle_count, 
                    robotState, emergencyStopState, 
                    joint_speed, RobotMode, 
                    joint_torques, joint_acc, 
                    SoftVersion, jointVersion, collisionStatus):  # Add set_servo_status under Braces
    uniqueid = "OWL1"
    point = Point("port8055") \
        .tag("Robot_id", "Owl_1") \
        .field("ServoStatus", servoStatus) \
        .field("Cycle_Mode", cycle_Mode) \
        .field("RobotState", robotState) \
        .field("EmergencyStopState", emergencyStopState) \
        .field("Base_Speed", float(joint_speed[0])) \
        .field("Shoulder_Speed", float(joint_speed[1])) \
        .field("Elbow_Speed", float(joint_speed[2])) \
        .field("Wrist1_Speed", float(joint_speed[3])) \
        .field("Wrist2_Speed", float(joint_speed[4])) \
        .field("Wrist3_Speed", float(joint_speed[5])) \
        .field("Robot_Mode", RobotMode) \
        .field("Base_Torque", round(joint_torques[0],2)) \
        .field("Shoulder_Torque", round(joint_torques[1],2)) \
        .field("Elbow_Torque", round(joint_torques[2],2)) \
        .field("Wrist1_Torque", round(joint_torques[3],2)) \
        .field("Wrist2_Torque", round(joint_torques[4],2)) \
        .field("Wrist3_Torque", round(joint_torques[5],2)) \
        .field("Base_Acc", float(joint_acc[0])) \
        .field("Shoulder_Acc", float(joint_acc[1])) \
        .field("Elbow_Acc", float(joint_acc[2])) \
        .field("Wrist1_Acc", float(joint_acc[3])) \
        .field("Wrist2_Acc", float(joint_acc[4])) \
        .field("Wrist3_Acc", float(joint_acc[5])) \
        .field("Software_Version", SoftVersion) \
        .field("jointVersion", jointVersion) \
        .field("uniqueID", uniqueid) \
        .field("collisionStatus", collisionStatus)        #Servo version uncomment on line 146,147 and add_on 157, 78
        #.field("cycle_time", cycle_time["code"]) \
        #.field("cycle_count", cycle_count) \
        #.field("ellapse_time", ellapse_time) \

    return point

def write_to_influxdb(servoStatus, tcp, cycle_Mode, ellapse_time, 
                    cycle_count, robotState, emergencyStopState, 
                    joint_speed, RobotMode, joint_torques, joint_acc, 
                    SoftVersion, jointVersion, collisionStatus):

    influx_client = influx_connection()

    influx_point = create_influxdb_point(servoStatus, tcp, cycle_Mode, ellapse_time, cycle_count, robotState,
                                         emergencyStopState, joint_speed, RobotMode, joint_torques, joint_acc,
                                         SoftVersion, jointVersion, collisionStatus)

    try:
        influx_client.write(database="final", record=influx_point)
        print("Data successfully written to InfluxDB")
        delete_from_sql()
    except Exception as e:
        print(f"Error writing data to InfluxDB: {e}")

def create_sqlite_table() -> None:
    """Inserts robot data into a SQLite database table

    Args:
        conn: The connection object to the SQLite database
    """

    fields = [
    "ServoStatus", "Cycle_Mode", "RobotState", "EmergencyStopState",
    "Base_Speed", "Shoulder_Speed", "Elbow_Speed",
    "Wrist1_Speed", "Wrist2_Speed", "Wrist3_Speed",
    "Robot_Mode", "Base_Torque", "Shoulder_Torque", "Elbow_Torque",
    "Wrist1_Torque", "Wrist2_Torque", "Wrist3_Torque",
    "Base_Acc", "Shoulder_Acc", "Elbow_Acc",
    "Wrist1_Acc", "Wrist2_Acc", "Wrist3_Acc",
    "Software_Version", "jointVersion", "uniqueID", "collisionStatus"   
    ]

    sql_query = (
    "CREATE TABLE IF NOT EXISTS robot_data (id SERIAL PRIMARY KEY,\n" +
    "    ServoStatus TEXT,\n" +
    "    Cycle_Mode TEXT,\n" +
    "    RobotState TEXT,\n" +
    "    EmergencyStopState TEXT,\n" +
    "    Base_Speed TEXT,\n" +
    "    Shoulder_Speed TEXT,\n" +
    "    Elbow_Speed TEXT,\n" +
    "    Wrist1_Speed TEXT,\n" +
    "    Wrist2_Speed TEXT,\n" +
    "    Wrist3_Speed TEXT,\n" +
    "    Robot_Mode TEXT,\n" +
    "    Base_Torque TEXT,\n" +
    "    Shoulder_Torque TEXT,\n" +
    "    Elbow_Torque TEXT,\n" +
    "    Wrist1_Torque TEXT,\n" +
    "    Wrist2_Torque TEXT,\n" +
    "    Wrist3_Torque TEXT,\n" +
    "    Base_Acc TEXT,\n" +
    "    Shoulder_Acc TEXT,\n" +
    "    Elbow_Acc TEXT,\n" +
    "    Wrist1_Acc TEXT,\n" +
    "    Wrist2_Acc TEXT,\n" +
    "    Wrist3_Acc TEXT,\n" +
    "    Software_Version TEXT,\n" +
    "    jointVersion TEXT,\n" +
    "    uniqueID TEXT,\n" +
    "    collisionStatus TEXT\n" +
    ");")

    cursor.execute(sql_query)       
    conn.commit()

def delete_from_sql() -> None:
    try:
        delete_query = "DELETE FROM sample_table WHERE rowid IN (SELECT rowid FROM sample_table LIMIT 1);"    # Assuming an "id" column for unique identification
        sqlite_cursor.execute(delete_query, (row[0],))  # Use the first column value (adjust if needed)
        conn.commit()
    except Exception as e:
        print(f"Error deleeting from SQLite :{e}")

def write_to_sqlite(servoStatus, tcp, cycle_Mode, ellapse_time, cycle_count, robotState,
                              emergencyStopState, joint_speed, RobotMode, joint_torques, joint_acc,
                              SoftVersion, jointVersion, collisionStatus) -> None:
    values = {
        "ServoStatus": servoStatus,
        "Cycle_Mode": cycle_Mode,
        "RobotState": robotState,
        "EmergencyStopState": emergencyStopState,
        "Base_Speed": float(joint_speed[0]),
        "Shoulder_Speed": float(joint_speed[1]),
        "Elbow_Speed": float(joint_speed[2]),
        "Wrist1_Speed": float(joint_speed[3]),
        "Wrist2_Speed": float(joint_speed[4]),
        "Wrist3_Speed": float(joint_speed[5]),
        "Robot_Mode": RobotMode,
        "Base_Torque": round(joint_torques[0], 2),
        "Shoulder_Torque": round(joint_torques[1], 2),
        "Elbow_Torque": round(joint_torques[2], 2),
        "Wrist1_Torque": round(joint_torques[3], 2),
        "Wrist2_Torque": round(joint_torques[4], 2),
        "Wrist3_Torque": round(joint_torques[5], 2),
        "Base_Acc": float(joint_acc[0]),
        "Shoulder_Acc": float(joint_acc[1]),
        "Elbow_Acc": float(joint_acc[2]),
        "Wrist1_Acc": float(joint_acc[3]),
        "Wrist2_Acc": float(joint_acc[4]),
        "Wrist3_Acc": float(joint_acc[5]),
        "Software_Version": SoftVersion,
        "jointVersion": jointVersion,
        "uniqueID": uniqueid,
        "collisionStatus": collisionStatus
    }

    try:
        sql_insert_query = """
        INSERT INTO robot_data (ServoStatus, Cycle_Mode, RobotState, EmergencyStopState,
                            Base_Speed, Shoulder_Speed, Elbow_Speed,
                            Wrist1_Speed, Wrist2_Speed, Wrist3_Speed,
                            Robot_Mode, Base_Torque, Shoulder_Torque, Elbow_Torque,
                            Wrist1_Torque, Wrist2_Torque, Wrist3_Torque,
                            Base_Acc, Shoulder_Acc, Elbow_Acc,
                            Wrist1_Acc, Wrist2_Acc, Wrist3_Acc,
                            Software_Version, jointVersion, uniqueID, collisionStatus)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """

        # Values to be inserted into the table (in the same order as the columns), excluding 'id'
        values_to_insert = (
            values["ServoStatus"], values["Cycle_Mode"], values["RobotState"], values["EmergencyStopState"],
            values["Base_Speed"], values["Shoulder_Speed"], values["Elbow_Speed"],
            values["Wrist1_Speed"], values["Wrist2_Speed"], values["Wrist3_Speed"],
            values["Robot_Mode"], values["Base_Torque"], values["Shoulder_Torque"], values["Elbow_Torque"],
            values["Wrist1_Torque"], values["Wrist2_Torque"], values["Wrist3_Torque"],
            values["Base_Acc"], values["Shoulder_Acc"], values["Elbow_Acc"],
            values["Wrist1_Acc"], values["Wrist2_Acc"], values["Wrist3_Acc"],
            values["Software_Version"], values["jointVersion"], values["uniqueID"], values["collisionStatus"]
        )

        # Execute the INSERT query with the corrected number of values
        cursor.execute(sql_insert_query, values_to_insert)

        write_to_influxdb(servoStatus, tcp, cycle_Mode, ellapse_time, cycle_count, robotState,
                              emergencyStopState, joint_speed, RobotMode, joint_torques, joint_acc,
                              SoftVersion, jointVersion, collisionStatus)
        
        delete_from_sql()


    except sqlite3.Error as error:
        print(f"Error writing to SQLite: {error}")

def main() -> None:
    
    while True:
        robot_ip = "192.168.1.200"
        conSuc, sock = connectETController(robot_ip)

        if conSuc and sock is not None:
            servoStatus = get_servo_status(sock)
            tcp = get_tcp_pose(sock)
            cycle_Mode = get_cycle_mode(sock)
            ellapse_time = get_ellapse_time(sock)
            cycle_count = get_cycle_count(sock)
            robotState = get_robot_state(sock)
            emergencyStopState = get_emergency_stop_state(sock)
            joint_speed = get_joint_speed(sock)
            RobotMode = get_robot_mode(sock)
            joint_torques = get_joint_torques(sock)
            joint_acc = get_joint_acc(sock)
            SoftVersion = get_software_version(sock)
            jointVersion = get_joint_version(sock)
            collisionStatus = get_collision_status(sock)

            create_sqlite_table() 
            write_to_sqlite(servoStatus, tcp, cycle_Mode, ellapse_time, cycle_count, robotState,
                              emergencyStopState, joint_speed, RobotMode, joint_torques, joint_acc,
                              SoftVersion, jointVersion, collisionStatus)

if __name__ == "__main__": 
    main()