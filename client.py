import socket
from threading import Thread
username = input("Enter Username: ")
Server_Ip_Address = input("Enter Server's IPAddress: ")
port1 = 5055
port2 = 5056
s1 = socket.socket()
s2 = socket.socket()
global connecter1
global connecter2
global a
global b
connecter1 = (Server_Ip_Address,port1)
connecter2 = (Server_Ip_Address,port2)
RegToSend = "REGISTER TOSEND " + username +"\n"+"\n"
RegToRecv = "REGISTER TORECV " + username +"\n"+"\n"
s1.connect(connecter1)
s2.connect(connecter2)
def RegistarAgain(s1,s2):
    s1.close()
    s2.close()
    stop_threads = True
    s1 = socket.socket()
    s2 = socket.socket()
    s1.connect(connecter1)
    s2.connect(connecter2)
    s1.send(RegToSend.encode())
    a = s1.recv(1024).decode()
    print(a)
    s2.send(RegToRecv.encode())
    b = s2.recv(1024).decode()
    print(b)
    t1 = Thread(target=send, args=(s1,s2,))
    stop_threads = False
    t2 = Thread(target=recieve, args=(s2,))

    # starting thread 1
    t1.start()
    # starting thread 2
    t2.start()
    return True
def CheckInput(x):
    if(x[0]!='@'):
        return -1
    j = 0
    for i in range (0,len(x)):
        if(x[i]==' '):
            if(j==0):
                k = i
            j = j +1
    if(j>=1):
        return k
    else:
        return -1
def send(s1,s2):
  while True:
        messageinput = input("Enter RecipientName And Message: ")
        pos = CheckInput(messageinput)
        if(pos == -1):
              print("Error Input is not message format Please Try Again")
              continue
        else:
           recipientname = messageinput[1:pos]
           message = messageinput[pos+1:]
           sendmessage = "SEND " + recipientname + "\n" + "Content-length:" + str(len(message))+ "\n\n" + message
           s1.send(sendmessage.encode())
           d = s1.recv(1024).decode()
           print(d)
           if(d=="ERROR 103 Header incomplete\n\n"):
               RegistarAgain(s1,s2)
               break


def recieve(s2):
    while True:
      try:
        c = s2.recv(1024).decode()
        lines = c.split('\n')
        print("\n"+c)
        if (lines[1][15:] == ""):
                s2.send(bytes("ERROR 103 Header incomplete\n\n", "utf-8"))
        else:
                s2.send(bytes("RECEIVED" + lines[0][8:] + "\n\n", "utf-8"))
      except:
          break
i = 0
s1.send(RegToSend.encode())
a = s1.recv(1024).decode()
print(a)
s2.send(RegToRecv.encode())
b = s2.recv(1024).decode()
print(b)
while(True):
    if (a[0:10] == "REGISTERED" and b[0:10] == "REGISTERED"):
        break
    if(i>=1):
        username = input("There is problem with your Username Enter different Username: ")
        RegToSend = "REGISTER TOSEND " + username + "\n" + "\n"
        RegToRecv = "REGISTER TORECV " + username + "\n" + "\n"
        s1.close()
        s2.close()
        s1 = socket.socket()
        s2 = socket.socket()
        s1.connect(connecter1)
        s2.connect(connecter2)
        s1.send(RegToSend.encode())
        a = s1.recv(1024).decode()
        print(a)
        s2.send(RegToRecv.encode())
        b = s2.recv(1024).decode()
        print(b)
        if (a[0:10] == "REGISTERED" and b[0:10] == "REGISTERED" ):
            break
    i = i+1


t1 = Thread(target=send, args=(s1,s2,))
t2 = Thread(target=recieve, args=(s2,))

# starting thread 1
t1.start()
# starting thread 2

t2.start()
