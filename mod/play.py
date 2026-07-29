import yt_dlp, asyncio
from music import ui
from music.queue import get_queue, play_next, start_progress_updater, progress_tasks

def setup(tree):
    @tree.command(name="play", description="放你喜歡的歌，星輝醬想跟你一起聽嘛…♪")
    async def play(interaction, query: str):
        if not interaction.user.voice or not interaction.user.voice.channel:
            return await interaction.response.send_message("快點進語音頻道嘛，星輝醬已經在裡面等親愛的很久了捏～", ephemeral=True)
        
        await interaction.response.defer()

        vc = interaction.guild.voice_client or await interaction.user.voice.channel.connect()
        search = query if query.startswith("http") else f"ytsearch5:{query}"

        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'noplaylist': True,
            'ignoreerrors': True,
            'user_agent': 'Mozilla/5.0'
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(search, download=False)
                
                if info and 'entries' in info:
                    entries = [e for e in info['entries'] if e is not None]
                elif info:
                    entries = [info]
                else:
                    entries = []

                if not entries:
                    return await interaction.followup.send("找不到這首歌捏，要不要換個關鍵字試試看？")
                
                song = entries[0]
        except Exception as e:
            print(f"[play 提取失敗]: {e}")
            return await interaction.followup.send("搜尋歌曲時發生錯誤，請稍後再試試看～")

        q = get_queue(interaction.guild_id)

        if vc.is_playing() or vc.is_paused():
            q.append(song)
            await interaction.followup.send(f"排進歌單囉！下一首**{song['title']}**也要跟親愛的繼續聽…♪")
        else:
            q.append(song)
            loop = asyncio.get_running_loop()
            play_next(vc, interaction.guild_id, loop, interaction.channel, is_first_play=True)
            embed = ui.create_music_embed(song, 0.0)
            msg = await interaction.followup.send(embed=embed, view=ui.PlayerView(vc, interaction.guild_id))
            progress_tasks[interaction.guild_id] = asyncio.create_task(start_progress_updater(msg, song, vc))