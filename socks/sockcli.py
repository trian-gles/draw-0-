import socket
import errno
import sys
import pickle


class Client:
    HEADER_LENGTH = 10
    IP = "127.0.0.1"
    PORT = 8000

    def __init__(self, username):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((Client.IP, Client.PORT))
        self.client_socket.setblocking(False)
        self.send_message(username)
        self.hand = []
        self.selected_card = 0

    def send_message(self, message):
        enc_message = message.encode('utf-8')
        message_header = f"{len(enc_message):<{Client.HEADER_LENGTH}}".encode('utf-8')
        self.client_socket.send(message_header + enc_message)

    def send_pickle(self, msg_dict):
        dict_pick = pickle.dumps(msg_dict)
        pick_mess = bytes(f"{len(dict_pick):<{Client.HEADER_LENGTH}}", "utf-8") + dict_pick
        self.client_socket.send(pick_mess)

    def pass_card(self):
        # removes the highlighted card and sends it
        card_id = self.hand.pop(self.selected_card)
        msg_dict = {"method": "pass", "id": card_id}
        self.send_pickle(msg_dict)

    def pass_null(self):
        # passes an empty card informing the next user to pass
        msg_dict = {"method": "pass", "id": "null_card"}
        self.send_pickle(msg_dict)

    def send_len(self):
        # informs the server of the size of the user's hand
        msg_dict = {"method": "send_len", "len": len(self.hand)}
        self.send_pickle(msg_dict)
        print("Responding with hand length")

    def cycle_right(self):
        self.selected_card = (self.selected_card + 1) % len(self.hand)

    def cycle_left(self):
        self.selected_card = (self.selected_card - 1) % len(self.hand)

    def send_start(self):
        msg_dict = {"method": "start"}
        self.send_pickle(msg_dict)

    def send_quit(self):
        msg_dict = {"method": "quit"}
        self.send_pickle(msg_dict)

    def listen(self):
        try:
            while True:
                # receive things
                pick_header = self.client_socket.recv(Client.HEADER_LENGTH)
                if not len(pick_header):
                    print("connection closed by the server")
                    sys.exit()

                pick_length = int(pick_header.decode("utf-8").strip())
                message_dict = pickle.loads(self.client_socket.recv(pick_length))
                if message_dict["method"] == "pass":
                    if message_dict["id"] != "null_card":
                        self.hand.append(message_dict['id'])
                    if len(self.hand) > 0:
                        self.pass_card()
                    print(self.hand)
                    return f"Received card to pass {message_dict['id']}"
                elif message_dict["method"] == "deal":
                    self.hand.append(message_dict['id'])
                    return f"Received card via deal {message_dict['id']}"
                elif message_dict["method"] == "get_len":
                    self.send_len()

        except IOError as e:
            if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                print("Reading error : " + str(e))
                sys.exit()
            return

        except Exception as e:
            print("General error : " + str(e))
            sys.exit()


if __name__ == "__main__":
    username = input("Username : ")
    client = Client(username)
    client.send_start()
    while True:
        received = client.listen()
        if received:
            print(received)
