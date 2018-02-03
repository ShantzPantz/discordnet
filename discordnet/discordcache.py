import json

message_cache_file = 'data/server_messages.json'


async def update_messages_cache(client):
    rows = []
    for server in client.servers:
        for channel in server.channels:
            async for m in client.logs_from(channel, limit=10000):
                rows.append({
                    'id': m.id,
                    'timestamp': m.timestamp.timestamp(),
                    'content': m.content,
                    'clean_content': m.clean_content,
                    'server_name': m.server.name,
                    'server_id': m.server.id,
                    'channel_name': m.channel.name,
                    'channel_id': m.channel.id,
                    'user': m.author.name,
                    'user_id': m.author.id,
                    'bot': m.author.bot
                })

    output = json.dumps(rows)
    fh = open(message_cache_file, "w")
    fh.write(output)
    fh.close()
    print("Done")


async def get_messages_from_cache(channel_id=None, user_id=None):
    jsondata = json.load(open(message_cache_file))
    usermessages = list(filter(lambda x: x['user_id'] == user_id
                        and (channel_id == x['channel_id']), jsondata))
    return usermessages


async def update_messages_if_required(client):
    await update_messages_cache(client)
