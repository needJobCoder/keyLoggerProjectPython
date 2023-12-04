import asyncio
import threading

HOST = 'localhost'
PORT = 3000
CLIENTS = []
server = None


async def echo_server(reader, writer):
    while True:
        data = await reader.read(1024)
        if not data:
            break
        print(data)
        writer.write(data)
        await writer.drain()  # Flow control, see later
    writer.close()


async def startServer(host, port):
    server = await asyncio.start_server(echo_server, host, port)
    print(f"Server Started at {HOST} on {PORT}")
    await server.serve_forever()


def setLoopEventForServerStart():
    asyncio.run(startServer(HOST, PORT))


async def createClient():
    client = await asyncio.open_connection(HOST, PORT)
    print(client)
    if client:
        CLIENTS.append(client)
        print(f"Client appended {client}")
        return client


def joinClient():
    asyncio.run(createClient())


async def broadCastMessage(messsage="broadcastHelloWorld"):
    if len(CLIENTS) > 0:
        print(f"number of client {len(CLIENTS)}")
        for client in CLIENTS:
            try:
                reader, writer = client
                writer.write(messsage.encode("utf-8"))
                await writer.drain()
            except Exception as e:
                print(f"Error broadcasting message to client: {e}")


async def sendMessageToServer(socket, message="hello World"):
    reader, writer = socket
    print(f"sending {message}")
    writer.write(message.encode("utf-8"))
    await writer.drain()


threading.Thread(target=setLoopEventForServerStart).start()



