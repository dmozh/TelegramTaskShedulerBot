from aiohttp import web, WSMsgType
import json, asyncio


async def broadcast(request, msg):
    # while True:
    for ws in request.app.wslist:
        await ws.send_str(msg)
    # await asyncio.sleep(10)


async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    print(request.url)
    request.app.wslist.append(ws)
    print(request.app.wslist)
    async for msg in ws:
        print(msg)
        if msg.type == WSMsgType.TEXT:
            if msg.data == 'close':
                await ws.close()
            else:
                print(msg.data)
                # await broadcast(request, tmp_val)
                await ws.send_str(msg.data + '/answer')
        elif msg.type == WSMsgType.ERROR:
            print('ws connection closed with exception %s' %
                  ws.exception())

    print('websocket connection closed')
    print(ws)
    return ws
