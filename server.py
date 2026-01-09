import socket
import threading
import tkinter as tk
from tkinter import filedialog

max_client_connection = 2

server_ip = "10.101.120.217"  # Change this to your desktop's IP address
port = int(input("Enter the port number to listen on: "))  # Input port number from user
ADDR = (server_ip, port)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(ADDR)
server_socket.listen()

print(
    "[WAIT] Multithreaded Server waits for maximum {} clients".format(
        max_client_connection
    )
)

client_list = []


class ClientThread(threading.Thread):
    def _init_(self, client_socket, addr):
        super()._init_()
        self.client_socket = client_socket
        self.addr = addr
        self.nickname = None
        self.authenticated = False

    def run(self):
        try:
            self.client_socket.sendall("Enter your nickname: ".encode())
            self.nickname = self.client_socket.recv(1024).decode().strip()
            print("[INFO] Client connected with nickname:", self.nickname)
            self.broadcast(f"{self.nickname} has joined the chat!")
            while True:
                message = self.client_socket.recv(1024).decode()
                if message:
                    print("[INFO] Message from {}: {}".format(self.nickname, message))
                    if message.startswith("/private"):
                        recipient, msg = message.split(maxsplit=1)[1].split(maxsplit=1)
                        self.send_private_message(recipient, msg)
                    elif message.startswith("/list"):
                        self.send_client_list()
                    elif message.startswith("/disconnect"):
                        self.disconnect()
                        break
                    elif message.startswith("/sendfile"):
                        file_path = message.split(maxsplit=1)[1]
                        self.receive_file(file_path)
                    else:
                        self.broadcast(f"{self.nickname}: {message}")
                else:
                    raise Exception("Client disconnected")
        except Exception as e:
            print("[DISCONNECTED] {}: {}".format(self.nickname, e))
            self.disconnect()

    def send_private_message(self, recipient, message):
        for client in client_list:
            if client.nickname == recipient:
                client.client_socket.sendall(
                    f"[PRIVATE] {self.nickname}: {message}".encode()
                )
                break
        else:
            self.client_socket.sendall("Recipient not found!".encode())

    def send_client_list(self):
        clients = ", ".join(client.nickname for client in client_list)
        self.client_socket.sendall(f"Connected clients: {clients}".encode())

    def broadcast(self, message):
        for client in client_list:
            if client != self:
                try:
                    client.client_socket.sendall(message.encode())
                except Exception as e:
                    print("[ERROR] Broadcasting to {}: {}".format(client.nickname, e))
                    client.disconnect()

    def receive_file(self, file_name):
        try:
            # Receive file size
            file_size = int(self.client_socket.recv(1024).decode().split(":")[1])

            # Create a buffer to store the file data
            file_data = b""

            # Receive file data in chunks
            while len(file_data) < file_size:
                # Receive up to 4096 bytes at a time (adjust buffer size as needed)
                chunk = self.client_socket.recv(4096)
                if not chunk:
                    raise RuntimeError("Socket connection broken")
                file_data += chunk

            # Save the received file data
            self.save_file(file_name, file_data)
            print(f"File '{file_name}' received and saved successfully.")
        except Exception as e:
            print("[ERROR] Receiving file from {}: {}".format(self.nickname, e))

    def save_file(self, file_name, file_data):
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        file_path = filedialog.asksaveasfilename(initialfile=file_name)
        if file_path:
            with open(file_path, "wb") as file:
                file.write(file_data)

    def disconnect(self):
        self.client_socket.sendall("You are now disconnected from the server.".encode())
        self.client_socket.close()
        client_list.remove(self)
        self.broadcast(f"{self.nickname} has left the chat.")


while True:
    try:
        if len(client_list) < max_client_connection:
            client_socket, addr = server_socket.accept()
            print(
                "[CONNECTED] Client with IP : {} & PORT : {}".format(addr[0], addr[1])
            )

            client_thread = ClientThread(client_socket, addr)
            client_thread.start()
            client_list.append(client_thread)

            if len(client_list) == max_client_connection:
                print(
                    "[=] Server has reached maximum connections {}".format(
                        max_client_connection
                    )
                )
    except KeyboardInterrupt:
        break
    except Exception as e:
        print("Error:", e)

# Cleanup
for client_thread in client_list:
    client_thread.client_socket.close()

server_socket.close()
