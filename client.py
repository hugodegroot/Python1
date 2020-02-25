# Python program to implement client side of chat room. 
import socket 
import select
import threading

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def connectSocket(s):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("18.195.107.195", 5378))
    return s

def makeUser(sock):
    username = input("Username: ")
    message = "HELLO-FROM " + username + '\n'
    sock.send(message.encode("utf-8"))
    data = sock.recv(4096)
    if "IN-USE".encode("utf-8") in data:
        return False
    else: 
        print(data)
        return True

def getServerData():
    try:
        BUFF_SIZE = 4096
        data = b''
        while True:
            part = sock.recv(BUFF_SIZE)
            data += part
            # print(data)
            if not data : 
                print("Socket is closed.")
                break
            elif data[-1] == "/n":
                data.split("/n")
            elif len(part) < BUFF_SIZE : 
                print(data.decode("utf-8"))
                data = b''
    except OSError as msg:
        print(msg)

def getUserData():
    try:
        while True:
            val = input("input: ")
            if val == "!quit":
                sock.close()
                break
            if val == "!who":
                message = "WHO\n"
                sock.send(message.encode())
                continue
            if "@" in val:
                val = val.replace("@", "SEND ")
                message = val + "\n"
                sock.send(message.encode())
                continue
            else:
                continue
    except OSError as msg:
        print(msg)

while True:
    sock = connectSocket(sock)
    userMade = makeUser(sock)
    if userMade:
        t1 = threading.Thread(target=getServerData)
        t2 = threading.Thread(target=getUserData)
        t1.start()
        t2.start()
        break
    else:
        data = sock.recv(4096)
        print(data)
        sock.shutdown(1)
        sock.close()
        sock = connectSocket(sock)

t1.join()
t2.join()