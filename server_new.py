import socket
import threading as thr
from headerMessage import *
from server_sql import SQLServer

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)
ThreadCount = 0

class ChatServer:
    def __init__(self):
        self.server_socket= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((HOST,PORT))
        self.server_socket.listen(5)
        self.registeredClient = []
        self.UserDB = SQLServer()
        self.Threads = []
    def getserverSocket(self):
        return self.server_socket
    def recieveData(self,connection,address):
        # TODO: Registrer the Client that the client first has to login or register before he can send a message. Probably with an registration hex value
        while True:
            
            acceptMessageHeader = connection.recv(HEADER_SIZE)
            if not acceptMessageHeader: 
                print("Connection closed!")
                return True
            if acceptMessageHeader:
                acceptMessageHeader = int(acceptMessageHeader.strip())
                messageSignal = connection.recv(SIGNAL_SIZE)

                # Recieve Message
                #
                #
                if int(messageSignal.strip())==1:
                    acceptMessage = connection.recv(acceptMessageHeader)
                    print(address[0],":",address[1],"-->",acceptMessage.decode('utf-8'))

                # Register User
                #
                #
                if int(messageSignal.strip())==0:
                    print("recieved registration!")

                    len_name = int(connection.recv(NAME_SIZE).strip())
                    len_surname = int(connection.recv(SURNAME_SIZE).strip())
                    len_uname = int(connection.recv(UNAME_SIZE).strip())
                    len_pw = int(connection.recv(PASSW_SIZE).strip())

                    userName = connection.recv(len_name).decode('utf-8')
                    print(userName)
                    userSurname = connection.recv(len_surname).decode('utf-8')
                    userUName = connection.recv(len_uname).decode('utf-8')
                    userPW = connection.recv(len_pw).decode('utf-8')

                    print("UserName:",userUName,"\nPasswortHash: ",userPW)
                    #TODO: Check if the Username already exists otherwise User has to reenter the Username. Currently no checks on Username


                    self.UserDB.createUserinDB(userUName,userName,userSurname,userPW)
                # Handle Login
                #
                #
                if int(messageSignal.strip())==2:
                    len_uname = int(connection.recv(UNAME_SIZE).strip())
                    len_pw = int(connection.recv(PASSW_SIZE).strip())

                    userUName = connection.recv(len_uname).decode('utf-8')
                    userPW = connection.recv(len_pw).decode('utf-8')

                    print(userUName)

                    db_uName_PW = self.UserDB.getPasswort(userUName)[0][0]

                    if db_uName_PW == userPW:
                        print("Login from " + userUName + " sucessfull")
                        connection.sendall(bytes(format_return_message(2, True), 'utf-8'))
                    else:
                        print("Login from " + userUName + " failed")
                        connection.sendall(bytes(format_return_message(2, False), 'utf-8'))
                #Handle create Chat Event
                # This will return the UID of the Chat User so that the message can be correctly packed.

                if int(messageSignal.strip())==3:
                    chatUser = str(connection.recv(acceptMessageHeader).decode('utf-8'))
                    print("{}:{} wants to chat with {}".format(address[0],address[1],str(chatUser)))
                    print("I'm checking if the user exists and send him this message otherwise I store the message as long the user is offline.")
                    remotechatUser = self.UserDB.getUserName(chatUser)
                    # Send Back UID of the User and tehn recieve the message with the associated User
                    print(f'UID is {remotechatUser[0][0]}')
                    connection.sendall(bytes(fromat_uid_chatUser(str(remotechatUser[0][0]),4),'utf-8'))

                # Handle Chat Message:
                if int(messageSignal.strip())==5:
                    len_uid = int(connection.recv(UID_LENGTH).strip())
                    len_msg = int(connection.recv(MSG_SIZE).strip())

                    uid = int(connection.recv(len_uid).decode('utf-8'))
                    msg = connection.recv(len_msg).decode('utf-8')

                    print(f'Want to send: {msg} to UID {uid}')



    def registerClient(self,connection):
        self.registeredClient.append(connection)
    def getregisteredClients(self):
        return self.registeredClient
    def reciverThreadWatcher(self):
        while True:
            for thread in self.Threads:
                if not thread.is_alive():
                    self.Threads.remove(thread)

    def __del__(self):
        self.server_socket.close()
    
if __name__=="__main__":
    MainChatServer = ChatServer()
    thr_listener = thr.Thread(target=MainChatServer.reciverThreadWatcher)
    thr_listener.start()
    while True:
        print("Warte auf Verbindung")
        connection, address = MainChatServer.getserverSocket().accept()
        MainChatServer.registerClient(connection)
        thr_listener = thr.Thread(target=MainChatServer.recieveData,args=(connection,address,))
        thr_listener.start()
        MainChatServer.Threads.append(thr_listener)
        print('Thread Number: ' + str(len(MainChatServer.Threads)))

