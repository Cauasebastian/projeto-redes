import socket
import threading

HEADER = 64
PORT = 5051  # Mesma porta que o servidor
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

def receive():
    while True:
        try:
            msg = client.recv(2048).decode(FORMAT)
            if msg:
                print(msg)
        except Exception as e:
            print(f"An error occurred: {e}")
            client.close()
            break

def start_client():
    receive_thread = threading.Thread(target=receive)
    receive_thread.start()

    try:
        while True:
            msg = input()
            if msg == DISCONNECT_MESSAGE:
                send(DISCONNECT_MESSAGE)
                break
            send(msg)
    except KeyboardInterrupt:
        send(DISCONNECT_MESSAGE)
        print("\nDisconnected from server.")
    finally:
        client.close()

start_client()
