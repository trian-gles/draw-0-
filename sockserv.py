import socket
import select
import pickle

HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 8000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((IP, PORT))
server_socket.listen()

sockets_list = [server_socket]

clients = {}

def send_pickle(message, user, send_sock):
    content_dict = {'message': message, 'user': user}
    dict_pick = pickle.dumps(content_dict)
    pick_mess = bytes(f"{len(dict_pick):<{HEADER_LENGTH}}", "utf-8") + dict_pick
    send_sock.send(pick_mess)

def receive_message(client_socket):
    try:
        message_header = client_socket.recv(HEADER_LENGTH)

        if not len(message_header):
            return False

        message_length = int(message_header.decode('utf-8').strip())
        return {"header": message_header,
        "data": client_socket.recv(message_length)}
    except:
        return False


while True:
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

    for notified_socket in read_sockets:
        if notified_socket == server_socket:
            client_socket, client_addr = server_socket.accept()

            user = receive_message(client_socket)
            if user is False:
                continue

            sockets_list.append(client_socket)

            clients[client_socket] = user

            print(f"accepted new connection from \
{client_addr[0]}: {client_addr[1]} username = {user['data'].decode('utf-8')}")

        else:
            message = receive_message(notified_socket)

            if message is False:
                print(f"Closed connection from {clients[notified_socket]['data'].decode('utf-8')}")
                sockets_list.remove(notified_socket)
                del clients[notified_socket]
                continue

            user = clients[notified_socket]
            print(f"received message from {user['data'].decode('utf-8')}: {pickle.loads(message['data'])}")
            for client_socket in clients:
                if client_socket != notified_socket:
                    send_pickle(pickle.loads(message['data']), user['data'].decode('utf-8'), client_socket)

    for notified_socket in exception_sockets:
        sockets_list.remove(notified_socket)
        del clients[notified_socket]
