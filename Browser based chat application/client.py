import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
from ttkthemes import ThemedStyle
import emoji

# Network Configuration
HOST_ADDR = '127.0.0.1'
HOST_PORT = 1489

# UI Theme Color Constants
BG_DARK = '#2F3136'
TEXT_LIGHT = "#E5E5EA"
ACCENT_GREEN = '#4CAF50'
PANEL_GRAY = '#ECEFF1'
ACCENT_PINK = '#C51162'

MAIN_FONT = ("Helvetica", 12)
BTN_FONT = ("Helvetica", 10)
DISPLAY_FONT = ("Helvetica", 10)

network_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def append_to_chat(text_data, tag_name=None):
    message_box.config(state=tk.NORMAL)
    message_box.insert(tk.END, f"{text_data}\n", tag_name)
    message_box.config(state=tk.DISABLED)
    message_box.see(tk.END)

def initiate_connection():
    user_handle = username_textbox.get().strip()
    if not user_handle:
        messagebox.showerror("Error", "Username should not be empty")
        return

    try:
        network_client.connect((HOST_ADDR, HOST_PORT))
        print("Successfully connected to server")
        append_to_chat("[CHATBOT] Successfully connected to the server")

        network_client.sendall(user_handle.encode('utf-8'))

        receiver_thread = threading.Thread(
            target=receive_server_messages, 
            args=(network_client,)
        )
        receiver_thread.daemon = True
        receiver_thread.start()

        username_textbox.config(state=tk.DISABLED)
        username_button.config(state=tk.DISABLED)

    except Exception as err:
        messagebox.showerror("Error", f"Unable to connect to server {HOST_ADDR} {HOST_PORT}: {err}")

def transmit_message():
    input_text = message_textbox.get().strip()
    if input_text:
        processed_text = emoji.demojize(input_text)
        network_client.sendall(processed_text.encode('utf-8'))
        append_to_chat(f"You ~ {input_text}", 'user_message')
        message_textbox.delete(0, tk.END)
    else:
        messagebox.showerror("Error", "Message should not be empty")

def attach_file():
    selected_file = filedialog.askopenfilename()
    if selected_file:
        file_msg = f"Uploaded file: {selected_file}"
        append_to_chat(f"You ~ {file_msg}", 'user_message')

def receive_server_messages(sock):
    while True:
        try:
            incoming_bytes = sock.recv(2048)
            if not incoming_bytes:
                break
            
            raw_msg = incoming_bytes.decode('utf-8')
            if '~' in raw_msg:
                sender, content = raw_msg.split('~', 1)
                append_to_chat(f"[{sender}] ~ {content}", 'user_message')
            else:
                append_to_chat(raw_msg)
        except Exception:
            messagebox.showerror("Error", "Message from user should not be empty")
            break

# GUI Setup
app_window = tk.Tk()
app_window.geometry("800x600")
app_window.title('Browser-Based Chat Application')
app_window.resizable(False, False)

gui_style = ThemedStyle(app_window)
gui_style.set_theme("arc")

app_window.configure(bg=BG_DARK)

app_window.grid_rowconfigure(0, weight=1)
app_window.grid_rowconfigure(1, weight=4)
app_window.grid_rowconfigure(2, weight=1)
app_window.grid_columnconfigure(0, weight=1)

# Top Bar (User Setup)
header_frame = tk.Frame(app_window, bg=BG_DARK)
header_frame.grid(row=0, column=0, sticky="ew")

username_label = tk.Label(header_frame, text="Enter Username: ", font=MAIN_FONT, bg=BG_DARK, fg=ACCENT_GREEN)
username_label.pack(side=tk.LEFT, padx=10, pady=10)

username_textbox = tk.Entry(header_frame, font=MAIN_FONT, bg=TEXT_LIGHT, fg="#223377", width=23)
username_textbox.pack(side=tk.LEFT, padx=10, pady=10)

username_button = tk.Button(
    header_frame, font=BTN_FONT, bg=ACCENT_GREEN, fg=TEXT_LIGHT, 
    command=initiate_connection, text="Join", borderwidth=2, 
    highlightbackground='#223377', highlightcolor='#223377', highlightthickness=2
)
username_button.pack(side=tk.LEFT, padx=10, pady=10)

# Middle Area (Chat Display)
chat_frame = tk.Frame(app_window, bg=PANEL_GRAY)
chat_frame.grid(row=1, column=0, sticky="nsew")

message_box = scrolledtext.ScrolledText(chat_frame, font=DISPLAY_FONT, bg=TEXT_LIGHT, fg="#555555", width=67, height=26.5)
message_box.config(state=tk.DISABLED)
message_box.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

message_box.tag_config('user_message', foreground='blue', font=('Helvetica', 10, 'bold'))

# Bottom Bar (Message Controls)
controls_frame = tk.Frame(app_window, bg=PANEL_GRAY)
controls_frame.grid(row=2, column=0, sticky="ew")

message_label = tk.Label(controls_frame, text="Message: ", font=MAIN_FONT, bg=BG_DARK, fg=ACCENT_GREEN)
message_label.pack(side=tk.LEFT, padx=10, pady=10)

message_textbox = tk.Entry(controls_frame, font=MAIN_FONT, bg=TEXT_LIGHT, fg="#556b2f", width=38)
message_textbox.pack(side=tk.LEFT, padx=10, pady=10)

message_button = tk.Button(
    controls_frame, font=BTN_FONT, bg=ACCENT_GREEN, fg=TEXT_LIGHT, 
    command=transmit_message, text="Send", borderwidth=2, 
    highlightbackground='#223377', highlightcolor='#223377', highlightthickness=2
)
message_button.pack(side=tk.LEFT, padx=10, pady=10)

file_button = tk.Button(
    controls_frame, font=BTN_FONT, bg=ACCENT_GREEN, fg=TEXT_LIGHT, 
    command=attach_file, text="Upload", borderwidth=2, 
    highlightbackground='#223377', highlightcolor='#223377', highlightthickness=2
)
file_button.pack(side=tk.LEFT, padx=10, pady=10)

def main():
    app_window.mainloop()

if __name__ == '__main__':
    main()