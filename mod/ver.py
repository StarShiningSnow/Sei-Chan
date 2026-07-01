import discord

def setup(tree):
    @tree.command(name="ver",description="查詢最新的版本紀錄")
    async def ver(interaction):
        await interaction.response.defer()
        with open("changelog.txt","r",encoding="utf-8") as f:
            content = f.read()
        parts = content.split("===")
        latest = parts[0].strip()
        embed = discord.Embed(title="更新紀錄",description=latest,color=discord.Color.random())
        await interaction.followup.send(embed=embed)