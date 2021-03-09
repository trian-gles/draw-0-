import socket
import select
import errno
import sys
import pickle

class Client():
    HEADER_LENGTH = 10
    IP = "127.0.0.1"
    PORT = 8000

    def __init__(self, username):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((Client.IP, Client.PORT))
        self.client_socket.setblocking(False)
        self.send_message(username)
        self.hand = []

    def send_message(self, message):
        enc_message = message.encode('utf-8')
        message_header = f"{len(enc_message):<{Client.HEADER_LENGTH}}".encode('utf-8')
        self.client_socket.send(message_header + enc_message)

    def send_pickle(self, msg_dict):
        dict_pick = pickle.dumps(msg_dict)
        pick_mess = bytes(f"{len(dict_pick):<{Client.HEADER_LENGTH}}", "utf-8") + dict_pick
        self.client_socket.send(pick_mess)

    def send_card(self, id):
        msg_dict = {"method": "pass", "id": id}
        self.send_pickle(msg_dict)

    def send_len(self):
        msg_dict = {"method": "send_len", "len": len(self.hand)}
        self.send_pickle(msg_dict)
        print("Responding with hand length")

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
                    return message_dict
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
    while True:
        msg = input(f"{username} : ")
        if msg == "quit":
            client.send_quit()
        elif msg:
            client.send_card(msg)
        received_card = client.listen()
        if received_card:
            print(received_card)
