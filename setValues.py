import tkinter as tk
import socket
import json

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



#functions to set values
def set_servo_status():
    value = entry_widgets[0].get()
    success, result, _ = send_command(sock, "set_servo_status", {"status": int(value)})
    if success:
        print("set_servo_status set to:", value)
    else:
        print("Failed to set set_servo_status")

def set_sys_var_d():
    input_str = entry_widgets[1].get()
    addr, value = map(int, input_str.split(","))
    success, result, _ = send_command(sock, "setSysVarD", {"addr": addr, "value": value})
    if success:
        print("setSysVarD set to:", value)
    else:
        print("Failed to set setSysVarD")

def cmd_set_tcp():
    input_str = entry_widgets[2].get()
    point, tool_num, unit_type = eval(input_str)  # Using eval to parse the list
    success, result, _ = send_command(sock, "cmd_set_tcp", {"point": point, "tool_num": int(tool_num), "unit_type": int(unit_type)})
    if success:
        print("cmd_set_tcp set to:", input_str)
    else:
        print("Failed to set cmd_set_tcp")

def set_user_frame():
    input_str = entry_widgets[3].get()
    user_num, user_frame, unit_type = map(int, input_str.split(","))
    success, result, _ = send_command(sock, "setUserFrame", {"user_num": user_num, "user_frame": user_frame, "unit_type": unit_type})
    if success:
        print("setUserFrame set to:", input_str)
    else:
        print("Failed to set setUserFrame")

def check_flange_button():
    button_num = entry_widgets[4].get()
    success, result, _ = send_command(sock, "checkFlangeButton", {"button_num": int(button_num)})
    if success:
        print("checkFlangeButton set to:", button_num)
    else:
        print("Failed to set checkFlangeButton")

def set_speed():
    value = entry_widgets[5].get()
    success, result, _ = send_command(sock, "setSpeed", {"value": int(value)})
    if success:
        print("setSpeed set to:", value)
    else:
        print("Failed to set setSpeed")

def set_output():
    input_str = entry_widgets[6].get()
    addr, status = map(int, input_str.split(","))
    success, result, _ = send_command(sock, "setOutput", {"addr": addr, "status": status})
    if success:
        print("setOutput set to:", input_str)
    else:
        print("Failed to set setOutput")

def set_virtual_output():
    input_str = entry_widgets[7].get()
    addr, status = map(int, input_str.split(","))
    success, result, _ = send_command(sock, "setVirtualOutput", {"addr": addr, "status": status})
    if success:
        print("setVirtualOutput set to:", input_str)
    else:
        print("Failed to set setVirtualOutput")

def set_analog_output():
    input_str = entry_widgets[8].get()
    addr, value = map(int, input_str.split(","))
    success, result, _ = send_command(sock, "setAnalogOutput", {"addr": addr, "value": value})
    if success:
        print("setAnalogOutput set to:", input_str)
    else:
        print("Failed to set setAnalogOutput")

def set_sys_var_b():
    input_str = entry_widgets[9].get()
    addr, value = map(int, input_str.split(","))
    success, result, _ = send_command(sock, "setSysVarB", {"addr": addr, "value": value})
    if success:
        print("setSysVarB set to:", input_str)
    else:
        print("Failed to set setSysVarB")

def set_sys_var_i():
    input_str = entry_widgets[10].get()
    addr, value = map(int, input_str.split(","))
    success, result, _ = send_command(sock, "setSysVarI", {"addr": addr, "value": value})
    if success:
        print("setSysVarI set to:", input_str)
    else:
        print("Failed to set setSysVarI")


def set_sys_var_p():
    input_str = entry_widgets[12].get()
    addr = int(input_str)
    success, result, _ = send_command(sock, "setSysVarP", {"addr": addr})
    if success:
        print("setSysVarP set to:", input_str)
    else:
        print("Failed to set setSysVarP")

def set_sys_var_v():
    input_str = entry_widgets[13].get()
    addr, pose = input_str.split(",")
    pose = list(map(float, pose.split()))
    success, result, _ = send_command(sock, "setSysVarV", {"addr": int(addr), "pose": pose})
    if success:
        print("setSysVarV set to:", input_str)
    else:
        print("Failed to set setSysVarV")

def transparent_transmission_init():
    input_str = entry_widgets[14].get()
    lookahead, t, smoothness = map(float, input_str.split(","))
    success, result, _ = send_command(sock, "transparent_transmission_init", {"lookahead": lookahead, "t": t, "smoothness": smoothness})
    if success:
        print("transparent_transmission_init set to:", input_str)
    else:
        print("Failed to set transparent_transmission_init")

def tt_set_current_servo_joint():
    input_str = entry_widgets[15].get()
    target_pos = list(map(float, input_str.split(",")))
    success, result, _ = send_command(sock, "tt_set_current_servo_joint", {"targetPos": target_pos})
    if success:
        print("tt_set_current_servo_joint set to:", input_str)
    else:
        print("Failed to set tt_set_current_servo_joint")

def set_profinet_int_output_registers():
    input_str = entry_widgets[16].get()
    addr, length, value = input_str.split(",")
    value = list(map(int, value.split()))
    success, result, _ = send_command(sock, "set_profinet_int_output_registers", {"addr": int(addr), "length": int(length), "value": value})
    if success:
        print("set_profinet_int_output_registers set to:", input_str)
    else:
        print("Failed to set set_profinet_int_output_registers")

def set_profinet_float_output_registers():
    input_str = entry_widgets[17].get()
    addr, length, value = input_str.split(",")
    value = list(map(float, value.split()))
    success, result, _ = send_command(sock, "set_profinet_float_output_registers", {"addr": int(addr), "length": int(length), "value": value})
    if success:
        print("set_profinet_float_output_registers set to:", input_str)
    else:
        print("Failed to set set_profinet_float_output_registers")


def establish_connection():
    global sock
    robot_ip = "192.168.1.200"
    conSuc, sock = connectETController(robot_ip)
    if conSuc:
        print("Connection successful")
    else:
        print("Failed to establish connection")


root = tk.Tk()
root.title("Value Setter")

# Create labels
labels = [
    "set_servo_status", "setSysVarD", "cmd_set_tcp", "setUserFrame",
    "checkFlangeButton", "setSpeed", "setOutput", "setVirtualOutput",
    "setAnalogOutput", "setSysVarB", "setSysVarI", "setSysVarD",
    "setSysVarP", "setSysVarV", "transparent_transmission_init",
    "tt_set_current_servo_joint", "set_profinet_int_output_registers",
    "set_profinet_float_output_registers"
]

label_widgets = []
for label_text in labels:
    label = tk.Label(root, text=label_text)
    label_widgets.append(label)

# Create text fields
entry_widgets = []
for _ in labels:
    entry = tk.Entry(root)
    entry_widgets.append(entry)

# Create buttons
button_widgets = []
button_functions = {
    "set_servo_status": set_servo_status,
    "setSysVarD": set_sys_var_d,
    "cmd_set_tcp": cmd_set_tcp,
    "setUserFrame": set_user_frame,
    "checkFlangeButton": check_flange_button,
    "setSpeed": set_speed,
    "setOutput": set_output,
    "setVirtualOutput": set_virtual_output,
    "setAnalogOutput": set_analog_output,
    "setSysVarB": set_sys_var_b,
    "setSysVarI": set_sys_var_i,
    "setSysVarP": set_sys_var_p,
    "setSysVarV": set_sys_var_v,
    "transparent_transmission_init": transparent_transmission_init,
    "tt_set_current_servo_joint": tt_set_current_servo_joint,
    "set_profinet_int_output_registers": set_profinet_int_output_registers,
    "set_profinet_float_output_registers": set_profinet_float_output_registers
}
for i in range(len(labels)):
    button = tk.Button(root, text="Set", command=button_functions.get(labels[i], lambda: print("Function not defined")))
    button_widgets.append(button)

# Add button to establish connection
connect_button = tk.Button(root, text="Connect to the Robot!", command=establish_connection)
connect_button.grid(row=len(labels), column=1, columnspan=2, padx=5, pady=5)


# Layout labels, text fields, and buttons
for i in range(len(labels)):
    label_widgets[i].grid(row=i, column=0, padx=5, pady=5)
    entry_widgets[i].grid(row=i, column=1, padx=5, pady=5)
    button_widgets[i].grid(row=i, column=2, padx=5, pady=5)

root.mainloop()
