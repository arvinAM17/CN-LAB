import socket
import threading

HOST = 'localhost'
PORT = 8080
ADDR = (HOST,PORT)
BUFSIZE = 4096

class Client(threading.Thread):
    MEMBERS = dict()
    LOCK = threading.Lock()
    
    def __init__(self, sock, addr):
        threading.Thread.__init__(self)
        self.addr = addr
        self.sock = sock
        self.sending_lock = threading.Lock()

    def add_member(self, _id):
        LOCK.acquire()
        Client.MEMBERS[id] = self
        LOCK.release()
    
    def send(self, data):
        self.sending_lock.acquire()
        self.sock.send(bytearray(data, 'utf-8'))
        self.sending_lock.release()

    def send_from_server(self, body, rcv_id):
        message = {'type': 'INFO', 'id': '_Server', 'reciever': rcv_id}
        message['body'] = body
        self.send(str(message))
    
    def forward_message(self, data):
        _id = data['reciever']
        if _id not in Client.MEMBERS:
            return False
        client = Client.MEMBERS[_id]
        client.send(str(data))
        return True
    
    def handle_msg(self, raw_data):
        data = eval(raw_data)
        _id = message['id']
        if data['type'] == 'LOGIN':
            if _id[0] == '_':
                self.send_from_server('NVALID', _id)
            else:
                self.add_member(_id)
                self.send_from_server('SUCC', _id)
        elif data['type'] == 'MESSAGE':
            res = self.forward_message(data)
            if not res:
                self.send_from_server('NEXIST', _id)

    def run(self):
        while True:
            data = self.sock.recv(BUFSIZE)
            if not data: 
                continue
            data = str(data, 'utf-8')
            self.handle_msg(data)
        self.sock.close()

if __name__=='__main__':
    serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serv.bind(ADDR)
    serv.listen()
    while True:
        sock, addr = serv.accept()
        client = Client(sock, addr)
        client.start()