import socket
import threading
import sys
import tkinter as tk
from tkinter import filedialog

server_ip = "10.101.120.217"  # Change this to your desktop's IP address
port = int(
    input("Enter the port number to connect to: ")
)  # Input port number from user
ADDR = (server_ip, port)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(ADDR)
print("[CONNECTING] Server with IP : {} & PORT : {}".format(ADDR[0], ADDR[1]))

nickname = input("Enter your nickname: ")
client_socket.sendall(nickname.encode())


def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message:
                print("[=] Message from server: {}".format(message))
                if message.startswith("[PRIVATE]"):
                    sender, msg = message.split(":", 1)
                    print(f"[=] Private message from {sender}: {msg}")
            else:
                raise Exception("Server disconnected")
        except Exception as e:
            print("[DISCONNECTED] {}".format(e))
            client_socket.close()
            sys.exit()


def send_messages():
    while True:
        try:
            message = input("Your message: ")
            if message == "/sendfile":
                file_path = select_file()
                if file_path:
                    send_file(file_path)
            else:
                client_socket.sendall(message.encode())
        except Exception as e:
            print("[ERROR] Sending message: {}".format(e))
            client_socket.close()
            sys.exit()


def select_file():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.askopenfilename()  # Open file dialog
    return file_path


def send_file(file_path):
    try:
        with open(file_path, "rb") as file:
            file_data = file.read()
            file_name = file_path.split("/")[-1]  # Extracting file name from the path
            file_size = len(file_data)
            # Send file metadata (name and size) first
            client_socket.sendall(f"{file_name}:{file_size}".encode())
            # Then send file data
            client_socket.sendall(file_data)
            print(f"File '{file_name}' sent successfully.")
    except FileNotFoundError:
        print("File not found!")
    except Exception as e:
        print("[ERROR] Sending file: {}".format(e))


# Start separate threads for sending and receiving messages
receive_thread = threading.Thread(target=receive_messages)
send_thread = threading.Thread(target=send_messages)

receive_thread.start()
send_thread.start()

# Wait for threads to complete (shouldn't happen)
receive_thread.join()
send_thread.join()
