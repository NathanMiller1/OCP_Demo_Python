"""
OMNIA Control Protocol Real-Time Demo

This Python script demonstrates real-time communication with OMNIA using the OMNIA Control Protocol (OCP).
It includes a graphical user interface (GUI) built with tkinter, allowing users to enable real-time information,
receive and parse XML messages from OMNIA, and update relevant text boxes with extracted data.

Dependencies:
    - tkinter: Python's standard GUI library
    - socket: Provides low-level networking interface
    - threading: Supports multithreading for handling concurrent tasks
    - xml.etree.ElementTree: Facilitates parsing XML messages

This script is open-source and available under the MIT License. Feel free to modify and distribute it according to
the terms of the license.

Author: Nathan Miller
Created: February 17, 2024
License: MIT License
"""


import tkinter as tk
import socket
import threading
import xml.etree.ElementTree as ET


def parse_xml(xml_bytes):
    """
    Parse XML byte messages from OMNIA and update relevant tkinter text boxes.

    This function specifically handles <SetRealTimeInfo> messages and extracts
    relevant information such as Timestamp, VO2, VCO2, Phase, VE, and HR.

    Args:
        xml_bytes (bytes): Bytes containing the XML message from OMNIA.

    Returns:
        None
    """

    # Parse the XML string into an ElementTree root element
    et_root = ET.fromstring(xml_bytes)

    # Find the first occurrence of the <SetRealTimeInfo> element in the XML structure
    set_real_time_info = et_root.find(".//SetRealTimeInfo")

    # If <SetRealTimeInfo> was found
    if set_real_time_info is not None:
        # Timestamp
        timestamp = set_real_time_info.findtext("TimeStamp")
        tb_time.delete('1.0', tk.END)
        tb_time.insert('1.0', timestamp)

        # VO2
        vo2 = set_real_time_info.findtext("VO2")
        tb_vo2.delete('1.0', tk.END)
        tb_vo2.insert('1.0', round(float(vo2), 1))

        # VCO2
        vco2 = set_real_time_info.findtext("VCO2")
        tb_vco2.delete('1.0', tk.END)
        tb_vco2.insert('1.0', round(float(vco2), 1))

        # Phase
        phase = set_real_time_info.findtext("PHASE")
        tb_phase.delete('1.0', tk.END)
        tb_phase.insert('1.0', phase)

        # VE
        ve = set_real_time_info.findtext("VE")
        tb_ve.delete('1.0', tk.END)
        tb_ve.insert('1.0', round(float(ve), 1))

        # HR
        hr = set_real_time_info.findtext("HR")
        tb_hr.delete('1.0', tk.END)
        tb_hr.insert('1.0', hr)
                
    
def enable_click():
    """
    Event handler for the enable button.

    Disables the button, retrieves the IP address and port from the entry widgets,
    creates a message to enable OMNIA Real-Time Information, sends the message to the specified
    IP address and port, and updates the status text box with the OMNIA server's response.
    Additionally, continuously receives and parses XML data from the server.

    Args:
        None

    Returns:
        None
    """
    # Disable the button to prevent multiple clicks
    button_enable["state"] = "disabled"

    # Get the IP address and port from entry widgets
    ip_address = str(eb_ip.get())
    port = int(eb_port.get())

    # Create the message to enable OMNIA Real-Time Information
    message = r'<OmniaXB><System><EnableRealTimeInformation><Enabled>1</Enabled></EnableRealTimeInformation></System></OmniaXB>'

    # Encode the message in bytes (UTF-8)
    byte_message = message.encode('utf-8')

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            # Connect to the specified IP address and port
            s.connect((ip_address, port))

            # Send the enable OMNIA Real-Time Information message to OMNIA
            s.sendall(byte_message)

            # Receive and display the OMNIA server's response
            omnia_reply = s.recv(1024)
            tb_status.delete('1.0', tk.END)
            tb_status.insert('1.0', omnia_reply.decode('utf-8'))

            # Continuously receive and parse XML data from the server
            while True:
                data = s.recv(1024)
                parse_xml(data)

        except Exception as e:
            # Display any exception in the status text box
            tb_status.delete('1.0', tk.END)
            tb_status.insert('1.0', e)


#Window Size Constants
xSpacing = 5
ySpacing = 5

#create GUI root
root = tk.Tk(className=' OMNIA Control Protocol Real-Time Demo')

# SETUP label
label_ip_port = tk.Label(root, text="SETUP")

# IP address label and entry box
label_IP = tk.Label(root, text="IP Address:")
eb_ip = tk.Entry(root)
eb_ip.insert(0, '127.0.0.1')

# Port label and entry box
label_port = tk.Label(root, text="Port:")
eb_port = tk.Entry(root)
eb_port.insert(0, '1234')

# Enable real-time button
# Starts a new daemon thread which handles messages and automatically terminates when the program exits
button_enable = tk.Button(root, 
                          text='Enable Real-Time Information', 
                          command=threading.Thread(target=enable_click, daemon=True).start)

label_col2_spacer = tk.Label(root, text="               ")
label_col3_spacer = tk.Label(root, text="               ")
label_blank1 = tk.Label(root, text=" ")
label_blank2 = tk.Label(root, text=" ")

# Status text box
tb_status = tk.Text(root, height=8, bg='white', borderwidth=2, relief='ridge')
tb_status.insert('1.0', 'Real-time information not enabled')

# REAL-TIME DATA label
label_RTD = tk.Label(root, text="REAL-TIME DATA")

# TimeStamp label and text box
label_time = tk.Label(root, text="Time:")
tb_time = tk.Text(root, height=1, width=29)

# VO2 label and text box
label_vo2 = tk.Label(root, text="VO2:")
tb_vo2 = tk.Text(root, height=1, width=10)

# VCO2 label and text box
label_vco2 = tk.Label(root, text="VCO2:")
tb_vco2 = tk.Text(root, height=1, width=10)

# Phase label and text box
label_phase = tk.Label(root, text="Phase:")
tb_phase = tk.Text(root, height=1, width=10)

# VE label and text box
label_ve = tk.Label(root, text="VE:")
tb_ve =tk.Text(root, height=1, width=10)

# HR label and text box
label_hr = tk.Label(root, text="HR:")
tb_hr = tk.Text(root, height=1, width=10)


##############################################################################
# Arrange grid begin
##############################################################################
label_col2_spacer.grid(row=0, column=2, sticky=tk.W, padx=xSpacing, pady=ySpacing) 
label_col3_spacer.grid(row=0, column=3, sticky=tk.W, padx=xSpacing, pady=ySpacing) 

# Setup
label_ip_port.grid(row=0, column=0, sticky=tk.W, padx=xSpacing, pady=ySpacing)
label_IP     .grid(row=1, column=0, sticky=tk.E, padx=xSpacing, pady=ySpacing)
eb_ip        .grid(row=1, column=1, sticky=tk.W, padx=xSpacing, pady=ySpacing)
label_port   .grid(row=2, column=0, sticky=tk.E, padx=xSpacing, pady=ySpacing)
eb_port      .grid(row=2, column=1, sticky=tk.W, padx=xSpacing, pady=ySpacing)
label_blank1 .grid(row=3, column=0, sticky=tk.W, padx=xSpacing, pady=ySpacing)

# Enable real-time
button_enable.grid(row=4, column=0, sticky=tk.W, padx=xSpacing, pady=ySpacing, columnspan=2)
tb_status    .grid(row=5, column=0, sticky=tk.W, padx=xSpacing, pady=ySpacing, columnspan=4)
label_blank2 .grid(row=6, column=0, sticky=tk.W, padx=xSpacing, pady=ySpacing)

# Real-time data
label_RTD    .grid(row=7, column=0, sticky=tk.W, padx=xSpacing, pady=ySpacing)
label_time   .grid(row=8, column=0, sticky=tk.E, padx=xSpacing, pady=ySpacing)
tb_time      .grid(row=8, column=1, sticky=tk.W, padx=xSpacing, pady=ySpacing)
label_phase  .grid(row=8, column=2, sticky=tk.E, padx=xSpacing, pady=ySpacing)
tb_phase     .grid(row=8, column=3, sticky=tk.W, padx=xSpacing, pady=ySpacing)
label_vo2    .grid(row=9, column=0, sticky=tk.E, padx=xSpacing, pady=ySpacing)
tb_vo2       .grid(row=9, column=1, sticky=tk.W, padx=xSpacing, pady=ySpacing)
label_ve     .grid(row=9, column=2, sticky=tk.E, padx=xSpacing, pady=ySpacing)
tb_ve        .grid(row=9, column=3, sticky=tk.W, padx=xSpacing, pady=ySpacing)
label_vco2   .grid(row=10, column=0, sticky=tk.E, padx=xSpacing, pady=ySpacing)
tb_vco2      .grid(row=10, column=1, sticky=tk.W, padx=xSpacing, pady=ySpacing)
label_hr     .grid(row=10, column=2, sticky=tk.E, padx=xSpacing, pady=ySpacing)
tb_hr        .grid(row=10, column=3, sticky=tk.W, padx=xSpacing, pady=ySpacing)

##############################################################################
# Arrange grid end
##############################################################################
                       
                           
if __name__ == "__main__":
    # Start main loop and show GUI
    root.mainloop() 
    