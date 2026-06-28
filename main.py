import discord,data.secret
from mod import ask,mc,map,intro,ver

client = discord.Client(intents=discord.Intents.default())
tree = discord.app_commands.CommandTree(client)

ask.setup(tree)
mc.setup(tree)
map.setup(tree)
intro.setup(tree)
ver.setup(tree)

@client.event
async def on_ready():
    await tree.sync()
    print(f"以{client.user}登入成功")

client.run(data.secret.token)