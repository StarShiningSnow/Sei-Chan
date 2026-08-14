from mcrcon import MCRcon
import secret

def setup(client):
    @client.event
    async def on_message(message):
        if message.author.bot or message.channel.id != secret.dc_id:
            return
        with MCRcon(secret.lan_ip,secret.rcon_pw,port=25575) as rcon:
            color = str(message.author.top_role.color) if message.author.top_role.color.value else "white"
            rcon.command(f'tellraw @a [{{"text":"[Discord] ","color":"gray"}},{{"text":"{message.author.display_name}","color":"{color}","hoverEvent":{{"action":"show_text","contents":"Discord 帳號：{message.author.name}\\n身份組：{message.author.top_role.name}"}}}},{{"text":"：{message.content}","color":"white"}}]')