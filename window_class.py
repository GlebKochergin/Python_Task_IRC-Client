from PyQt6.QtWidgets import \
    QApplication, QPushButton, QVBoxLayout, QLineEdit, QLabel, \
    QStackedWidget, QDialog, QScrollArea
import sys

from IRCHandler import IRCHandler
from channels_window_class import ServerWindow
from chat_window_class import ChatWindow


def go_to_server_window():
    server_window = ServerWindow(go_to_chat_server,
                                 main_window.nickname.text(),
                                 main_window.irc_server_input.text())
    widget.addWidget(server_window)
    widget.setCurrentIndex(widget.currentIndex() + 1)


def go_to_chat_server():
    server = widget.currentWidget().channel_input.text()
    widget.currentWidget().IRCHandler.join_channel(server)
    chat_window = ChatWindow()
    widget.addWidget(chat_window)
    widget.setCurrentIndex(widget.currentIndex() + 1)


def go_to_previous_window():
    widget.setCurrentIndex(widget.currentIndex() - 1)


class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle('IRC-Client')
        self.resize(600, 400)
        self.setMaximumSize(1200, 800)
        self.setStyleSheet('background-image: url(main_back.jpg);')
        self.text = QLabel('Welcome to the club body!')
        self.text.setStyleSheet('font-size : 40px;')
        self.text.setMinimumSize(500, 50)
        self.text.setMaximumSize(600, 50)

        layout = QVBoxLayout()
        self.setLayout(layout)

        # layout.addWidget(scroll)

        self.irc_server_input = QLineEdit()
        self.irc_server_input.setStyleSheet('background-color: #D2FFF2; '
                                            'font-size : 30px;')
        self.irc_server_input.setMinimumSize(500, 50)
        self.irc_server_input.setMaximumSize(600, 50)
        self.irc_server_input.setPlaceholderText('Вставьте ссылку на '
                                                 'IRC-сервер')
        self.irc_server_input.setEchoMode(QLineEdit.EchoMode.Normal)

        self.nickname = QLineEdit()
        self.nickname.setStyleSheet('background-color: #D2FFF2; '
                                    'font-size : 30px;')
        self.nickname.setMinimumSize(500, 50)
        self.nickname.setMaximumSize(600, 50)
        self.nickname.setPlaceholderText('Введите свой никнейм')
        self.nickname.setEchoMode(QLineEdit.EchoMode.Normal)

        self.enter_button = QPushButton('Enter')
        self.enter_button.setStyleSheet('background-color: #2DBC91;'
                                        'font-size: 20px;')
        self.enter_button.setMinimumSize(500, 50)
        self.enter_button.setMaximumSize(600, 50)
        self.enter_button.clicked.connect(self.enter_chat)

        layout.addWidget(self.text)
        layout.addWidget(self.irc_server_input)
        layout.addWidget(self.nickname)
        layout.addWidget(self.enter_button)

        self.show()

    def enter_chat(self):
        if len(self.irc_server_input.text()) == 0 \
                or len(self.nickname.text()) == 0:
            self.setStyleSheet('background-color: #FF7070')
        else:
            self.setStyleSheet('background-image: url(main_back.jpg);')
            go_to_server_window()


app = QApplication(sys.argv)
widget = QStackedWidget()
widget.setMinimumSize(1200, 800)
widget.setMaximumSize(1200, 800)

main_window = MainWindow()
widget.addWidget(main_window)
widget.setWindowTitle(widget.currentWidget().windowTitle())
widget.show()

sys.exit(app.exec())
