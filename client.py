import socket
import threading

username = input('Please, enter your login: ')
password = input('Please, enter your password: ')

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 1024))

client_socket.send(username.encode())
client_socket.send(password.encode())


def receive_messages():
    while True:
        message = client_socket.recv(1024).decode()
        print(message)


client_thread = threading.Thread(target=receive_messages)

client_thread.start()

while True:
    message = input('Enter your message: ')
    client_socket.send(message.encode())
