# Python program to implement client side of chat room. 
import socket 
import select 
import sys 
import threading
import random

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

if len(sys.argv) != 3: 
    print("Correct usage: script, IP address, port number")
    exit() 

IP_address = str(sys.argv[1]) 
Port = int(sys.argv[2]) 
s.connect((IP_address, Port))

def getData():
    while True:
        try:
            data = s.recv(4096)
            print(data)
            if "IN-USE".encode("utf-8") in data:
                s.close()
                makeUserAgain()
            if not data : 
                print("Socket is closed.")
                break
            else : print(data.decode("utf-8"))
        except OSError as msg:
            print(msg)
            continue
        

t1 = threading.Thread(target=getData)
t1.start()

def makeUser():
    my_username = input("Username: ")
    username = my_username
    message = "HELLO-FROM " + username + '\n'
    s.send(message.encode("utf-8"))

def makeUserAgain():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("18.195.107.195", 5378))
    my_username = input("Username: ")
    username = my_username
    message = "HELLO-FROM " + username + '\n'
    s.send(message.encode("utf-8"))
    
makeUser()

# message = "WHO\n"
# s.send(message.encode("utf-8"))
# users_list = s.recv(4096)
# print(users_list)
# for x in users_list:
#     if x == my_username:
#         my_username = input("This username has already been taken, please try another one: ")
#     else:
#         continue

while True:
    val = input("")
    if val == "!quit": 
        s.close()
        break
    elif val == "!who":
        message = "WHO\n"
        s.send(message.encode())
    elif "@" in val:
        val = val.replace("@", "SEND ")
        message = val + "\n"
        s.send(message.encode())
    else:
        val = input("")
t1.join()