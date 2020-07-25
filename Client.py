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
        self.sending_lock = threading.Lock()

    def send(self, message):
        self.sending_lock.acquire()
        data = str(message) + '$$$'
        self.sock.send(bytearray(data, 'utf-8'))
        self.sending_lock.release()
    
    def login(self, _id):
        self.id = _id
        message = {'type': 'LOGIN', 'sender': self.id, 'receiver': '_Server'}
        self.send(str(message))
        while True:
            data = self.sock.recv(BUFSIZE)
            if data: 
                break
        data = str(data, 'utf-8')
        data = eval(data)
        return data['body']
    
    def handle_client_info(self, data):
        _id = data['sender']
        _num = data['num']
        self.lock.acquire()
        message = self.chats[_id]['messages'][_num]
        message['status'] = data['body']
        if data['body'] == 'SEEN':
            self.chats[_id]['new'] += 1
        self.lock.release()
    
    def send_info(self, info, num, _id):
        message = {'type': 'INFO', 'sender': self.id, 'num': num, 'body': info, 'receiver': _id}
        self.send(message)

    def handle_message(self, data):
        _id = data['sender']
        message = {'sender': _id, 'status': 'RECV', 'body': data['body']}
        self.lock.acquire()
        if _id not in self.chats:
            self.chats[_id] = {'messages': [], 'new': 0}
        self.chats[_id]['messages'].append(message)
        length = len(self.chats[_id]['messages'])
        self.lock.release()
        self.send_info('RECV', length-1, _id)
        print(c.chats)

    def handle_data(self, raw_data):
        splitted_data = raw_data.split('$$$')[:-1]
        for data in splitted_data:
            data = eval(data)
            if data['type'] == 'INFO':
                if data['sender'] != '_Server':
                    self.handle_client_info(data)
            elif data['type'] == 'MSSG':
                self.handle_message(data)

    def receive(self):
        while True:
            data = self.sock.recv(BUFSIZE)
            if not data:
                continue
            data = str(data, 'utf-8')
            self.handle_data(data)
        self.sock.close()
    
    def send_message(self, _id, text):
        message = {'sender': self.id, 'status': 'SEND', 'body': text}
        self.lock.acquire()
        if _id not in self.chats:
            self.chats[_id] = {'messages': [], 'new': 0}
        self.chats[_id]['messages'].append(message)
        self.lock.release()
        data = {'type':'MSSG', 'sender': self.id, 'body': text, 'receiver': _id}
        self.send(data)
    
    def seen(self, _id):
        self.lock.acquire()
        self.chats[_id]['new'] = 0
        messages = self.chats[_id]['messages']
        length = len(messages)
        for i in range(length-1, 0, -1):
            if messages[i]['status'] == 'SEEN':
                break
            messages[i]['status'] = 'SEEN'
            self.send_info('SEEN', i, _id)
        self.lock.release()
               
    def start(self):
        thread = threading.Thread(target=self.receive, args=())
        thread.start()

if __name__=='__main__':
    c = Client()
    c.login(input('id: '))
    c.start()
    while True:
        cmd = input('msg: ')
        cmd = cmd.split()
        c.send_message(cmd[0], cmd[1])
        c.seen(cmd[0])

    
