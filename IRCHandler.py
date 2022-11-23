import asyncio

from IRCClient import IRCSimpleClient
from data_analyze import IRCDataAnalyzer
from logger import log


class IRCHandler:
    def __init__(self, username, server="irc.freenode.net", port=6667):
        self.client = IRCSimpleClient(username, server, port)
        self.names = list[str]

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

    async def get_channels_list(self) -> list[str]:
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
                await channels.add_raw_data(resp)
                return await channels.get_data()
                # channel = input(*[str(i) for i in client.channels])

            if "321" in resp or "322" in resp:
                await channels.add_raw_data(resp)
                continue

    async def join_channel(self, channel: str):
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
                await names.add_raw_data(resp)
                continue

            if "353" in resp:
                await names.add_raw_data(resp)

            if "366" in resp:
                self.names = await names.get_data()
                return True

    def get_names(self):
        return self.names

    async def send_message(self):
        print("INININININN")
        while True:
            msg = input("In")
            self.client.send_message_to_channel(msg)


    async def receive_messages(self):
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
                    log(f"{resp.split('!')[0]} joined")
                if action == "PRIVMSG":
                    print(f"{resp.split('!')[0]} " + resp.split(":")[2])

