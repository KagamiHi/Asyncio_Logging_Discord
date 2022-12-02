import json
import websockets
import asyncio

async def send_json_request(ws,request):
    await ws.send(json.dumps(request))

async def receive_json_response(ws):
    response = await ws.recv()
    if response:
        return json.loads(response)

async def heartbeat(intercal, ws):
    print ('Heartbeat begin')
    while True:
        await asyncio.sleep(intercal)
        heartbeatJSON={
            "op": 1,
            "d": "null"
        }
        await send_json_request(ws, heartbeatJSON)
        print ("Heartbeat sent")

async def start_discord_connect():
    async with websockets.connect('wss://gateway.discord.gg/?v=6&encording=json') as ws:
        event = await receive_json_response(ws)
        heartbeat_interval = event['d']['heartbeat_interval'] / 1000
        loop = asyncio.get_event_loop()
        loop.create_task(heartbeat(heartbeat_interval, ws))
        ###################################
        user_token = 'TOKEN HERE'
        ###################################
        payload = {
            "op": 2,
            "d": {
                "token": user_token,
                "properties": {
                    "$os": 'windows',
                    '$browser': 'chrome' ,
                    '$device': 'pc'
                }
            }
        }
        await send_json_request(ws,payload)
        loop.run_until_complete(await receiver_discord_connection (ws, bot, telegram_user_id))
        
async def receiver_discord_connection (ws):
    while True:
        received_event = await receive_json_response(ws)
        if received_event == None:
            print ('event is None')
            ws.close()
        else:
            try:
                if received_event['t'] == 'MESSAGE_CREATE':
                    refined_event = await translate_event_to_message_info_list(received_event['d'])
                    discord_message = " : ".join([refined_event[0]]+refined_event[2:5])
                    print (discord_message) 
            except:
                pass    

async def translate_event_to_message_info_list(message_event):
    discord_event_info_list=['No data','No data','No data','No data','No data', 'No data']
    if 'member' in message_event:
        message_type = 'Group'
    else:
        message_type = 'Privat'
    timestamp_list = message_event['timestamp'][:19].split("T")
    author = message_event['author']
    author_username = author['username']
    author_discord_id = author['id']
    content = message_event['content']
    discord_event_info_list[0] = message_type
    discord_event_info_list[1] = timestamp_list[0]
    discord_event_info_list[2] = timestamp_list[1]
    discord_event_info_list[3] = author_username
    discord_event_info_list[4] = content
    discord_event_info_list[5] = author_discord_id
    return discord_event_info_list


if __name__ == "__main__":               
    asyncio.run(start_discord_connect()) 