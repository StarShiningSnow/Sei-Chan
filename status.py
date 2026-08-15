import discord,secret,mcstatus

def setup(tree):
    @tree.command(description="皇帝陛下、総理閣下、並びに高官の皆様へ報告です。帝國情報ネットワークは極めて円滑に稼働しております！ (⁠✧⁠ω⁠✧⁠)")
    async def status(interaction):
        await interaction.response.defer() 
        status = mcstatus.JavaServer.lookup("127.0.0.1").status()
        embed = discord.Embed(title="🎮 帝国情報網 稼働状況報告",color=discord.Color.green(),description=f"```\n{status.description}\n```")
        embed.add_field(name="🌐 帝国接続拠点",value=f"`{secret.wan_ip}`",inline=False)
        embed.add_field(name="📌 運用規格",value=f"`{status.version.name}`",inline=True)
        embed.add_field(name="👥 領域内滞在者",value=f"`{status.players.online} / {status.players.max}`",inline=True)
        embed.add_field(name="🟢 伝達遅延",value=f"`{round(status.latency,1)} ms`",inline=True)
        embed.add_field(name="🧑‍💻 監視対象名簿",value=f"```\n{'\n'.join(p.name for p in status.players.sample)if status.players.sample else '該当者なし'}\n```",inline=False)
        embed.set_footer(text="⚙️ 連邦省情報局管轄システム • 天皇陛下万歳！")
        await interaction.followup.send(embed=embed)