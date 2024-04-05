#!/usr/bin/python
# -*- coding:UTF-8 -*-
#EC_CommunicationProtocolManual_Ver3.8.2.pdf

import modbus_tk.modbus_tcp as mt
import modbus_tk.defines as md
from time import *

def getShortValue(value):
    '''
    The state value value is short type
    param value: unsigned int type
    return: 16-bit signed short type
    '''
    if value >= pow(2, 15):
        return (~(value - 1) & (pow(2, 16) - 1)) * -1
    else:
        return value

# Create ModbusTCP connection
master = mt.TcpMaster("192.168.1.200", 502)   #192.168.1.200
master.set_timeout(5.0)

joint_value = []  # Used to save the robot joint angle information
joint_speed_value = []  # Used to save the robot joint speed information
tcp_value = []  # Used to save TCP pose information of the robot
tcp_speed_value = []  # Used to save the robot TCP speed information
input_value = []  # Used to save the robot digital input port information
output_value = []  # Used to save the robot digital output port information
ainput_value = []  # Used to save robot analog input port information
aoutput_value = []  # Used to save robot analog output port information
safety_params_enable_value = []  # Used to save robot safety parameter enabling information
collision_enable_value = []  # Used to save the robot collision detection enabling information
timestamp_value = []  # Used to save robot system timestamp information

while True:
    # Read R200, R210, R220, R228, R229, R230, R240, R250, R260, R270, R280 register data respectively
    hold_joint = master.execute(1, md.READ_HOLDING_REGISTERS, 200, 8)
    hold_joint_speed = master.execute(1, md.READ_HOLDING_REGISTERS, 210, 8)
    hold_tcp = master.execute(1, md.READ_HOLDING_REGISTERS, 220, 6)
    hold_safety_params_enable_status = master.execute(1, md.READ_HOLDING_REGISTERS, 228, 1)
    hold_collision_enable_status = master.execute(1, md.READ_HOLDING_REGISTERS, 229, 1)
    hold_tcp_speed = master.execute(1, md.READ_HOLDING_REGISTERS, 230, 1)
    hold_input = master.execute(1, md.READ_HOLDING_REGISTERS, 240, 3)
    hold_output = master.execute(1, md.READ_HOLDING_REGISTERS, 250, 2)
    hold_ainput = master.execute(1, md.READ_HOLDING_REGISTERS, 260, 3)
    hold_aoutput = master.execute(1, md.READ_HOLDING_REGISTERS, 270, 5)
    hold_timestamp = master.execute(1, md.READ_HOLDING_REGISTERS, 280, 4)

    # Change the data unit and save it in the list
    for joint in hold_joint:
        joint_value.append(getShortValue(joint) / 5000.0 * 180 / 3.14)
    for speed in hold_joint_speed:
        joint_speed_value.append(getShortValue(speed) * 180 / 3.14 / 1000.0)
    for tcp in hold_tcp:
        if hold_tcp.index(tcp) < 3:
            tcp_value.append(getShortValue(tcp) / 10.0)
        else:
            tcp_value.append(getShortValue(tcp) / 5000.0 * 180 / 3.14)
    for status in hold_safety_params_enable_status:
        safety_params_enable_value.append(getShortValue(status))
    for status in hold_collision_enable_status:
        collision_enable_value.append(getShortValue(status))
    for speed in hold_tcp_speed:
        tcp_speed_value.append(getShortValue(speed) / 10.0)
    for input in hold_input:
        input_value.append(input)
    for output in hold_output:
        output_value.append(output)
    for ainput in hold_ainput:
        ainput_value.append(getShortValue(ainput) / 1000.0)
    for aoutput in hold_aoutput:
        aoutput_value.append(getShortValue(aoutput) / 1000.0)
    for timestamp in hold_timestamp:
        timestamp_value.append(timestamp)

    # Print a list of robot related data
    print("joint_value =", joint_value)
    print("joint_speed_value =", joint_speed_value)
    print("tcp_value =", tcp_value)
    print("safety_params_enable_status =", safety_params_enable_value)
    print("collision_enable_status =", collision_enable_value)
    print("tcp_speed_value =", tcp_speed_value)
    print("input_value =", input_value)
    print("output_value =", output_value)
    print("ainput_value =", ainput_value)
    print("aoutput_value =", aoutput_value)

    print(timestamp_value[0], timestamp_value[1], timestamp_value[2], timestamp_value[3])
    Time_stamp = (timestamp_value[0] + (timestamp_value[1] << 16) + (timestamp_value[2] << 32) + (
                timestamp_value[3] << 48))
    print(Time_stamp)
    
    """
    timeValue = time.gmtime((timestamp_value[0] + (timestamp_value[1] << 16) + (timestamp_value[2] << 32) + (
                timestamp_value[3] << 48)) / 1000)
    print(timeValue)
    
    print(time.strftime("%Y-%m-%d %H:%M:%S", timeValue))
"""
    # Clear lists
    joint_value.clear()
    safety_params_enable_value.clear()
    collision_enable_value.clear()
    joint_speed_value.clear()
    tcp_value.clear()
    tcp_speed_value.clear()
    input_value.clear()
    output_value.clear()
    ainput_value.clear()
    aoutput_value.clear()
    timestamp_value.clear()

    # Get once in 1 second
    sleep(1)