from PyQt6.QtWidgets import (QApplication, QWidget, QTextEdit, QPushButton,
                              QHBoxLayout, QLineEdit, QLabel, QVBoxLayout)
from PyQt6.QtCore import pyqtSignal, QObject
import socket
import threading
from cryptography.fernet import Fernet

KEY = b'85yncM9Z8RBngCq2xttihn-zGH_6ihzgki7OmRWonq0='
fernet = Fernet(KEY)


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
        cipher_text = fernet.encrypt(secret_message)
        self.conn.sendall(cipher_text)
        self.message_area.append(f"Sen: {text}")
        self.textbox.clear()

    def receive_message(self, message):
        self.message_area.append(message)

    def wait_for_connection(self):
        try:
            self.conn, addr = self.s.accept()
            print("Bağlantı kabul edildi:", addr)
            threading.Thread(target=self.receive_loop, daemon=True).start()
        except Exception as e:
            print("Server accept hatası:", e)

    def receive_loop(self):
        try:
            while True:
                data = self.conn.recv(1024)
                if not data:
                    break
                decrypted_text = fernet.decrypt(data)
                original_text = decrypted_text.decode()
                self.new_message.emit(f"Karşı taraf: {original_text}")
        except Exception as e:
            print("Receive loop hatası:", e)


if __name__ == "__main__":
    app = QApplication([])
    window = modselector()
    window.show()
    app.exec()
