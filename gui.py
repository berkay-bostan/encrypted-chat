from PyQt6.QtWidgets import (QApplication, QWidget, QTextEdit, QPushButton,
                              QHBoxLayout, QLineEdit, QLabel, QVBoxLayout)
from PyQt6.QtCore import pyqtSignal, QObject
import socket
import threading
from cryptography.fernet import Fernet
import secrets
import hashlib
import base64


p_hex = """
FFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD
129024E088A67CC74020BBEA63B139B22514A08798E3404
DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C
245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406
B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE
45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD
24CF5F83655D23DCA3AD961C62F356208552BB9ED529077
096966D670C354E4ABC9804F1746C08CA18217C32905E46
2E36CE3BE39E772C180E86039B2783A2EC07A28FB5C55DF
06F4C52C9DE2BCBF6955817183995497CEA956AE515D226
18985811D52D8ECD9F4E62A2BE28D63C1FDA4B0F6D8B27C
7D82A6A1C0A9AB558173D2A5AA37AAA3F4F5B70FE2AB05D
40F6F757683D8CC94E243F5DED6DD5F52F9DBF1A147E28C
7E3C1E9AACD3F9E52F7C5A9D4C3B2A4EE73CFAA31D89D8B
1FE4A0FCD8A1E0FC2A0AC91C7B23E3D2C97C0A5A2F0F0EF
1A48F9A0A6E3B84698C1D6E13FD8A5C6D5DB18F9BF1E6E4
FFFFFFFFFFFFFFFF
""".replace("\n", "")
p = int(p_hex, 16)
g = 2


class modselector(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mod Selector GUI")
        self.setGeometry(100, 100, 600, 500)
        self.label = QLabel()
        button1 = QPushButton("server")
        button2 = QPushButton("client")
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(button1)
        layout.addWidget(button2)
        self.setLayout(layout)
        button1.clicked.connect(self.server_selected)
        button2.clicked.connect(self.client_selected)

    def server_selected(self):
        self.chat_window = chatWindow("server")
        self.chat_window.show()
        self.close()

    def client_selected(self):
        self.chat_window = chatWindow("client")
        self.chat_window.show()
        self.close()


class chatWindow(QWidget):
    new_message = pyqtSignal(str)

    def __init__(self, mode):
        super().__init__()
        self.setWindowTitle(f"Encrypted Chat - {mode}")
        self.mode = mode

        if mode == "server":
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.bind(("127.0.0.1", 9000))
            self.s.listen(1)
            threading.Thread(target=self.wait_for_connection, daemon=True).start()

        if mode == "client":
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.connect(("127.0.0.1", 9000))
            self.conn = self.s
            A_bytes = self.conn.recv(384)
            A = int.from_bytes(A_bytes,"big")
            b = secrets.randbelow(p)
            B = pow(g,b,p)
            self.conn.sendall(B.to_bytes(384,"big"))
            shared_secret = pow(A,b,p)
            derived_key = hashlib.sha256(shared_secret.to_bytes(384,"big")).digest()
            self.fernet = Fernet(base64.urlsafe_b64encode(derived_key))
            threading.Thread(target=self.receive_loop, daemon=True).start()

        self.setGeometry(150, 150, 500, 500)
        self.message_area = QTextEdit()
        self.message_area.setReadOnly(True)

        self.textbox = QLineEdit()
        self.send_button = QPushButton("Send")

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.textbox)
        input_layout.addWidget(self.send_button)

        layout = QVBoxLayout()
        layout.addWidget(self.message_area)
        layout.addLayout(input_layout)
        self.setLayout(layout)

        self.send_button.clicked.connect(self.send_message)
        self.new_message.connect(self.receive_message)

    def send_message(self):
        text = self.textbox.text()
        secret_message = text.encode()
        cipher_text = self.fernet.encrypt(secret_message)
        self.conn.sendall(cipher_text)
        self.message_area.append(f"Sen: {text}")
        self.textbox.clear()

    def receive_message(self, message):
        self.message_area.append(message)

    def wait_for_connection(self):
        try:
            self.conn, addr = self.s.accept()
            a = secrets.randbelow(p)
            A = pow(g,a,p)
            self.conn.sendall(A.to_bytes(384,"big"))
            B_bytes = self.conn.recv(384)
            B = int.from_bytes(B_bytes,"big")
            shared_secret = pow(B,a,p)
            derived_key = hashlib.sha256(shared_secret.to_bytes(384,"big")).digest()
            self.fernet = Fernet(base64.urlsafe_b64encode(derived_key))
            print("Bağlantı kabul edildi:", addr)
            threading.Thread(target=self.receive_loop, daemon=True).start()
        except Exception as e:
            import traceback
            traceback.print_exc()

    def receive_loop(self):
        try:
            while True:
                data = self.conn.recv(1024)
                if not data:
                    break
                decrypted_text = self.fernet.decrypt(data)
                original_text = decrypted_text.decode()
                self.new_message.emit(f"Karşı taraf: {original_text}")
        except Exception as e:
            print("Receive loop hatası:", e)


if __name__ == "__main__":
    app = QApplication([])
    window = modselector()
    window.show()
    app.exec()
