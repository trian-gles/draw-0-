import socket
import select
import errno
import sys
import pickle

HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 8000

my_username = input("Username: ")
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))
client_socket.setblocking(False)

def send_message(message):
    enc_message = message.encode('utf-8')
    message_header = f"{len(enc_message):<{HEADER_LENGTH}}".encode('utf-8')
    client_socket.send(message_header + enc_message)

send_message(my_username)

while True:
    message = input(f"{my_username} : ")

    if message:
        send_message(message)

    try:
        while True:
            # receive things
            pick_header = client_socket.recv(HEADER_LENGTH)
            if not len(pick_header):
                print("connection closed by the server")
                sys.exit()

            pick_length = int(pick_header.decode("utf-8").strip())
            message_dict = pickle.loads(client_socket.recv(pick_length))


            print(message_dict)

    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print("Reading error : " + str(e))
            sys.exit()
        continue

    except Exception as e:
        print("General error : " + str(e))
        sys.exit()
