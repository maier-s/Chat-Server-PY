import socket
import ssl
from _thread import start_new_thread
from headerMessage import HEADER_SIZE

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)
ThreadCount = 0

class ChatServer:
    def __init__(self):
        self.context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        self.context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        self.context.load_cert_chain(certfile='/home/stefanmaier/Dokumente/Privat/cert/server.crt', keyfile='/home/stefanmaier/Dokumente/Privat/cert/server.key')

        self.server_socket= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((HOST,PORT))
        self.server_socket.listen(5)
        self.server_socket = self.context.wrap_socket(self.server_socket,server_side=True)
        self.registeredClient = []
    def getserverSocket(self):
        return self.server_socket
    def recieveData(self,connection):
        while True:
            acceptMessageHeader = connection.recv(HEADER_SIZE)
            if acceptMessageHeader:
                acceptMessageHeader = int(acceptMessageHeader.strip())
                acceptMessage = connection.recv(acceptMessageHeader)
                print(acceptMessage.decode('utf-8'))
    def registerClient(self,connection):
        self.registeredClient.append(connection)
    def getregisteredClients(self):
        return self.registeredClient
    
if __name__=="__main__":
    MainChatServer = ChatServer()
    while True:
        print("Warte auf Verbindung")
        connection, address = MainChatServer.getserverSocket().accept()
        #MainChatServer.registerClient(connection
        start_new_thread(MainChatServer.recieveData,(connection,))
        ThreadCount += 1
        print('Thread Number: ' + str(ThreadCount))

