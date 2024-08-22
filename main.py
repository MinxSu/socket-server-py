import asyncio
import websockets
import json
import time
import queue

# Maximum number of concurrent connections allowed
# MAX_CONNECTIONS = 3
# Create a semaphore to limit connections
# connection_semaphore = asyncio.Semaphore(MAX_CONNECTIONS)

MAX_CONNECTIONS = 10
connection_counter = 0


async def handle_message(websocket):
        # async with connection_semaphore:
    if connection_counter >= MAX_CONNECTIONS:
        await websocket.close(1013, "Maximum connections reached")
        return

    connection_counter += 1
    try:
        async for message in websocket:
            try:
                # 解碼JSON訊息
                data = json.loads(message)
                print(f"Received message: {data}")

                # fake process
                time.sleep(3)
                # if data["event"] == "SAY":
                #     response_data = {"event": "CHAT_MSG", "user": "", "message": data["message"]}
                # else:
                #     response_data = {"event": "CHAT_MSG", "user": "", "message": "Set_name"}
                response_data = {"response": f"{data} Message received successfully!"}

                # 將回應編碼為JSON並發送回客戶端
                response_message = json.dumps(response_data)
                await websocket.send(response_message)

            except json.JSONDecodeError:
                print("Invalid JSON format")

    finally:
        connection_counter -= 1
        pass


async def main():
    async with websockets.serve(handle_message, "127.0.0.1", 8766):
        print('start server: 127.0.0.1:8766')
        await asyncio.Future()  # run forever


asyncio.run(main())
