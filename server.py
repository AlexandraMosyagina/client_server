import socket
import threading
import logging

clients = []

logger = logging.getLogger('server')
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler('chat_log.txt')
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('[%(asctime)s]%(message)s')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


def handling_message(client_socket, client_address):
    username = client_socket.recv(1024).decode()
    print(f'{username} was connected')

    clients.append((username, client_socket))
    for _, socket in clients:
        socket.send(f'{username} enter in this chat'.encode())

    while True:
        message = client_socket.recv(1024).decode()

        if not message:
            break

        formatted_message = f' {username}: {message}'
        logger.info(formatted_message)

        for name, socket in clients:
            if socket != client_socket:
                socket.send(f'{username} says: {message}'.encode())

    clients.remove((username, client_socket))
    for _, socket in clients:
        socket.send(f'{username} leave this chat')
    client_socket.close()


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 1024))
server_socket.listen()

print('The server was launched')

while True:
    client_socket, client_address = server_socket.accept()
    client_thread = threading.Thread(target=handling_message, args=(client_socket, client_address))

    client_thread.start()
