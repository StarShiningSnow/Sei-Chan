import asyncio,re,discord,secret

async def log(channel):
    process = await asyncio.create_subprocess_exec("tail", "-f", secret.log_path, stdout=asyncio.subprocess.PIPE)
    async for line in process.stdout: # type: ignore
        msg = line.decode().strip().split("]: ")[-1]
        if m := re.match(r"(.+) joined the game$", msg):
            embed = discord.Embed(title="🛬 帝国領域 入国記録",description=f"【入国者】 {m.group(1)} 殿",color=discord.Color.green())
        elif m := re.match(r"(.+) left the game$", msg):
            embed = discord.Embed(title="🛫 帝国領域 出国記録",description=f"【出国者】 {m.group(1)} 殿",color=discord.Color.red())
        elif m := re.match(r"<(.+)> (.+)", msg):
            embed = discord.Embed(title="💬 帝国領域内 発言伝達",description=f"**{m.group(1)}**\n> {m.group(2)}",color=discord.Color.blue())
        elif m := re.match(r"(.+) has made the advancement (.+)", msg):
            embed = discord.Embed(title="🏆 帝国偉業達成 顕彰",description=f"**{m.group(1)}**\n> 【{m.group(2)}】",color=discord.Color.gold()) 
        else: continue
        embed.set_author(name=m.group(1),icon_url=f"https://mc-heads.net/avatar/{m.group(1)}")
        embed.set_footer(text="⚙️ 連邦省情報局電信転送 • 帝国領域内受信")
        await channel.send(embed=embed)