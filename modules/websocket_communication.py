import asyncio
import functools
import json
import threading

import websockets

###########################---Communication Manager---###########################


class CommsManager:
    # This class will be used by the game to talk
    # to the other client

    def __init__(self):
        self.status = "Searching"

        self.to_send = []
        self.buffer = []
        self.updates = []

        self.running = True

        self.serverStop = None

    def flush(self):
        # clears the two current "to_send" and replaces it with the updates
        # that are in the buffer
        # this is to avoid race conditions

        self.to_send.clear()
        self.to_send = self.buffer
        self.buffer.clear()

    def send_message(self, update: dict):
        # send information to the server or client
        self.buffer.append(update)

    def load_updates(self, updates_json_str: str):
        updates_json = json.loads(updates_json_str)

        if "Updates" in updates_json.keys:
            content = updates_json["Updates"]
            [self.updates.append(item) for item in content if content != []]

    def parse_message(self, message_str):
        message_json = json.loads(message_str)

        content = message_json["Updates"]
        if content:
            self.updates += content

        if "websocket.disconnect" in content:
            self.running = False

    def get_unsend(self):
        if "websocket.disconnect" in self.to_send:
            self.running = False
        return json.dumps({"Updates": self.to_send})

    def export_updates(self):
        # returns the current updates and deletes the ones he returned
        to_return = self.updates.copy()
        [self.updates.remove(item) for item in to_return]
        return to_return


###########################---Threads---###########################


class WsServerThread(threading.Thread):
    # This Thread contains the sever
    # and is launched by the host

    def __init__(self, ip, port, c_manager: CommsManager):
        super().__init__()
        self.ip = ip
        self.port = port
        self.c_manager = c_manager

    async def ws_main(self):
        self.c_manager.serverStop = asyncio.Future()
        try:
            async with websockets.serve(functools.partial(server, c_manager=self.c_manager), self.ip, self.port):
                # run until c_manager.serverStop.set_result() is called
                await self.c_manager.serverStop
        except OSError:  # Can't connect to IP
            self.c_manager.status = "Failure"

    def run(self):
        asyncio.run(self.ws_main())


class WsClientThread(threading.Thread):
    # This Thread contains the client
    # and is launched by the non hosting player

    def __init__(self, ip, port, c_manager: CommsManager):
        super().__init__()
        self.ip = ip
        self.port = port
        self.c_manager = c_manager

    def run(self):
        try:
            asyncio.run(client(self.ip, self.port, c_manager=self.c_manager))
        except OSError:  # Can't connect to IP
            self.c_manager.status = "Failure"

###########################---Communication Functions---###########################


async def server(websocket, *args, **kwargs):
    # this functions handles communication for the server
    c_manager = kwargs.get("c_manager")

    c_manager.status = "Connected"

    while c_manager.running:
        await websocket.send(c_manager.get_unsend())  # Send information

        c_manager.flush()  # Delete the send information

        # Receive new information
        c_manager.parse_message(await websocket.recv())

        await asyncio.sleep(0.05)  # Wait; to not consume too much resources

    c_manager.status = "Disconnected"
    await websocket.close()
    c_manager.serverStop.set_result(0)   # set a result to end the future


async def client(ip, port, c_manager: CommsManager):
    # this functions handles communication for the client

    websocket = await websockets.connect(f"ws://{ip}:{port}")

    c_manager.status = "Connected"

    while c_manager.running:

        # Receive new information
        c_manager.parse_message(await websocket.recv())

        # print(c_manager.updates) #[DEBUG]

        await websocket.send(c_manager.get_unsend())  # Send information

        c_manager.flush()  # Delete the send information

        await asyncio.sleep(0.05)  # Wait; to not consume too much resources

    c_manager.status = "Disconnected"
    await websocket.close()


###########################---The Function to Call---###########################


def start_websocket(ip, port, is_host=False) -> CommsManager:
    # Stats the websocket in a different thread
    # and returns the CommsManager, he allows the user to communicate

    c_manager = CommsManager()

    if is_host:
        thread = WsServerThread(ip, port, c_manager)
    else:
        thread = WsClientThread(ip, port, c_manager)

    thread.start()

    return c_manager
