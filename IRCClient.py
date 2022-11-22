import socket
import codecs


class IRCSimpleClient:
    def __init__(self, username, channel, server="irc.freenode.net",
                 port=6667):
        self.username = username
        self.server = server
        self.port = port
        self.channel = self._channel_format(channel)
        self._conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    @staticmethod
    def _channel_format(channel: str) -> str:
        return channel if channel.startswith("#") else f"#{channel}"

    def connect(self):
        try:
            self._conn.connect((self.server, self.port))
        except Exception:
            return False
        username = self.username
        self.send_cmd("USER", f"{username} {username} {username} {username}")
        self.send_cmd("NICK", f"{username}")
        return True

    def get_response(self):
        resp = self._conn.recv(2048)
        return codecs.decode(resp, encoding="cp1251")

    def send_cmd(self, cmd, message):
        command = f"{cmd} {message}\r\n".encode("cp1251")
        self._conn.send(command)
        print("send command", command.decode("cp1251"))

    def send_message_to_channel(self, message):
        command = "PRIVMSG {}".format(self.channel)
        message = ":" + message
        self.send_cmd(command, message)

    def join_channel(self):
        cmd = "JOIN"
        channel = self.channel
        self.send_cmd(cmd, channel)

