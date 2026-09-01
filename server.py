import socket
from cryptography.fernet import Fernet
import threading

KEY = b'85yncM9Z8RBngCq2xttihn-zGH_6ihzgki7OmRWonq0='
fernet = Fernet(KEY)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("127.0.0.1",9000))
s.listen(1)
print("Listening...")
conn, addr = s.accept()
print("Connecting ",addr)

def receive_loop(sock):
    while True:
        data = sock.recv(1024)
        if not data:
            break
        decrypted_text = fernet.decrypt(data)
        original_text = decrypted_text.decode()
        print("Received: ",original_text)

def send_loop(sock):
    while True:
        message = input("Send: ")
        secret_message = message.encode()
        cipher_text = fernet.encrypt(secret_message)
        sock.sendall(cipher_text)         

thread1 = threading.Thread(target=receive_loop,args=(conn,))
thread2  = threading.Thread(target=send_loop,args = (conn,))

thread1.start()
thread2.start()

thread1.join()
thread2.join()



