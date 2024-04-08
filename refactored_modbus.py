import modbus_tk.modbus_tcp as mt
import modbus_tk.defines as md
from time import sleep
from influxdb_client_3 import InfluxDBClient3, Point
from datetime import datetime
from influx import influx_connection

def getShortValue(value):
    """
    Converts an unsigned integer value to a 16-bit signed short value.

    Args:
        value (int): The unsigned integer value to convert.

    Returns:
        int: The converted 16-bit signed short value.
    """
    if value >= pow(2, 15):
        return (~(value - 1) & (pow(2, 16) - 1)) * -1
    else:
        return value


def establish_connection(ip, port):
    """
    Establishes a Modbus TCP connection to the robot controller with the specified IP and port.

    Args:
        ip (str): The IP address of the robot controller.
        port (int): The port number to use for the Modbus TCP connection.

    Returns:
        modbus_tk.modbus_tcp.TcpMaster: The created Modbus TCP master object representing the connection.
    """

    master = mt.TcpMaster(ip, port)
    master.set_timeout(5.0)
    return master

def read_registers(master, address, num_registers):
    """
    Reads data from a set of holding registers on the robot controller using the provided Modbus TCP master.

    Args:
        master (modbus_tk.modbus_tcp.TcpMaster): The Modbus TCP master object representing the connection.
        address (int): The starting address of the holding registers to read.
        num_registers (int): The number of holding registers to read.

    Returns:
        list: A list containing the read data values.
    """

    return master.execute(1, md.READ_HOLDING_REGISTERS, address, num_registers)

def convert_data(data_list):
    """
    Converts a list of data values using the `getShortValue` function for each element.

    Args:
        data_list (list): The list of data values to convert.

    Returns:
        list: A new list containing the converted data values.
    """

    converted_data = []
    for data in data_list:
        converted_data.append(getShortValue(data))
    return converted_data

def print_data(*data_lists):
    """
    Prints the contents of multiple data lists provided as arguments, each on a separate line.

    Args:
        *data_lists (list): A variable number of data lists to print.
    """

    for data_list in data_lists:
        print(data_list)

def get_timestamp(timestamp_values):
    """
    Combines four separate timestamp values into a single integer value.

    Args:
        timestamp_values (list): A list containing four individual timestamp values.

    Returns:
        int: The combined timestamp integer.
    """
    Time_stamp = timestamp_values[0] + (timestamp_values[1] << 16) + (timestamp_values[2] << 32) + (timestamp_values[3] << 48)
    return Time_stamp

def clear_lists(*lists):
    """
    Clears all lists provided as arguments.

    Args:
        *lists (list): A variable number of lists to clear.
    """

    for l in lists:
        l.clear()


def create_influxdb_point(timestamp, joint_values, joint_speed_values, tcp_values):
    point = Point("robot_data") \
        .tag("robot_id", "robot_1") \
        .field("timestamp", timestamp) \
        .field("joint_value_1", joint_values[0]) \
        .field("joint_value_2", joint_values[1]) \
        .field("joint_value_3", joint_values[2]) \
        .field("joint_value_4", joint_values[3]) \
        .field("joint_value_5", joint_values[4]) \
        .field("joint_value_6", joint_values[5]) \
        .field("joint_value_7", joint_values[6]) \
        .field("joint_value_8", joint_values[7]) \
        .field("joint_speed_1", joint_speed_values[0]) \
        .field("joint_speed_2", joint_speed_values[1]) \
        .field("joint_speed_3", joint_speed_values[2]) \
        .field("joint_speed_4", joint_speed_values[3]) \
        .field("joint_speed_5", joint_speed_values[4]) \
        .field("joint_speed_6", joint_speed_values[5]) \
        .field("joint_speed_7", joint_speed_values[6]) \
        .field("joint_speed_8", joint_speed_values[7]) \
        .field("tcp_x", tcp_values[0]) \
        .field("tcp_y", tcp_values[1]) \
        .field("tcp_z", tcp_values[2]) \
        .field("tcp_rx", tcp_values[3]) \
        .field("tcp_ry", tcp_values[4]) \
        .field("tcp_rz", tcp_values[5])

    return point


def main():
    """
    The main function that establishes a connection, reads data from the robot controller in a loop,
    processes and prints the data, and then clears the temporary data lists.
    """

    master = establish_connection("192.168.1.200", 502)

    # Establish connection to InfluxDB
    influx_client = influx_connection()

    while True:
        hold_joint = read_registers(master, 200, 8)
        hold_joint_speed = read_registers(master, 210, 8)
        hold_tcp = read_registers(master, 220, 6)
        hold_safety_params_enable_status = read_registers(master, 228, 1)
        hold_collision_enable_status = read_registers(master, 229, 1)
        hold_tcp_speed = read_registers(master, 230, 1)
        hold_input = read_registers(master, 240, 3)
        hold_output = read_registers(master, 250, 2)
        hold_ainput = read_registers(master, 260, 3)
        hold_aoutput = read_registers(master, 270, 5)
        hold_timestamp = read_registers(master, 280, 4)

        joint_value = convert_data(hold_joint)
        joint_speed_value = convert_data(hold_joint_speed)
        tcp_value = convert_data(hold_tcp)
        safety_params_enable_value = convert_data(hold_safety_params_enable_status)
        collision_enable_value = convert_data(hold_collision_enable_status)
        tcp_speed_value = convert_data(hold_tcp_speed)
        input_value = convert_data(hold_input)
        output_value = convert_data(hold_output)
        ainput_value = convert_data(hold_ainput)
        aoutput_value = convert_data(hold_aoutput)
        timestamp_value = convert_data(hold_timestamp)

        print_data(joint_value, joint_speed_value, tcp_value, safety_params_enable_value, collision_enable_value,
                   tcp_speed_value, input_value, output_value, ainput_value, aoutput_value)

        Time_stamp = get_timestamp(timestamp_value)
        print(Time_stamp)


        # Create InfluxDB point
        timestamp = datetime.utcnow().isoformat()
        influx_point = create_influxdb_point(timestamp, joint_value, joint_speed_value, tcp_value)

        # Write data to InfluxDB
        try:
            influx_client.write(influx_point)
            print("Data successfully written to InfluxDB")
        except Exception as e:
            print(f"Error writing data to InfluxDB: {e}")

        clear_lists(joint_value, joint_speed_value, tcp_value, safety_params_enable_value, collision_enable_value,
                    tcp_speed_value, input_value, output_value, ainput_value, aoutput_value, timestamp_value)

        sleep(1)

if __name__ == "__main__":
    main()