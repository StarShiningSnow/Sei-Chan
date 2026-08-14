import discord,secret,status,map,m2d,asyncio,d2m

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)

status.setup(tree)
map.setup(tree)
d2m.setup(client)
m2d_task = None

@client.event
async def on_ready():
    global m2d_task
    await tree.sync()
    if not m2d_task or m2d_task.done():
        m2d_task = asyncio.create_task(m2d.log(client.get_channel(secret.dc_id)))

client.run(secret.dc_token)