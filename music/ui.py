import discord
from music.queue import (
    toggle_loop, play_previous, is_looping, 
    toggle_autoplay, is_autoplay, 
    toggle_secret_mode, is_secret_mode
)

def format_time(seconds: float) -> str:
    m, s = divmod(int(seconds), 60)
    return f"{m:02d}:{s:02d}"

def create_music_embed(song: dict, elapsed: float) -> discord.Embed:
    duration = song.get('duration', 0)
    bar_length = 16
    
    if duration > 0:
        progress = min(max(elapsed / duration, 0.0), 1.0)
        if progress > 0.97:
            progress = 1.0

        filled = int(progress * bar_length)

        bar = "  " + "━" * filled + "●" + "━" * (bar_length - filled)
        curr_str = format_time(min(elapsed, duration))
        dur_str = format_time(duration)
        
        time_str = f"```{bar}\n{curr_str}" + " " * 12 + f"{dur_str}```"
    else:
        bar = "●" + "━" * bar_length
        curr_str = format_time(elapsed)
        time_str = f"```{bar}\n{curr_str}" + " " * 12 + "直播/無時長```"

    embed = discord.Embed(
        title=song.get('title', '未知歌曲'),
        url=song.get('webpage_url', 'https://www.youtube.com'),
        description=time_str,
        color=0x9B59B6
    )

    if song.get('thumbnail'):
        embed.set_thumbnail(url=song['thumbnail'])
        
    return embed


class PlayerView(discord.ui.View):
    def __init__(self, vc: discord.VoiceClient, guild_id: int | None = None):
        super().__init__(timeout=None)
        self.vc = vc
        
        gid = guild_id or (vc.guild.id if vc and vc.guild else None)
        if gid:
            for item in self.children:
                if isinstance(item, discord.ui.Button):
                    if item.label == "🔁" and is_looping(gid):
                        item.style = discord.ButtonStyle.success
                    elif item.label == "♾️" and is_autoplay(gid):
                        item.style = discord.ButtonStyle.success
                    elif item.label == "✨" and is_secret_mode(gid):
                        item.style = discord.ButtonStyle.success

    @discord.ui.button(label="⏮️", style=discord.ButtonStyle.secondary, row=0)
    async def prev(self, interaction, button):
        if play_previous(interaction.guild_id):
            if self.vc.is_playing() or self.vc.is_paused():
                self.vc.stop()
        await interaction.response.defer()

    @discord.ui.button(label="⏯️", style=discord.ButtonStyle.secondary, row=0)
    async def pause(self, interaction, button):
        if self.vc.is_playing():
            self.vc.pause()
            button.style = discord.ButtonStyle.danger
        elif self.vc.is_paused():
            self.vc.resume()
            button.style = discord.ButtonStyle.secondary
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="⏭️", style=discord.ButtonStyle.secondary, row=0)
    async def skip(self, interaction, button):
        if self.vc.is_playing() or self.vc.is_paused():
            self.vc.stop()
        await interaction.response.defer()

    @discord.ui.button(label="🔁", style=discord.ButtonStyle.secondary, row=1)
    async def loop(self, interaction, button):
        state = toggle_loop(interaction.guild_id)
        button.style = discord.ButtonStyle.success if state else discord.ButtonStyle.secondary
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="♾️", style=discord.ButtonStyle.secondary, row=1)
    async def autoplay(self, interaction, button):
        state = toggle_autoplay(interaction.guild_id, vc=self.vc, loop=interaction.client.loop)
        for item in self.children:
            if isinstance(item, discord.ui.Button) and item.label == "✨":
                item.style = discord.ButtonStyle.secondary
        button.style = discord.ButtonStyle.success if state else discord.ButtonStyle.secondary
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="✨", style=discord.ButtonStyle.secondary, row=1)
    async def secret(self, interaction, button):
        state = toggle_secret_mode(interaction.guild_id, vc=self.vc, loop=interaction.client.loop)
        for item in self.children:
            if isinstance(item, discord.ui.Button) and item.label == "♾️":
                item.style = discord.ButtonStyle.secondary
        button.style = discord.ButtonStyle.success if state else discord.ButtonStyle.secondary
        await interaction.response.edit_message(view=self)