import discord,secret,status,map

client = discord.Client(intents=discord.Intents.default())
tree = discord.app_commands.CommandTree(client)

status.setup(tree)
map.setup(tree)

@client.event
async def on_ready():
    await tree.sync()

client.run(secret.dc_token)