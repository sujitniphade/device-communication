import customtkinter as ctk
from tkinter import scrolledtext
import tkinter as tk
from Device_Communication_logic import DeviceCommunication

class DeviceCommunicationGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Device Communication")
        self.root.geometry("400x600")  # Initial size of the window

        # Create an instance of DeviceCommunication
        self.device_comm = DeviceCommunication()

        # Set the appearance mode of customtkinter
        ctk.set_appearance_mode("System")  # Modes: "System" (default), "Dark", "Light"
        ctk.set_default_color_theme("custom_theme.json")  # Themes: "blue" (default), "dark-blue", "green"

        # GUI Setup
        self.create_widgets()
        self.update_button_states(False)

    def create_widgets(self):
        # IP and Port Frame
        ip_port_frame = ctk.CTkFrame(self.root)
        ip_port_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky='ew')

        ip_label = ctk.CTkLabel(ip_port_frame, text="IP Address:")
        ip_label.grid(row=0, column=0, padx=10, pady=10, sticky='w')
        self.ip_entry = ctk.CTkEntry(ip_port_frame)
        self.ip_entry.grid(row=0, column=1, padx=10, pady=10, sticky='ew')

        port_label = ctk.CTkLabel(ip_port_frame, text="Port:")
        port_label.grid(row=1, column=0, padx=10, pady=10, sticky='w')
        self.port_entry = ctk.CTkEntry(ip_port_frame)
        self.port_entry.grid(row=1, column=1, padx=10, pady=10, sticky='ew')

        # Command and Checkboxes Frame
        command_frame = ctk.CTkFrame(self.root)
        command_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky='ew')

        self.connect_button = ctk.CTkButton(command_frame, text="Connect", command=self.connect_device)
        self.connect_button.grid(row=0, column=0, padx=10, pady=10, sticky='ew')

        self.disconnect_button = ctk.CTkButton(command_frame, text="Disconnect", command=self.disconnect_device)
        self.disconnect_button.grid(row=0, column=1, padx=10, pady=10, sticky='ew')

        command_label = ctk.CTkLabel(command_frame, text="Command:")
        command_label.grid(row=1, column=0, padx=10, pady=10, sticky='w')
        self.command_entry = ctk.CTkEntry(command_frame, width=250)
        self.command_entry.grid(row=1, column=1, padx=10, pady=10, sticky='ew')

        # CR and LF checkboxes
        self.cr_checkbox_var = tk.IntVar()
        cr_checkbox = ctk.CTkCheckBox(command_frame, text="Send with \\r (CR)", variable=self.cr_checkbox_var)
        cr_checkbox.grid(row=2, column=0, padx=10, pady=10, sticky='w')

        self.lf_checkbox_var = tk.IntVar()
        lf_checkbox = ctk.CTkCheckBox(command_frame, text="Send with \\n (LF)", variable=self.lf_checkbox_var)
        lf_checkbox.grid(row=2, column=1, padx=10, pady=10, sticky='w')

        # Send Button
        send_button = ctk.CTkButton(command_frame, text="Send Command", command=self.send_command)
        send_button.grid(row=3, column=1, padx=10, pady=10, sticky='ew')

        # Output Box and Clear Button Frame
        output_frame = ctk.CTkFrame(self.root)
        output_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky='ew')

        # Output Box (Using tkinter's ScrolledText as customtkinter doesn't have this)
        self.output_box = scrolledtext.ScrolledText(output_frame, height=10, width=50, state=tk.DISABLED, wrap=tk.WORD)
        self.output_box.grid(row=0, column=0, padx=10, pady=10, sticky='ew')
        self.output_box.tag_config('green', foreground='green')

        # Clear Output Button
        clear_button = ctk.CTkButton(output_frame, text="Clear",fg_color="#fff000", command=self.Clear)
        clear_button.grid(row=1, column=0, pady=10, sticky='e')

        # Status Label
        self.status_label = ctk.CTkLabel(self.root, text="Disconnected", text_color="red")
        self.status_label.grid(row=3, column=0, columnspan=2, pady=10)

        # Configure row and column weights for responsiveness
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        ip_port_frame.grid_columnconfigure(1, weight=1)
        command_frame.grid_columnconfigure(1, weight=1)
        output_frame.grid_columnconfigure(0, weight=1)

    def update_button_states(self, is_connected):
        """Update the state of the connect and disconnect buttons."""
        if is_connected:
            self.connect_button.configure(fg_color="green")
            self.disconnect_button.configure(fg_color="#fff000")
        else:
            self.connect_button.configure(fg_color="#fff000")
            self.disconnect_button.configure(fg_color="red")

    def connect_device(self):
        """Connect to the device using the logic class."""
        ip = self.ip_entry.get()
        port = self.port_entry.get()
        self.device_comm.connect_device(ip, port, self.output_box, self.status_label)
        self.update_button_states(True)

    def disconnect_device(self):
        """Disconnect from the device using the logic class."""
        self.device_comm.disconnect_device(self.output_box, self.status_label)
        self.update_button_states(False)

    def send_command(self):
        """Send the command using the logic class."""
        command = self.command_entry.get()
        append_cr = self.cr_checkbox_var.get()
        append_lf = self.lf_checkbox_var.get()
        self.device_comm.send_command(command, append_cr, append_lf, self.output_box)

    def Clear(self):
        """Clear the content of the output box."""
        self.output_box.configure(state='normal')
        self.output_box.delete('1.0', tk.END)
        self.output_box.configure(state='disabled')

if __name__ == "__main__":
    root = ctk.CTk()  # Change to customtkinter root window
    app = DeviceCommunicationGUI(root)
    root.mainloop()
