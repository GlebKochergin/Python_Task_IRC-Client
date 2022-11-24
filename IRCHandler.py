import asyncio
from chat_recorder import ChatRecorder
from IRCClient import IRCSimpleClient
from data_analyze import IRCDataAnalyzer
from logger import log


class IRCHandler:
    def __init__(self, username, server="irc.freenode.net", port=6667):
        self.client = IRCSimpleClient(username, server, port)
        self.names = list[str]
        self.recorder = ChatRecorder("log.txt")
        self.message = ''


    def connect_to_server(self):
        self.client.connect()
        username = self.client.username
        self.client.send_cmd("USER",
                             f"{username} {username} {username} {username}")
        self.client.send_cmd("NICK", f"{username}")
        connected = False
        while not connected:
            resp = str(self.client.get_response())

            if len(resp) != 0:
                log("recieved", resp.strip())

            if "No Ident response" in resp:
                self.client.send_cmd("NICK", username)
                self.client.send_cmd(
                    "USER", "{} * * :{}".format(username, username))

            if "PING" in resp:
                for line in resp.split("\n"):
                    if line.startswith("PING"):
                        self.client.send_cmd("PONG", ":" + line.split(":")[1]
                                             .strip("\r\n"))
                        break

            if "433" in resp:
                username = "_" + self.client.username
                self.client.send_cmd("NICK", username)
                self.client.send_cmd(
                    "USER", f"{username} * * {username}")

            if "376" in resp:
                return True

    def get_channels_list(self) -> list[str]:
        def get_channels(raw_data: str):
            channels = []
            for line in raw_data.split("\r\n"):
                if line == "":
                    continue
                if line.split(" ")[1] == "322":
                    channels.append(line.split(" ")[3])

            return channels

        channels = IRCDataAnalyzer(get_channels)
        self.client.send_cmd("LIST", "")

        while True:
            resp = str(self.client.get_response())
            if "323" in resp:
                channels.add_raw_data(resp)
                return channels.get_data()
                # channel = input(*[str(i) for i in client.channels])

            if "321" in resp or "322" in resp:
                channels.add_raw_data(resp)
                continue

    def join_channel(self, channel):
        def get_names(raw_data: str):
            users = []
            admins = []
            for line in raw_data.split("\r\n"):
                if line == "":
                    continue
                if line.split(" ")[1] == "353":
                    names = [_ for _ in line.split(":")[2].split(" ")]
                    for i in range(len(names)):
                        if names[i].startswith("@"):
                            admins.append(names[i])
                    names = filter(lambda x: not x.startswith("@"), names)
                    users += names
            print(admins)
            ans = sorted(admins, key=lambda x: x.lower())\
                  + sorted(users, key=lambda x: x.lower())
            return ans

        self.client.join_channel(channel)
        names = IRCDataAnalyzer(get_names)
        while True:
            resp = str(self.client.get_response())

            if len(resp) != 0:
                log("recieved", resp.strip())

            if "333" in resp:
                names.add_raw_data(resp)
                continue

            if "353" in resp:
                names.add_raw_data(resp)

            if "366" in resp:
                self.names = names.get_data()
                return True

            if "475" in resp:
                return False

    def get_names(self):
        return self.names

    def send_message(self):
        if self.message != '':
            self.client.send_message_to_channel(self.message)
            self.recorder.add_record(f"{self.client.username}: {self.message}")

    def receive_messages(self):
        while True:
            resp = str(self.client.get_response())
            if len(resp) != 0:
                log("recieved", resp.strip())

            if "PING" in resp:
                for line in resp.split("\n"):
                    if line.startswith("PING"):
                        self.client.send_cmd("PONG", ":" + line.split(":")[1]
                                             .strip("\r\n"))
                        break

            if len(resp.split("!")) == 2:
                action = resp.split(" ")[1]
                if action == "JOIN":
                    self.recorder.add_record(f"{resp.split('!')[0][1:]} joined")
                    return f"{resp.split('!')[0][1:]} joined"
                if action == "QUIT":
                    self.recorder.add_record(f"{resp.split('!')[0][1:]} quited")
                    return f"{resp.split('!')[0][1:]} quited"
                if action == "PRIVMSG":
                    self.recorder.add_record(f"{resp.split('!')[0][1:]} " + resp.split(":")[2])
                    return f"{resp.split('!')[0][1:]} " + resp.split(":")[2]

