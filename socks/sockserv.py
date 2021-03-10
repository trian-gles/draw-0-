import socket
import select
import pickle
import time
import threading
import os

class Server:
    HEADER_LENGTH = 10
    IP = "127.0.0.1"
    PORT = 8000

    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((Server.IP, Server.PORT))
        self.server_socket.listen()

        self.sockets_list = [self.server_socket]
        self.clients = {}

        self.cards = list(range(42))
        self.mode = "sleep"

    def send_pickle(self, content_dict, send_sock):
        dict_pick = pickle.dumps(content_dict)
        pick_mess = bytes(f"{len(dict_pick):<{Server.HEADER_LENGTH}}", "utf-8") + dict_pick
        send_sock.send(pick_mess)

    def receive_message(self, client_socket):
        try:
            message_header = client_socket.recv(Server.HEADER_LENGTH)

            if not len(message_header):
                return False

            message_length = int(message_header.decode('utf-8').strip())
            return {"header": message_header,
            "data": client_socket.recv(message_length)}
        except:
            return False


    def deal_cards(self):
        print("timer action called")
        threading.Timer(1, self.deal_cards).start()


    def listen(self):
        read_sockets, _, exception_sockets = select.select(self.sockets_list, [], self.sockets_list)

        for notified_socket in read_sockets:
            if notified_socket == self.server_socket:
                client_socket, client_addr = self.server_socket.accept()

                user = self.receive_message(client_socket)
                if user is False:
                    continue

                self.sockets_list.append(client_socket)

                self.clients[client_socket] = user

                print(f"accepted new connection from \
    {client_addr[0]}: {client_addr[1]} username = {user['data'].decode('utf-8')}")

            else:
                message = self.receive_message(notified_socket)

                if message is False:
                    print(f"Closed connection from {self.clients[notified_socket]['data'].decode('utf-8')}")

                    if self.clients[notified_socket]['data'].decode('utf-8') == "debug":
                        quit()

                    self.sockets_list.remove(notified_socket)
                    del self.clients[notified_socket]
                    continue

                user = self.clients[notified_socket]
                data = pickle.loads(message['data'])
                send_to_index = self.sockets_list.index(notified_socket) + 1
                print(f"received message from {user['data'].decode('utf-8')}: {data}")


                if data["method"] == "pass":
                    if send_to_index < len(self.sockets_list):
                        print(f"Passing card {data['id']}")
                        self.send_pickle(data, self.sockets_list[send_to_index])
                    else:
                        print(f"Discarding {data['id']}")
                elif data["method"] == "quit":
                    os._exit(0)
                elif data["method"] == "start":
                    self.mode = "deal"
                    print("Dealing cards")
                    self.deal_cards()


#                for client_socket in self.clients:
#                    if client_socket != notified_socket:
#                        self.send_pickle(pickle.loads(message['data']), user['data'].decode('utf-8'), client_socket)

        for notified_socket in exception_sockets:
            self.sockets_list.remove(notified_socket)
            del self.clients[notified_socket]

if __name__ == "__main__":
    server = Server()
    while True:
        server.listen()
