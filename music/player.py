import yt_dlp,discord

queues = {}
current = {}
history = {}
player_messages = {}

ydl_opts = {"format": "bestaudio/best","quiet": True, "noplaylist": True}

ffmpeg_opts = {
    "before_options":
        "-reconnect 1 " 
        "-reconnect_streamed 1 " "-reconnect_delay_max 5",
    "options":
        "-vn"}

def get_audio(query):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl: # type: ignore
        info = ydl.extract_info(query,download=False)
    return info

def play_next(voice,guild_id):
    if guild_id not in queues:
        return
    if len(queues[guild_id]) == 0:
        return
    song = queues[guild_id].pop(0)
    if guild_id not in history:
        history[guild_id] = []

    if guild_id in current:
        history[guild_id].append(
        current[guild_id]
    )
    current[guild_id] = song
   
    try:
        info = get_audio(song["query"])
        audio_url = info.get("url")
        if audio_url is None:
            play_next(voice,guild_id)
            return
        source = discord.FFmpegPCMAudio(audio_url,**ffmpeg_opts) # type: ignore
        voice.play(source,after=lambda e: play_next(voice,guild_id))
    except Exception as e:
        print(f"播放下一首失敗：{e}")
        play_next(voice,guild_id)

async def play_music(voice,guild_id,query):
    if guild_id not in queues:
        queues[guild_id]=[]
    info = get_audio(query)
    title = info.get("title","未知歌曲")
    if voice.is_playing():
        queues[guild_id].append({"query": query,"title": title})
        return {"status": "queued", "title": title}

    audio_url = info.get("url")
    current[guild_id]={"title":title}
    source = discord.FFmpegPCMAudio(audio_url,**ffmpeg_opts) # type: ignore
    voice.play(source,after=lambda e: play_next(voice,guild_id))
    return {"status": "playing","title": title,"thumbnail":info.get("thumbnail")}

def get_queue(guild_id):
    return queues.get(guild_id,[])

def pause_music(voice):
    if voice.is_playing():
        voice.pause()
        return True
    return False

def resume_music(voice):
    if voice.is_paused():
        voice.resume()
        return True
    return False

def skip_music(voice, guild_id):
    if voice.is_playing():
        voice.stop()

    play_next(voice, guild_id)

def previous_music(voice, guild_id):

    if guild_id not in history:
        return False

    if len(history[guild_id]) == 0:
        return False

    song = history[guild_id].pop()

    if voice.is_playing():
        voice.stop()

    queues[guild_id].insert(
        0,
        current[guild_id]
    )

    queues[guild_id].insert(
        0,
        song
    )

    return True
