import copy
import Client

clients = {}

LOGIN = 0
MENU = 1
CHATS = 2


def CLI():
    global state
    current_client = None
    while True:
        if state == LOGIN:
            print('-- Hello!')
            id = input('-- Please enter your id: ')
            if id in clients:
                current_client = clients[id]
            else:
                current_client = Client.Client()
                current_client.login(id)
                clients[id] = current_client
            current_client.start()
            state = MENU

        elif state == MENU:
            print('-- chats: view your chats')
            print('-- send: send a message to a chat id')
            print('-- logout: exit this user')
            print('-- exit: exit the program')
            command = input()
            if command == 'chats':
                state = CHATS
            elif command == 'send':
                id = input('Please enter the receiving id: ')
                message = input('Please enter the message: ')
                ans = current_client.send_message(id, message)
                if ans == 'RECV':
                    print('Message successfully sent to ' + id)
                elif ans == 'NEXIST':
                    print('Could not send the message: id not found')
                elif ans == 'NSEND':
                    print('Message not sent')
                else:
                    print('WTH is happening')
            elif command == 'logout':
                current_client = None
                state = LOGIN
            elif command == 'exit':
                exit()
            else:
                print('unrecognized command, please enter again')

        elif state == CHATS:
            current_chats = copy.deepcopy(current_client.chats)
            for id in current_chats:
                num = current_chats[id]['new']
                print('- chat ' + id, '(' + str(num) + ')')
            print('-- see: see the messages of a chat')
            print('-- back: go back to the previous menu')
            command = input()
            if command == 'see':
                id = input('please enter the chat id')
                messages = current_chats[id]['messages']
                current_client.seen(id)
                for message in messages:
                    message_id = message['sender']
                    message_state = message['status']
                    message_body = message['body']
                    log = ''
                    if message_id == current_client.id:
                        log += 'you: '
                        log += message_body
                        log += 'seen' if message_state == 'SEEN' else 'sent'
                    else:
                        log += message_id + ': '
                        log += message_body
                    log += ' ' + message['time']
                    print(log)
            elif command == 'back':
                state = MENU
            else:
                print('unrecognized command, please enter again')

        else:
            print('WTF')


if __name__ == '__main__':
    state = LOGIN
    CLI()
