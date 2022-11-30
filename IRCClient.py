import socket
import codecs

import logger


class IRCSimpleClient:
    def __init__(self, username, server="irc.freenode.net",
                 port=6667):
        self.username = username
        self.server = server
        self.port = port
        self._conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.channels = []

    @staticmethod
    def _channel_format(channel: str) -> str:
        return channel if channel.startswith("#") else f"#{channel}"

    def connect(self):
        try:
            self._conn.connect((self.server, self.port))
        except Exception:
            logger.log("Failed")
            return False
        return True

    def get_response(self):
        resp = self._conn.recv(2048)
        return codecs.decode(resp, encoding="cp1251")

    def send_cmd(self, cmd, message):
        command = f"{cmd} {message}\r\n".encode("cp1251")
        self._conn.send(command)
        print("send command", command.decode("cp1251"))
        #сделать этот метод приватным

    def send_message_to_channel(self, message):
        command = "PRIVMSG {}".format(self.channel)
        message = ":" + message
        self.send_cmd(command, message)

    def join_channel(self, channel):
        self.channel = self._channel_format(channel)
        cmd = "JOIN"
        channel = self.channel
        self.send_cmd(cmd, channel)

    def get_channel_list(self):
        self.send_cmd("LIST", "")


