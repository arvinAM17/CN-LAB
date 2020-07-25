import socket
import threading

HOST = 'localhost'
PORT = 8080
ADDR = (HOST,PORT)
BUFSIZE = 4096

class Client():
    def __init__(self):
        self.sock = socket.socket()                     
        self.sock.connect(ADDR)
        self.id = None
        self.chats = dict()
        self.lock = threading.Lock()

    def send(self, message):
        self.lock.acquire()
        data = str(message)
        self.sock.send(bytearray(data, 'utf-8'))
        self.lock.release()
    
    def loggin(self, _id):
        self.id = _id
        message = {'type': 'LOGIN', 'id': self.id, 'reciever': '_Server'}
        data = bytearray(str(message), 'utf-8')
        self.sock.send(data)
        while True:
            data = self.sock.recv(BUFSIZE)
            if data: 
                break
        data = str(data, 'utf-8')
        data = eval(data)
        return data['body']
    
    def handle_client_info(self, data):
        _id = data['id']
        _num = data['MSSG_NUM']
        self.lock.acquire()
        message = self.chats[_id]['messages'][_num]
        message['status'] = data['body']
        self.lock.release()
    
    def send_info(self, _id, info):
        message = {'id': _id}

    def handle_message(self, data):
        _id = data['id']
        message = {'sender': _id, 'status': 'RECV', 'body': data['body']}
        self.lock.acquire()
        self.chats[_id]['messages'].append(message)
        self.lock.release()

    def handle_data(self, raw_data):
        data = eval(raw_data)
        if data['type'] == 'INFO':
            if data['id'] != '_Server':
                self.handle_client_info(data)
        elif data['type'] == 'MSSG':
            self.handle_message(data)

    def recieve(self):
        while True:
            data = self.sock.recv(BUFSIZE)
            if not data:
                continue
            data = str(data, 'utf-8')
            self.handle_data(data)
        self.sock.close()
        
    def start(self):

if __name__=='__main__':
    
