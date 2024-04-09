import collections
import struct

# Define a dictionary outside the loop to store data format information
# This dictionary maps human-readable names (keys) to struct format codes (values)

data_format = collections.OrderedDict(
    {
        "MessageSize": "I",
        "TimeStamp": "Q",
        "autorun_cycleMode": "B",
        "machinePos01": "d",
        "machinePos02": "d",
        "machinePos03": "d",
        "machinePos04": "d",
        "machinePos05": "d",
        "machinePos06": "d",
        "machinePos07": "d",
        "torque04": "d",
        "torque05": "d",
        "torque06": "d",
        "torque07": "d",
        "torque08": "d",
        "robotState": "d",
        "servoReady": "i",
        "can_motor_run": "i",
        "motor_speed01": "i",
        "motor_speed02": "i",
        "motor_speed03": "i",
        "machinePos08": "d",
        "machinePose01": "d",
        "machinePose02": "d",
        "machinePose03": "d",
        "machinePose04": "d",
        "machinePose05": "d",
        "machinePose06": "d",
        "machineUserPose01": "d",
        "machineUserPose02": "d",
        "machineUserPose03": "d",
        "machineUserPose04": "d",
        "machineUserPose05": "d",
        "machineUserPose06": "d",
        "torque01": "d",
        "torque02": "d",
        "torque03": "d",
        "motor_speed04": "i",
        "motor_speed05": "i",
        "motor_speed06": "i",
        "motor_speed07": "i",
        "motor_speed08": "i",
        "robotMode": "i",
        "analog_ioInput01": "d",
        "analog_ioInput02": "d",
        "analog_ioInput03": "d",
        "analog_ioOutput01": "d",
        "analog_ioOutput02": "d",
        "analog_ioOutput03": "d",
        "analog_ioOutput04": "d",
        "analog_ioOutput05": "d",
        "digital_ioInput": "Q",
        "digital_ioOutput": "Q",
        "collision": "B",
        "machineFlangePose01": "d",
        "machineFlangePose02": "d",
        "machineFlangePose03": "d",
        "machineFlangePose04": "d",
        "machineFlangePose05": "d",
        "machineFlangePose06": "d",
        "machineUserFlangePose01": "d",
        "machineUserFlangePose02": "d",
        "machineUserFlangePose03": "d",
        "machineUserFlangePose04": "d",
        "machineUserFlangePose05": "d",
        "machineUserFlangePose06": "d",
        "emergencyStopState": "B",
        "tcp_speed": "d",
        "joint_speed01": "d",
        "joint_speed02": "d",
        "joint_speed03": "d",
        "joint_speed04": "d",
        "joint_speed05": "d",
        "joint_speed06": "d",
        "joint_speed07": "d",
        "joint_speed08": "d",
        "tcpacc": "d",
        "jointacc01": "d",
        "jointacc02": "d",
        "jointacc03": "d",
        "jointacc04": "d",
        "jointacc05": "d",
        "jointacc06": "d",
        "jointacc07": "d",
        "jointacc08": "d",
        "joint_temperature01": "d",
        "joint_temperature02": "d",
        "joint_temperature03": "d",
        "joint_temperature04": "d",
        "joint_temperature05": "d",
        "joint_temperature06": "d",
        "joint_torque01": "d",
        "joint_torque02": "d",
        "joint_torque03": "d",
        "joint_torque04": "d",
        "joint_torque05": "d",
        "joint_torque06": "d",
        "extjoint_torques01": "d",
        "extjoint_torques02": "d",
        "extjoint_torques03": "d",
        "extjoint_torques04": "d",
        "extjoint_torques05": "d",
        "extjoint_torques06": "d",
        "exttcpforceintool01": "d",
        "exttcpforceintool02": "d",
        "exttcpforceintool03": "d",
        "exttcpforceintool04": "d",
        "exttcpforceintool05": "d",
        "exttcpforceintool06": "d",
        "dragState": "B",
        "joint_pos": "d",
        "tcp_pos": "d",
        "CurrentCoord": "i",
        "CycleMode": "i",
        "CurrentJobLine": "s",
        "CurrentEncode": "d",
        "ToolNumber": "i",
        "UserNumber": "B",
        "motor_torque": "d",
        "PathPointIndex": "i",
        "teach_switch": "i",
        "set_tcp": "d",
        "UserFrame": "i",
        "CycleMode": "i",
        "UserFrame": "i",
        "TcpPos": "d",
        "Payload": "d",
        "CentreMass": "i",
        "RobotType": "i",
        "DH": "i",
        "CollisionEnable": "i",
        "CollisionSensitivity": "i",
        "remote_sys_password": "I",
        "SafetyParams": "I",
        "CollisionState": "B",
        "Speed": "i",
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
       fmt_size = struct.calcsize(fmt)  # Calculate size of data chunk based on format

       # Slice data into a chunk and remove that chunk from the original data
       data_chunk, data = data[:fmt_size], data[fmt_size:]

       # Unpack the data chunk using the format string and store the value in the dictionary
       unpacked_data[key] = struct.unpack(f"!{fmt}", data_chunk)[0]


def print_data():
    """
    Prints the contents of the unpacked_data dictionary.
    """

    print(unpacked_data)
