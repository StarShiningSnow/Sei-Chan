import discord
from mcstatus import JavaServer
from ai import model
from data import secret

MC_SYSTEM = "根據伺服器資訊創作抒情的短句。"

def setup(tree):
    @tree.command(name="mc",description="查看Minecraft伺服器即時資訊")
    async def mc(interaction):
        await interaction.response.defer()
        try:
            server = await JavaServer.async_lookup(secret.mc_ip)
            status = await server.async_status()
        except Exception:
            embed = discord.Embed(title="嗚……我找不到伺服器了。",description="Server Offline",color=discord.Color.red())
            await interaction.followup.send(embed=embed)
            return

        server_info = [
            ("**🌐 IP位置**",secret.mc_ip,False),
            ("**🟢 運行版本**",status.version.name,True),
            ("**🔵 在線人數**",f"{status.players.online} / {status.players.max}",True),
            ("**⚡ 延遲**",f"{status.latency:.0f} ms",True),
            ("**📢 本日公告**",str(status.description),False)]
        if status.players.sample:
            server_info.append((
                "**👤 在線玩家**","\n".join(player.name for player in status.players.sample),False))
            
        prompt = (f"伺服器資訊\n在線人數: {status.players.online}/{status.players.max}")
        if status.players.sample:
            prompt += "\n在線玩家: " + "、".join(player.name for player in status.players.sample)

        try:
            text = await model.generate(prompt,MC_SYSTEM,temperature=0.1,num_predict=500)
            text = text.split("#",1)[0].strip()
        except Exception:
            text = "Someone tell StarShiningSnow there is a problem with my AI."

        embed = discord.Embed(title="伺服器目前狀態",color=discord.Color.green())
        for name,value,inline in server_info:
            embed.add_field(name=name,value=value,inline=inline)
        embed.set_footer(text=text)
        await interaction.followup.send(embed=embed)