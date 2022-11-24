import asyncio
from IRCClient import IRCSimpleClient
import threading

from IRCHandler import IRCHandler
from logger import log


def print_response(client):
    pass
    resp = client.get_response()
    if resp:
        if len(str(resp)) != 0:
            msg = resp.strip().split(":")
            log("response" + " " + "<{}> {}".format(msg[1].split("!")[0],
                                                    msg[2].strip()))


async def start_irc_client(server: str, username: str):
    handler = IRCHandler(username=username, server=server)
    handler.connect_to_server()
    print(handler.get_channels_list())
    handler.join_channel("freenode")
    print(handler.get_names())
    tasks = [threading.Thread(target=handler.receive_messages),
             threading.Thread(target=handler.send_message())]

    for t in tasks:
        t.start()

    for t in tasks:
        t.join()

    #
    # while (cmd != "/quit"):
    #     cmd = input(f"<{username}> :").strip()
    #     if cmd == "/quit":
    #         client.send_cmd("QUIT", "App closed")
    #     client.send_message_to_channel(cmd)
    #
    #     response_thread = threading.Thread(target=print_response,
    #                                        args=[client])
    #     response_thread.daemon = True
    #     response_thread.start()


async def first_window(server, nickname):
    await start_irc_client(server, nickname)


if __name__ == "__main__":
    asyncio.run(first_window("irc.freenode.net", "ff"))
