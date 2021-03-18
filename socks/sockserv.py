import socket
import select
import pickle
import threading
import os
from random import choice, shuffle
import logging
import datetime




class Server:
    HEADER_LENGTH = 10

    def __init__(self, ip="127.0.0.1", port=8000):
        logging.basicConfig(filename="server.log", level=logging.DEBUG, filemode='w')
        self.print_log(f"Building server on IP {ip}, PORT {port}")
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((ip, port))
        self.server_socket.listen()

        self.sockets_list = [self.server_socket]
        self.clients = {}

        self.cards = list(range(42))
        shuffle(self.cards)
        # The mode will go from "sleep" to "deal" to "pass" to "finish"
        self.mode = "sleep"

    def print_log(self, msg):
        print(msg)
        logging.debug(str(datetime.datetime.now()) + " : " + msg)

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
        user_keys = list(self.clients.keys())
        all_card_four = list(map(lambda user: self.clients[user]['cards'] > 3, user_keys))
        if not all(all_card_four):
            chosen_user = False
            while not chosen_user:
                pot_user = choice(user_keys)
                if self.clients[pot_user]["cards"] < 4:
                    try:
                        self.deal_card_to(pot_user)
                    except ConnectionAbortedError:
                        return
                    chosen_user = True
            threading.Timer(1, self.deal_cards).start()
        else:
            # Finish the deal phase
            self.print_log("Moving to main phase")
            self.pass_cards()

    def deal_card_to(self, user):
        # in the deal phase, sends a card to the selected user
        card_id = self.cards.pop()
        self.print_log(f"Sending card to {self.clients[user]['data'].decode('utf-8')}")
        self.clients[user]["cards"] += 1
        msg_dict = {"method": "deal", "id": card_id}
        self.send_pickle(msg_dict, user)

    def pass_cards(self):
        if len(self.sockets_list) < 2:
            self.print_log("All users have quit, closing server")
            os._exit(0)
        first_user = self.sockets_list[1]
        if len(self.cards) > 0:
            card_id = self.cards.pop()
        else:
            card_id = "null_card"
        msg_dict = {"method": "pass", "id": card_id}
        self.send_pickle(msg_dict, first_user)
        threading.Timer(1, self.pass_cards).start()

    def listen(self):
        read_sockets, _, exception_sockets = select.select(self.sockets_list, [], self.sockets_list)

        for notified_socket in read_sockets:
            if notified_socket == self.server_socket:
                client_socket, client_addr = self.server_socket.accept()

                user = self.receive_message(client_socket)
                if user is False:
                    continue

                self.sockets_list.append(client_socket)
                user["cards"] = 0
                self.clients[client_socket] = user

                self.print_log(f"accepted new connection from \
{client_addr[0]}: {client_addr[1]} username = {user['data'].decode('utf-8')}")


            else:
                message = self.receive_message(notified_socket)

                if message is False:
                    self.print_log(f"Closed connection from {self.clients[notified_socket]['data'].decode('utf-8')}")

                    if self.clients[notified_socket]['data'].decode('utf-8') == "debug":
                        quit()

                    self.sockets_list.remove(notified_socket)
                    del self.clients[notified_socket]
                    continue

                user = self.clients[notified_socket]
                username = user['data'].decode('utf-8')
                msg_dict = pickle.loads(message['data'])
                send_to_index = self.sockets_list.index(notified_socket) + 1
                self.print_log(f"received message from {user['data'].decode('utf-8')}: {msg_dict}")

                if msg_dict["method"] == "pass":
                    if send_to_index < len(self.sockets_list):
                        self.print_log(f"Passing card {msg_dict['id']}")
                        self.send_pickle(msg_dict, self.sockets_list[send_to_index])
                    else:
                        print(f"Discarding {msg_dict['id']}")
                elif msg_dict["method"] == "quit":
                    os._exit(0)
                elif msg_dict["method"] == "start":
                    if self.mode == "sleep":
                        self.mode = "deal"
                        self.print_log(f"User {username} has initiated the piece")
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
