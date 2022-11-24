from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QScrollArea, QLabel, QLineEdit
from IRCHandler import IRCHandler


class ServerWindow(QScrollArea):
    def __init__(self, func, nickname, server):
        super(ServerWindow, self).__init__()
        self.setWindowTitle('IRC-Chat')
        self.resize(1200, 800)
        self.setMaximumSize(1200, 800)
        self.setStyleSheet('background-image: url(second_back.png);')
        self.IRCHandler = IRCHandler(nickname, server)
        self.IRCHandler.connect_to_server()
        self.channels = self.IRCHandler.get_channels_list()

        layout = QVBoxLayout()
        self.setLayout(layout)

        for i in range(len(self.channels)):
            server_button = QLabel(f'{self.channels[i]}')
            # server_button = QPushButton(f'{self.channels[i]}')
            server_button.setStyleSheet('background-color: #2DBC91;'
                                        'font-size: 10px;')
            server_button.setMinimumSize(500, 25)
            server_button.setMaximumSize(600, 25)
            # server_button.clicked.connect(
            #     lambda x: self.IRCHandler.join_channel(self.channels[i]))
            layout.addWidget(server_button)
        self.channel_input = QLineEdit()
        self.enter_channel = QPushButton('Enter!')
        self.enter_channel.clicked.connect(func)
        layout.addWidget(self.channel_input)
        layout.addWidget(self.enter_channel)
        self.show()

