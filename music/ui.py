import discord
from music import player

def music_embed(song,thumbnail=None):

    embed = discord.Embed(title="🎵 星輝醬音樂播放器",description="",color=discord.Color.gold())

    embed.add_field(name="🎧 目前播放",value=song["title"],inline=False)

    if song.get("thumbnail"):
        embed.set_image(url=song["thumbnail"])

    return embed

class MusicView(discord.ui.View):
    def __init__(self,voice,guild_id):
        super().__init__(timeout=None) 
        self.voice = voice
        self.guild_id = guild_id

    @discord.ui.button(emoji="⏮️",style=discord.ButtonStyle.secondary)
    async def previous(self,interaction,button):

        result = player.previous_music(
        self.voice,
        self.guild_id
    )

        if result:
            await interaction.response.send_message(
            "⏮️ 播放上一首",
            ephemeral=True
        )
        else:
            await interaction.response.send_message(
            "沒有上一首歌曲",
            ephemeral=True
        )

    @discord.ui.button(emoji="⏯️",style=discord.ButtonStyle.primary)
    async def pause(self,interaction,button):

        if self.voice.is_playing():
            player.pause_music(self.voice)
            await interaction.response.send_message(
            "⏸️ 已暫停",
            ephemeral=True)
        elif self.voice.is_paused():
            player.resume_music(self.voice)
            await interaction.response.send_message(
            "▶️ 繼續播放",
            ephemeral=True
        )

        else:
            await interaction.response.send_message(
            "目前沒有播放音樂",
            ephemeral=True
        )

    @discord.ui.button(emoji="⏭️",style=discord.ButtonStyle.secondary)
    async def skip(self,interaction,button):
        player.skip_music(
        self.voice,
        self.guild_id
    )

        await interaction.response.send_message(
        "⏭️ 已跳過歌曲",
        ephemeral=True
    )