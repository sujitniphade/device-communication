import socket
from tkinter import messagebox

class DeviceCommunication:
    def __init__(self):
        self.sock = None
        self.is_connected = False

    def connect_device(self, ip, port, output_box, status_label):
        """Connect to the device."""
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(5)
            self.sock.connect((ip, int(port)))
            self.is_connected = True
            status_label.configure(text="Connected", text_color="green")
            output_box.configure(state='normal')
            output_box.insert('end', f"Connected to {ip}:{port}\n", 'green')
            output_box.configure(state='disabled')
        except socket.error as e:
            messagebox.showerror("Connection Error", f"Error connecting to {ip}:{port}\n{e}")
            self.is_connected = False

    def disconnect_device(self, output_box, status_label):
        """Disconnect from the device."""
        if self.sock:
            self.sock.close()
            self.sock = None
            self.is_connected = False
            status_label.configure(text="Disconnected", text_color="red")
            output_box.configure(state='normal')
            output_box.insert('end', "Disconnected\n", 'green')
            output_box.configure(state='disabled')

    def send_command(self, command, append_cr, append_lf, output_box):
        """Send a command to the device."""
        if not self.is_connected:
            messagebox.showerror("Error", "Not connected to the device.")
            return

        # Append CR and LF based on checkboxes
        if append_cr:
            command += "\r"
        if append_lf:
            command += "\n"

        try:
            self.sock.sendall(command.encode())
            response = self.sock.recv(1024).decode()
            output_box.configure(state='normal')
            output_box.insert('end', f"Sent: {command.strip()}\nReceived: {response}\n", 'green')
            output_box.configure(state='disabled')
        except socket.error as e:
            messagebox.showerror("Socket Error", f"Error sending command: {e}")
