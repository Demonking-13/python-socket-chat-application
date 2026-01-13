# 📝 Python Socket Chat Application (Client–Server)

A Python-based TCP client–server chat application that enables real-time communication between multiple clients. The project supports public messaging, private chats, client listing, and file transfer using socket programming and multithreading. It is designed as an academic and practical demonstration of computer networking concepts.

---

## 🚀 Features

- Client–server architecture using TCP sockets  
- Multithreaded server to handle multiple clients simultaneously  
- Real-time message broadcasting  
- Private messaging between clients  
- Client list command  
- File transfer support with file dialog  
- Graceful client connection and disconnection handling  

---

## 🛠️ Tech Stack

- **Python 3**
- **Socket Programming (TCP/IP)**
- **Threading**
- **Tkinter** (file dialog support)

---

## 📁 Project Structure

```
python-socket-chat-application/
│
├── server.py     # Multithreaded server application
├── client.py     # Client-side application
├── README.md     # Project documentation
```

---

## 🔧 Configuration

Before running the application, update the server IP address in both `server.py` and `client.py`:

```python
server_ip = "YOUR_SERVER_IP_ADDRESS"
```

Ensure that the server and clients are connected to the same network or have proper network access.

---

## ▶️ Running the Server

```bash
python server.py
```

---

## ▶️ Running the Client

```bash
python client.py
```

---

## 💬 Available Commands

| Command | Description |
|-------|------------|
| `/private <nickname> <message>` | Send a private message |
| `/list` | Display connected clients |
| `/sendfile` | Send a file |
| `/disconnect` | Disconnect from server |

---

## 🎓 Use Cases

- Computer Networks laboratory project  
- Learning TCP socket programming  
- Multithreaded server design  
- Chat system prototype  

---

## 📄 License

MIT License

---

## 👨‍💻 Author

**Devit**  
Aspiring Software Engineer | Networking & Systems Enthusiast
