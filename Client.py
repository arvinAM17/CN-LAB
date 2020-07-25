import socket

HOST = 'localhost'
PORT = 8080
ADDR = (HOST,PORT)
BUFSIZE = 4096

class Client():
    def __init__(self):
        self.sock = socket.socket()                     
        self.sock.connect(ADDR)
        self.id = None

    def send(self, message):
        data = str(message)
        self.sock.send(bytearray(data, 'utf-8'))
    
    def loggin(self, _id):
        self.id = _id
        message = {'type': 'LOGIN', 'id': self.id, 'reciever': '_Server'}
        self.sock.send(message)
        while True:
            data = self.sock.recv(BUFSIZE)
            if data: 
                break
        data = str(data, 'utf-8')
        data = eval(data)
        return data['body']

    def start(self):
        
  
# receive data from the server 
print s.recv(1024) 
# close the connection 
s.close()

if __name__=='__main__':
    
