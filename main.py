import asyncio
from IRCClient import IRCSimpleClient
import threading
from data_analyze import IRCDataAnalyzer
from logger import log


def print_response(client):
    pass
    resp = client.get_response()
    if resp:
        if len(str(resp)) != 0:
            msg = resp.strip().split(":")
            log("response" + " " + "<{}> {}".format(msg[1].split("!")[0],
                                                    msg[2].strip()))


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


def get_channels(raw_data: str):
    channels = []
    for line in raw_data.split("\r\n"):
        if line == "":
            continue
        if line.split(" ")[1] == "322":
            channels.append(line.split(" ")[3])

    return channels


async def start_irc_client(username: str, channel: str):
    cmd = ""
    joined = False
    client = IRCSimpleClient(username, channel, "irc.ircnet.ru")
    client.connect()
    names = IRCDataAnalyzer(get_names)
    channels = IRCDataAnalyzer(get_channels)
    while not joined:
        resp = str(client.get_response())

        if len(resp) != 0:
            log("recieved", resp.strip())

        if "PING" in resp:
            for line in resp.split("\n"):
                if line.startswith("PING"):
                    client.send_cmd("PONG", ":" + line.split(":")[1]
                                    .strip("\r\n"))
                    break

        if "No Ident response" in resp:
            client.send_cmd("NICK", username)
            client.send_cmd(
                "USER", "{} * * :{}".format(username, username))

        if "321" in resp:
            await channels.add_raw_data(resp)
            continue

        if "323" in resp:
            await channels.add_raw_data(resp)
            client.join_channel()
            print(await channels.get_data())
            continue

        if "322" in resp:
            await channels.add_raw_data(resp)
            continue

        # we're accepted, now let's join the channel!
        if "376" in resp:
            client.send_cmd("LIST", "")

        # username already in use? try to use username with _
        if "433" in resp:
            username = "_" + username
            client.send_cmd("NICK", username)
            client.send_cmd(
                "USER", "{} * * :{}".format(username, username))

        if "333" in resp:
            await names.add_raw_data(resp)
            continue

        if "353" in resp:
            await names.add_raw_data(resp)

        # we've joined
        if "366" in resp:
            joined = True

    print(await names.get_data())
    while (cmd != "/quit"):
        cmd = input(f"<{username}> :").strip()
        if cmd == "/quit":
            client.send_cmd("QUIT", "App closed")
        client.send_message_to_channel(cmd)

        response_thread = threading.Thread(target=print_response,
                                           args=[client])
        response_thread.daemon = True
        response_thread.start()


if __name__ == "__main__":
    asyncio.run(start_irc_client("ff", "#freenode"))
