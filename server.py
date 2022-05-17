import re
import socket
from threading import Thread
import sys
def CheckName(x):
      n = bool(re.match("^[A-Za-z0-9]*$",str(x[16:])))
      return n
def CheckReg(x):
      if(x[0:8]=="REGISTER" and (x[9:15]=="TOSEND" or x[9:15]=="TORECV")):
          return True
      return False
def Remove_Registeration(x):
     for j in send:
         if (send[j]==x):
             i=j
     del send[i]

     for j in recv:
         if (recv[j]==x):
             i = j
     del recv[i]
def Get_registered_Reply(x,p,z):
    Registeration_Message = x.split('\n')
    if(CheckName(Registeration_Message[0])==True and CheckReg(Registeration_Message[0])==True):
        if(z==0):
               recv[p] = Registeration_Message[0][16:]
        else:
               send[p] = Registeration_Message[0][16:]
        return x[0:8]+"ED"+x[8:]
    elif(CheckName(Registeration_Message[0]) == False and CheckReg(Registeration_Message[0])==True):
        return "ERROR 100 Malformed username\n\n"
    else:
        return "ERROR 101 No user registered\n\n"
def IsReg(x):
    for i in send:
        if(send[i]==x or x ==i):
            return True
    for i in recv:
        if (recv[i]==x or x ==i):
            return True
    if(x=="ALL"):
        return True
    return False
def findname(x):
    return recv[x]
def findp2(x):
    for i in send:
        if(send[i] == x):
            return i
def findp1(x):
    for i in recv:
        if(recv[i] == x):
            return i
def client_Registration(p1,p2):
        Registeration_Message = p1.recv(1024).decode()
        registered_Reply = Get_registered_Reply( Registeration_Message, p1, 0)
        print( registered_Reply )
        p1.send( registered_Reply .encode())
        Registeration_Message = p2.recv(1024).decode()
        registered_Reply = Get_registered_Reply( Registeration_Message, p2, 1)
        print( registered_Reply )
        p2.send( registered_Reply .encode())
def client_Message_Receiving_And_Sending(p1):
 if(IsReg(p1)):
   while True:
    message = p1.recv(1024).decode()
    if (message[0:4] != "SEND"):
        print("Error message is not in sending message form")
    else:
        lines = message.split('\n')
        if (lines[1][15:] == ""):
            p1.send(("ERROR 103 Header incomplete\n\n").encode())
            findp2(findname(p1)).close()
            p1.close()
            Remove_Registeration(findname(p1))
            break
        elif (IsReg(lines[0][5:]) == False):
            p1.send(("ERROR 102 Unable to send\n\n").encode())
            continue
        elif (lines[0][5:]=="ALL"):
            brodcast(p1,lines)
        else:
            ReplyToSender = "SEND " + lines[0][5:] + "\n\n"
            p1.send(ReplyToSender.encode())
            forwardmessage = "FORWARD " + findname(p1) + "\n" + lines[1] + "\n\n" + lines[3]
            recpient = lines[0][5:]
            p2 = findp2(recpient)
            p2.send(forwardmessage.encode())
            ReplyFromReceiver = p2.recv(1024).decode()
            print(ReplyFromReceiver)

def brodcast(p1,lines):
    ReplyToSender = "SEND" + lines[0][5:] + "\n\n"
    p1.send(ReplyToSender.encode())
    forwardmessage = "FORWARD " + findname(p1) + "\n" + lines[1] + "\n\n" + lines[3]
    for i in send:
        if(i==findp2(findname(p1))):
            continue
        i.send(forwardmessage.encode())
send = {}
recv = {}
port1 = 5055
port2 = 5056
s1 = socket.socket()
s2 = socket.socket()
binder1 = ('localhost',port1)
binder2 = ('localhost',port2)
s1.bind(binder1)
s2.bind(binder2)
s1.listen()
s2.listen()
print("Waiting For Connection\n\n")
while True:
   p1,address1 = s1.accept()
   p2,address2 = s2.accept()
   Registeration_Thread = Thread(target=client_Registration, args=(p1,p2))
   Registeration_Thread.start()
   SendingMessage_Thread = Thread(target=client_Message_Receiving_And_Sending, args=(p1,))
   SendingMessage_Thread.start()





