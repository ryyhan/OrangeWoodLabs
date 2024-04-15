import socket
import json
import time
import datetime
from influx import influx_connection, Point

CycleTime = -1
cycle_start_time = -1
RobotUtilisation = 0


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
        

def create_influxdb_point(servoStatus, tcp, cycle_Mode, cycle_time,
                    ellapse_time, cycle_count, robotState, emergencyStopState, joint_speed, RobotMode, joint_torques,
                    joint_acc, SoftVersion, jointVersion):  # Add set_servo_status under Braces
    point = Point("port8055") \
        .tag("Robot_id", "Owl_1") \
        .field("ServoStatus", servoStatus) \
        .field("Cycle_Mode", cycle_Mode) \
        .field("RobotState", robotState) \
        .field("EmergencyStopState", emergencyStopState) \
        .field("Base_Speed", joint_speed[0]) \
        .field("Shoulder_Speed", joint_speed[1]) \
        .field("Elbow_Speed", joint_speed[2]) \
        .field("Wrist1_Speed", joint_speed[3]) \
        .field("Wrist2_Speed", joint_speed[4]) \
        .field("Wrist3_Speed", joint_speed[5]) \
        .field("Robot_Mode", RobotMode) \
        .field("Base_Torque", round(joint_torques[0],2)) \
        .field("Shoulder_Torque", round(joint_torques[1],2)) \
        .field("Elbow_Torque", round(joint_torques[2],2)) \
        .field("Wrist1_Torque", round(joint_torques[3],2)) \
        .field("Wrist2_Torque", round(joint_torques[4],2)) \
        .field("Wrist3_Torque", round(joint_torques[5],2)) \
        .field("Base_Acc", joint_acc[0]) \
        .field("Shoulder_Acc", joint_acc[1]) \
        .field("Elbow_Acc", joint_acc[2]) \
        .field("Wrist1_Acc", joint_acc[3]) \
        .field("Wrist2_Acc", joint_acc[4]) \
        .field("Wrist3_Acc", joint_acc[5]) \
        .field("Software_Version", SoftVersion) \
        .field("jointVersion", jointVersion)       
        #.field("Servo_Version", servoVersion)        #Servo version uncomment on line 146,147 and add_on 157, 78
        #.field("cycle_time", cycle_time["code"]) \
        #.field("cycle_count", cycle_count) \
        #.field("ellapse_time", ellapse_time) \

    return point

if __name__ == "__main__":
    
    
    robot_ip = "192.168.1.200"
    conSuc, sock = connectETController(robot_ip)
    if (conSuc == True):
        ping_start_time = time.time()
    
    while (True):
        robot_ip = "192.168.1.200"
        conSuc, sock = connectETController(robot_ip)
        if(conSuc == True and sock is not None): 
            
            suc, servoStatus, id = send_command(sock, "getServoStatus")
            print("Servo Status is: ",servoStatus)
            suc, tcp, id = send_command(sock, "get_tcp_pose", {"tool_num": 0})
            #print("Tool Number is: ",tcp)
            suc, cycle_Mode, id = send_command(sock, "getCycleMode")
            #print("Cycle mode is: ",cycle_Mode)
            suc, ellapse_time, id = send_command(sock, "getSysVarD",{"addr":7})
            #print("ellapse_time is: ",ellapse_time)
            suc, cycle_count, id = send_command(sock, "getSysVarD",{"addr":8})
            #print("Cycle_count is: ",cycle_count)
            suc, robotState , id = send_command(sock, "getRobotState")
            #print("Robot Status is: ",robotState)
            suc, emergencyStopState , id = send_command(sock, "get_estop_status")
            #print("EmergencyStopState of robot state is : ", emergencyStopState)
            suc, joint_speed , id = send_command(sock, "get_joint_speed")
            #print("Joint Speed of robot state is : ", joint_speed)
            suc, RobotMode , id = send_command(sock, "getRobotMode")
            #print("RobotMode is : ", RobotMode)
            suc, joint_torques , id = send_command(sock, "get_joint_torques")
            #print("joint_torque is : ", joint_torques)
            suc, joint_acc , id = send_command(sock, "get_joint_acc")
            #print("joint_torque is : ", joint_acc)
            suc, SoftVersion , id = send_command(sock, "getSoftVersion")
            #print("Software_version is : ", SoftVersion)
            suc, jointVersion , id = send_command(sock, "getJointVersion", {"axis":0})
            #print("getJointVersion is : ", jointVersion)
            
            
            """
            
            #setting values
            suc, set_servo_status , id= send_command(sock,"set_servo_status",{"status":1})
            print (suc, set_servo_status, id)
            suc, cycle_time, id = send_command(sock, "setSysVarD",{"addr":6,"value":123})
            #print("Cycle_time is: ",cycle_time)
            suc, result , id = send_command(sock, "md_set_tcp", {"point": [10, 0, 0, 30, 0, 0], "tool_num": 1, "unit_type":0})
            print (suc, result , id)
            user_frame=[499.011212,570.517817, 247.082805, -3.141593, -0.000000, -0.773067]
            ret , result , id=send_command(sock,"setUserFrame",{"user_num":0,"user_frame":user_frame,"unit_type":1})
            ret , result , id = send_command(sock, "setCollisionEnable", {"enable": 1})
            if ret :
                print("result =", result )
            else :
                print("err_msg=", result ["message"])
                
            ret , result , id = send_command(sock, "setCollisionSensitivity", {"value": 50})
            if ret :
                print ("result =", result )
            else :
                print("err_msg=", result ["message"])

            
            #security parameter
            
            ret , result , id=send_command(sock,"setAutoRunToolNumber",{"tool_num": 0})
            if ret :
                print (" result = ", result )
            else :
                print ("err_msg = ", result ["message"])
                
            #robot arm and cente of gravity
            suc, result , id = send_command(sock, "cmd_set_payload",{"tool_num":0, "m":5, "cog" :[10, 20,30]})
            
            #robot arm tool center
            suc, result , id = send_command(sock, "cmd_set_tcp", {"point": [10, 0, 0, 30, 0, 0], "tool_num": 1, " unit_type ":0})
            
            #Collision Enable
            suc , result , id = send_command(sock, "setCollisionEnable", {"enable": 1})
            
            #Collision Sensitivity
            suc , result , id = send_command(sock, " setCollisionSensitivity ", {"value": 50})
            
            #User Coordinate System Data 
            suc , result , id=send_command(sock,"setUserFrame",{"user_num":0,"user_frame":user_frame,"unit_type":1})

            # set end state
            suc, result , id=send_command(sock,"checkFlangeButton",{"button_num":0})
        
            # set robot runnig speed
            suc, result , id = send_command(sock, "setSpeed", {"value": 30})
            
            #set IO status
            
            for i in range (0, 20 ,1) :
                # Set output IO status
                suc, result , id=send_command(sock,"setOutput",{"addr":i,"status":1})

            #set virtual io pins
            
            for i in range(528, 800 ,1) :
                # Set virtual output IO status
                suc, result , id=send_command(sock,"setVirtualOutput",{"addr": i ,"status":1})
                
            # Set analog output
            suc, result , id=send_command(sock,"setAnalogOutput",{"addr":0,"value":-10})
            suc, result , id=send_command(sock,"setAnalogOutput",{"addr":1,"value":-3.5})
            suc, result , id=send_command(sock,"setAnalogOutput",{"addr":2,"value":0})
            suc, result , id=send_command(sock,"setAnalogOutput",{"addr":3,"value":0.5})
            suc, result , id=send_command(sock,"setAnalogOutput",{"addr":4,"value":0.5})
            
            for n in range (0, 11 ,1):
                # Set system B variable value
                suc, result , id=send_command(sock,"setSysVarB",{"addr":i,"value":100})


            for n in range (0, 11 ,1):
                # Set system I variable value
                suc, result , id=send_command(sock,"setSysVarI",{"addr":i,"value":100})
                
            for n in range (0, 11 ,1) :
                # Set system D variable value
                suc, result , id=send_command(sock,"setSysVarD",{"addr":i,"value":100})
                
            #set sys variable P
            point = [0, -90, 0, -90, 90, 0]
            ret , result , id=send_command(sock,"setSysVarP",{"addr":0,"pos":point})

            #Set the system V variable value
            suc, result , id = send_command(sock, "setSysVarV", {"addr": 0,"pose":[243.5,-219.4,169.578000,3.139376,-0.002601,0.106804]})
            
            #set the scope of variable of system variable V
            pos = [200, 125.5, -50, 1.57, -1.57, 3.14]
            ret , result , id=send_command(sock,"setSysVarV",{"addr":0,"pos":pos})
            
            # Transparent transmission starting point
            P0 = [0, -90, 0, -90, 90, 0]
            if (conSuc):
                # Initialize transparent transmission service
                suc, result , id=send_command(sock,"transparent_transmission_init",{"lookahead":400,"t" :10, "smoothness":0.1})
                # Set the current transparent transmission target joint point
                suc, result , id=send_command(sock,"tt_set_current_servo_joint",{"targetPos": P0})
                
            
            
            # Set the profinet int output register
            suc, result , id = send_command(sock, "set_profinet_int_output_registers", {"addr": 1, "length": 2, "value": [1,1]})
            
            # Set the profinet float type output register
            suc, result , id = send_command(sock, "set_profinet_float_output_registers", {"addr": 0, "length": 2, "value": [1,1]})
            
            
            # Set the Ethernet/IP int output register
            suc, result , id = send_command(sock, "set_eip_int_output_registers", {"addr": 1, "length": 2, "value": [1,1]})
            
            # Set the profinet float type output register
            suc, result , id = send_command(sock, "set_profinet_float_output_registers", {"addr": 0, "length": 2, "value": [1,1]})

            """
            
            
            if robotState == 3:
                cycle_start_time = time.time()
                print(cycle_start_time,"------------------------")
            elif robotState == 1:
                pass
            elif robotState == 0:  
                if cycle_start_time is not None:
                    print("Cycle start time = ", cycle_start_time)
                    cycle_end_time = time.time()  # Stop recording time
                    CycleTime = cycle_end_time - cycle_start_time
                    print("CycleTime is:", round(CycleTime,2))
                    cycle_start_time = -1
                    
            PowerOnTime = time.time() - ping_start_time
            print("PowerOnTime is :", round(PowerOnTime,2))
            
            if (CycleTime != -1):
                RobotUtilisation = RobotUtilisation+ round((CycleTime/PowerOnTime),2)*100
                print("RobotUtilisation is :",RobotUtilisation,"%")
        
        
            """
            # Establish connection to InfluxDB
            influx_client = influx_connection()
        
            # Create InfluxDB point
            #timestamp = datetime.utcnow().isoformat()
            influx_point = create_influxdb_point(servoStatus, tcp, cycle_Mode, cycle_time,
                    ellapse_time, cycle_count, robotState, emergencyStopState, joint_speed, 
                    RobotMode, joint_torques, joint_acc, SoftVersion, jointVersion)   #Add set_servo_status under Braces

            # Write data to InfluxDB
            try:
                influx_client.write(database="final", record = influx_point)
                print("Data successfully written to InfluxDB")
            except Exception as e:
                print(f"Error writing data to InfluxDB: {e}")
   
        
        """
        if (conSuc == False):
            ping_end_time = time.time()
            print(f"Machine is currently unreachable.")
            if (ping_start_time is not None):
                PowerOnTime = ping_end_time - ping_start_time
                print("PowerOnTime is ", round(PowerOnTime,2))
            if (CycleTime != -1):
                RobotUtilisation = RobotUtilisation+ round((CycleTime/PowerOnTime),2)*100
                print("RobotUtilisation------------------------------------------------",RobotUtilisation,"%")
                cycle_start_time = -1
            else:
                print("Not Now")
            break
            