# Python program to implement client side of chat room. 
import socket 
import select
import threading

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("18.195.107.195", 5378))

def connectSocket():
    sock.connect(("18.195.107.195", 5378))
    return sock

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
    while True:
        data = sock.recv(4096)
        if not data : 
            print("Socket is closed.")
            break
        else : print(data.decode("utf-8"))

def getUserData():
    while True:
        val = input("input: ")
        if val == "!quit": 
            sock.close()
            break
        elif val == "!who":
            message = "WHO\n"
            sock.send(message.encode())
        elif "@" in val:
            val = val.replace("@", "SEND ")
            message = val + "\n"
            sock.send(message.encode())
        else:
            val = input("")

while True:
    userMade = makeUser(sock)
    if userMade:
        t1 = threading.Thread(target=getServerData())
        t2 = threading.Thread(target=getUserData())
        t1.start()
        t2.start()
    else:
        sock.close()
        connectSocket()

t1.join()
t2.join()