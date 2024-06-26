import tkinter as tk
import socket
import json
from tkinter import messagebox
from tkinter import ttk

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
        messagebox.showinfo("Success", f"set_servo_status set to: {value}")
    else:
        messagebox.showerror("Error", "Failed to set set_servo_status")

def set_sys_var_d():
    input_str = entry_widgets[1].get()
    addr, value = map(int, input_str.split(";"))
    success, result, _ = send_command(sock, "setSysVarD", {"addr": addr, "value": value})
    if success:
        messagebox.showinfo("Success", f"setSysVarD set to: {value}")
    else:
        messagebox.showerror("Error", "Failed to set setSysVarD")

def cmd_set_tcp():
    input_str = entry_widgets[2].get()

    parts = input_str.split(";")

    point = list(map(float, parts[0].split(",")))
    tool_num = int(parts[1])
    unit_type = int(parts[2])

    success, result, _ = send_command(sock, "cmd_set_tcp", {"point": point, "tool_num": int(tool_num), "unit_type": int(unit_type)})
    if success:
        messagebox.showinfo("Success", f"cmd_set_tcp set to: {input_str}")
    else:
        messagebox.showerror("Error", "Failed to set cmd_set_tcp")

def set_user_frame():
    input_str = entry_widgets[3].get()
    parts = input_str.split(";")

    user_num = int(parts[0])
    user_frame = list(map(float, parts[1].split(",")))
    unit_type = int(parts[2])

    print(f"first:{user_num}, second{user_frame}, third:{unit_type}")
    success, result, _ = send_command(sock, "setUserFrame", {"user_num": user_num, "user_frame": user_frame, "unit_type": unit_type})
    if success:
        messagebox.showinfo("Success", f"setUserFrame set to: {input_str}")
    else:
        messagebox.showerror("Error", "Failed to set setUserFrame")

#collision enable
#collision sensitivity
#setAutoRunToolNumber
def check_flange_button():
    button_num = entry_widgets[4].get()
    success, result, _ = send_command(sock, "checkFlangeButton", {"button_num": int(button_num)})
    if success:
        messagebox.showinfo("Success", f"checkFlangeButton set to: {button_num}")
    else:
        messagebox.showerror("Error", "Failed to set checkFlangeButton")

def set_speed():
    value = entry_widgets[5].get()
    success, result, _ = send_command(sock, "setSpeed", {"value": int(value)})
    if success:
        messagebox.showinfo("Success", f"setSpeed set to: {value}")
    else:
        messagebox.showerror("Error", "Failed to set setSpeed")

def set_output():
    input_str = entry_widgets[6].get()

    parts = input_str.split(";")
    addr = int(parts[0])
    status = int(parts[1])

    success, result, _ = send_command(sock, "setOutput", {"addr": addr, "status": status})
    if success:
        messagebox.showinfo("Success", f"setOutput set to: {input_str}")
    else:
        messagebox.showerror("Error", "Failed to set setOutput")

def set_virtual_output():
    input_str = entry_widgets[7].get()

    parts = input_str.split(";")
    addr = int(parts[0])
    status = int(parts[1])

    success, result, _ = send_command(sock, "setVirtualOutput", {"addr": addr, "status": status})
    if success:
        messagebox.showinfo("Success", f"setVirtualOutput set to: {input_str}")
    else:
        messagebox.showerror("Error", "Failed to set setVirtualOutput")

def set_analog_output():
    input_str = entry_widgets[8].get()

    parts = input_str.split(";")
    addr = int(parts[0])
    value = int(parts[1])

    success, result, _ = send_command(sock, "setAnalogOutput", {"addr": addr, "value": value})
    if success:
        messagebox.showinfo("Success", f"setAnalogOutput set to: {input_str}")
    else:
        messagebox.showerror("Error", "Failed to set setAnalogOutput")

def set_sys_var_b():
    input_str = entry_widgets[9].get()

    parts = input_str.split(";")
    addr = int(parts[0])
    value = int(parts[1])

    success, result, _ = send_command(sock, "setSysVarB", {"addr": addr, "value": value})
    if success:
        messagebox.showinfo("Success", f"setSysVarB set to: {input_str}")
    else:
        messagebox.showerror("Error", "Failed to set setSysVarB")

def set_sys_var_i():
    input_str = entry_widgets[10].get()

    parts = input_str.split(";")
    addr = int(parts[0])
    value = int(parts[1])

    success, result, _ = send_command(sock, "setSysVarI", {"addr": addr, "value": value})
    if success:
        messagebox.showinfo("Success", f"setSysVarI set to: {input_str}")
    else:
        messagebox.showerror("Error", "Failed to set setSysVarI")

def set_sys_var_p():
    input_str = entry_widgets[11].get()

    parts = input_str.split(";")
    addr = int(parts[0])
    point = list(map(float, parts[1].split(",")))
    
    success, result, _ = send_command(sock,"setSysVarP",{"addr":addr,"pos":point})
    if success:
        messagebox.showinfo("Success", f"setSysVarP set to: {input_str}")
    else:
        messagebox.showerror("Error", "Failed to set setSysVarP")

def set_sys_var_v():
    input_str = entry_widgets[12].get()
   
    parts = input_str.split(";")
    addr = int(parts[0])
    pose = list(map(float, parts[1].split(",")))

    success, result, _ = send_command(sock, "setSysVarV", {"addr": int(addr), "pose": pose})
    if success:
        messagebox.showinfo("Success", f"setSysVarV set to: {input_str}")
    else:
        messagebox.showerror("Error", "Failed to set setSysVarV")

def transparent_transmission_init():
    input_str = entry_widgets[13].get()

    parts = input_str.split(";")
    lookahead = int(parts[0])
    t = int(parts[1])
    smoothness = int(parts[2])

    success, result, _ = send_command(sock, "transparent_transmission_init", {"lookahead": lookahead, "t": t, "smoothness": smoothness})
    if success:
        messagebox.showinfo("Success", f"transparent_transmission_init set to: {input_str}")
    else:
        messagebox.showerror("Error", "Failed to set transparent_transmission_init")

def tt_set_current_servo_joint():
    input_str = entry_widgets[14].get()
    
    parts = input_str.split(";")
    targetPos = list(map(float, parts[0].split(",")))

    success, result, _ = send_command(sock, "tt_set_current_servo_joint", {"targetPos": target_pos})
    if success:
        messagebox.showinfo("Success", f"tt_set_current_servo_joint set to: {input_str}")
    else:
        messagebox.showerror("Error", "Failed to set tt_set_current_servo_joint")

def set_profinet_int_output_registers():
    input_str = entry_widgets[15].get()
   
    parts = input_str.split(";")

    address = int(parts[0])
    length = int(parts[1])
    value = list(map(float, parts[2].split(",")))

    success, result, _ = send_command(sock, "set_profinet_int_output_registers", {"addr": int(addr), "length": int(length), "value": value})
    if success:
        messagebox.showinfo("Success", f"set_profinet_int_output_registers set to: {input_str}")
    else:
        messagebox.showerror("Error", "Failed to set set_profinet_int_output_registers")

def set_profinet_float_output_registers():
    input_str = entry_widgets[16].get()
    
    parts = input_str.split(";")

    address = int(parts[0])
    length = int(parts[1])
    value = list(map(float, parts[2].split(",")))

    success, result, _ = send_command(sock, "set_profinet_float_output_registers", {"addr": int(addr), "length": int(length), "value": value})
    if success:
        messagebox.showinfo("Success", f"set_profinet_float_output_registers set to: {input_str}")
    else:
        messagebox.showerror("Error", "Failed to set set_profinet_float_output_registers")

def set_eip_int_output_registers():
    input_str = entry_widgets[17].get()
    
    parts = input_str.split(";")

    address = int(parts[0])
    length = int(parts[1])
    value = list(map(float, parts[2].split(",")))

    success, result, _ = send_command(sock, "set_eip_int_output_registers", {"addr": 1, "length": 2, "value": [1,1]})
    if success:
        messagebox.showinfo("Success", f"set_eip_int_output_registers set to: {input_str}")
    else:
        messagebox.showerror("Error", "Failed to set set_eip_int_output_registers")
        

def move_by_Line() -> None:

    point = []
    point .append([0.0065,-103.9938,102.2076,-88.2138, 90.0000,0.0013])
    point .append([-16.2806,-82.4996,81.9848,-89.4851, 90.0000, -16.2858])
    point .append([3.7679, -71.7544, 68.7276, -86.9732, 90.0000, 3.7627])
    point .append([12.8237,-87.3028,87.2361,-89.9333, 90.0000,12.8185])
    
    for i in range (4):
        # Linear motion
        suc, result , id=send_command(sock,"moveByLine",{"targetPos":point[i],"speed_type" :0, "speed":200,"cond_type":0,"cond_num":7,"cond_value":1})
    if suc:
        messagebox.showinfo("Success", f"Robot moved successfully!")
    else:
        messagebox.showerror("Error", "Failed to move robot")       

def establish_connection():
    global sock
    robot_ip = "192.168.1.200"
    conSuc, sock = connectETController(robot_ip)
    if conSuc:
        messagebox.showinfo("Success", "Connection successful")
    else:
        messagebox.showerror("Error", "Failed to establish connection")


root = tk.Tk()
root.title("Value Setter")
root.attributes("-fullscreen", True)  # Open the window in full-screen mode

# Define dark mode theme
style = ttk.Style()
style.theme_use("clam")  # Choose one of the existing themes to inherit settings from
style.configure("Dark.TLabel", foreground="white", background="black")  # Define label style for dark mode
style.configure("Dark.TEntry", foreground="white", background="gray20", fieldbackground="gray30")  # Define entry field style for dark mode
style.configure("Dark.TButton", foreground="white", background="gray30")  # Define button style for dark mode

# Create a heading label
heading_label = ttk.Label(root, text="SET VALUES TO THE ROBOT", style="Dark.TLabel")
heading_label.config(font=("Helvetica", 36, "bold italic"), foreground="white")  # Customize font, size, weight, and color
heading_label.pack(pady=20)

# Create scrollable frame
main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=True)

canvas = tk.Canvas(main_frame)
canvas.pack(side="left", fill="both", expand=True)

scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
scrollbar.pack(side="right", fill="y")

canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind("<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all")))

scrollable_frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")



# Create labels
labels = [
    "set_servo_status", "setSysVarD", "cmd_set_tcp", "setUserFrame",
    "checkFlangeButton", "setSpeed", "setOutput", "setVirtualOutput",
    "setAnalogOutput", "setSysVarB", "setSysVarI",
    "setSysVarP", "setSysVarV", "transparent_transmission_init",
    "tt_set_current_servo_joint", "set_profinet_int_output_registers",
    "set_profinet_float_output_registers", "set_eip_int_output_registers"
]

label_widgets = []
for label_text in labels:
    label = tk.Label(scrollable_frame, text=label_text, padx=50, pady=15)
    label_widgets.append(label)

# Create text fields
entry_widgets = []
for _ in labels:
    entry = ttk.Entry(scrollable_frame, width=20)
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
    "set_profinet_float_output_registers": set_profinet_float_output_registers,
    "set_eip_int_output_registers": set_eip_int_output_registers
}
for i in range(len(labels)):
    button = ttk.Button(scrollable_frame, text="Set", style="Dark.TButton", command=button_functions.get(labels[i], lambda: print("Function not defined")))
    button_widgets.append(button)

# Layout labels, text fields, buttons, and connect button
half_labels = len(labels) // 2
# Place the widgets for the first half on the left side
for i in range(half_labels):
    label_widgets[i].grid(row=i, column=0, padx=(20,5), pady=5, sticky="e")
    entry_widgets[i].grid(row=i, column=1, padx=5, pady=5, sticky="w")
    button_widgets[i].grid(row=i, column=2, padx=5, pady=5, sticky="w")

# Place the widgets for the second half on the right side
for i in range(half_labels, len(labels)):
    offset = i - half_labels
    label_widgets[i].grid(row=offset, column=3, padx=(20,5), pady=5, sticky="e")
    entry_widgets[i].grid(row=offset, column=4, padx=5, pady=5, sticky="w")
    button_widgets[i].grid(row=offset, column=5, padx=5, pady=5, sticky="w")

# Add the Connect and Move buttons at the bottom
connect_button = ttk.Button(root, text="Connect to the Robot!", style="Dark.TButton", command=establish_connection)
connect_button.pack(side="bottom", padx=10, pady=10)

move_text = ttk.Entry(root, width=40)  
move_text.pack(side="top", padx=40, pady=10)
move_button = ttk.Button(root, text="Move Robot", style="Dark.TButton", command=move_by_Line)
move_button.pack(side="bottom", padx=40, pady=10)

root.resizable(False, False)
root.mainloop()
 