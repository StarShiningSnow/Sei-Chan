import discord, asyncio, yt_dlp, random, time
from data import secret

queues = {}
loops = {}
history = {}
channels = {}
autoplays = {}
secret_playlists = {}
progress_tasks = {}
idle_tasks = {}
monitor_tasks = {}    

def get_queue(guild_id: int):
    if guild_id not in queues:
        queues[guild_id] = []
    return queues[guild_id]

def get_history(guild_id: int):
    if guild_id not in history:
        history[guild_id] = []
    return history[guild_id]

def is_looping(guild_id: int):
    return loops.get(guild_id, False)

def toggle_loop(guild_id: int):
    loops[guild_id] = not is_looping(guild_id)
    return loops[guild_id]

def is_autoplay(guild_id: int):
    return autoplays.get(guild_id, False)

def toggle_autoplay(guild_id: int, vc=None, loop=None):
    autoplays[guild_id] = not is_autoplay(guild_id)
    if autoplays[guild_id]:
        secret_playlists[guild_id] = False
        if vc and loop and vc.is_connected() and not vc.is_playing() and not vc.is_paused():
            play_next(vc, guild_id, loop)
    return autoplays[guild_id]

def is_secret_mode(guild_id: int):
    return secret_playlists.get(guild_id, False)

def toggle_secret_mode(guild_id: int, vc=None, loop=None):
    secret_playlists[guild_id] = not is_secret_mode(guild_id)
    if secret_playlists[guild_id]:
        autoplays[guild_id] = False
        if vc and loop and vc.is_connected() and not vc.is_playing() and not vc.is_paused():
            play_next(vc, guild_id, loop)
    return secret_playlists[guild_id]

def play_previous(guild_id: int):
    h = get_history(guild_id)
    if not h: return False
    prev_song = h.pop()
    q = get_queue(guild_id)
    q.insert(0, prev_song)
    return True

def get_recent_titles(guild_id: int, limit: int = 10):
    h = get_history(guild_id)
    return [s.get('title') for s in h[-limit:] if s.get('title')]

def get_recent_urls(guild_id: int, limit: int = 10):
    h = get_history(guild_id)
    urls = []
    for s in h[-limit:]:
        u = s.get('webpage_url') or s.get('url') or s.get('id')
        if u: urls.append(u)
    return urls

def fetch_related_song(guild_id: int, song_info: dict):
    title = song_info.get('title', '')
    uploader = song_info.get('uploader', '') or song_info.get('artist', '')
    recent_titles = get_recent_titles(guild_id, limit=10)
    recent_urls = get_recent_urls(guild_id, limit=10)

    search_query = f"{uploader} {title}" if uploader else title
    search = f"ytsearch10:{search_query} mix"

    opts = {
        'format': 'bestaudio/best', 
        'quiet': True, 
        'noplaylist': True, 
        'ignoreerrors': True,
        'user_agent': 'Mozilla/5.0'
    }

    with yt_dlp.YoutubeDL(opts) as ydl:
        try:
            info = ydl.extract_info(search, download=False)
            entries = [e for e in (info.get('entries') if info and 'entries' in info else [info]) if e]
        except Exception as e:
            print(f"[fetch_related_song] 搜尋失敗: {e}")
            return None

        for entry in entries:
            entry_title = entry.get('title')
            entry_url = entry.get('webpage_url') or entry.get('url') or entry.get('id')
            if entry_title in recent_titles or entry_url in recent_urls:
                continue

            return entry

    return None

def fetch_secret_song(guild_id: int):
    opts = {'format': 'bestaudio/best', 'quiet': True, 'extract_flat': 'in_playlist', 'user_agent': 'Mozilla/5.0', 'ignoreerrors': True}
    recent_titles = get_recent_titles(guild_id, limit=10)
    recent_urls = get_recent_urls(guild_id, limit=10)

    with yt_dlp.YoutubeDL(opts) as ydl:
        try:
            info = ydl.extract_info(secret.SECRET_PLAYLIST_URL, download=False)
            entries = info.get('entries', []) if info else []
        except Exception as e:
            print(f"[fetch_secret_song] 提取秘密歌單失敗: {e}")
            return None

        if not entries: return None
        
        unplayed = [
            e for e in entries 
            if e.get('title') not in recent_titles and (e.get('url') or e.get('id')) not in recent_urls
        ]
        pool = unplayed if unplayed else entries
        
        chosen = random.choice(pool)
        detail_opts = {'format': 'bestaudio/best', 'quiet': True, 'user_agent': 'Mozilla/5.0', 'ignoreerrors': True}
        with yt_dlp.YoutubeDL(detail_opts) as ydl_detail:
            song_url = chosen.get('url') or chosen.get('webpage_url') or f"https://www.youtube.com/watch?v={chosen.get('id')}"
            return ydl_detail.extract_info(song_url, download=False)

def refresh_song_url(song: dict):
    url = song.get('webpage_url') or song.get('url')
    if not url:
        return song
    opts = {'format': 'bestaudio/best', 'quiet': True, 'user_agent': 'Mozilla/5.0'}
    with yt_dlp.YoutubeDL(opts) as ydl:
        try:
            fresh_info = ydl.extract_info(url, download=False)
            if fresh_info and 'url' in fresh_info:
                song['url'] = fresh_info['url']
        except Exception as e:
            print(f"[refresh_song_url] 刷新網址失敗: {e}")
    return song

async def start_progress_updater(msg, song, vc):
    from music.ui import create_music_embed
    start_time = time.time()
    accumulated_time = 0.0
    last_update = start_time
    duration = song.get('duration', 0)

    try:
        while vc and (vc.is_playing() or vc.is_paused()):
            await asyncio.sleep(2.5)
            now = time.time()
            if vc.is_playing():
                accumulated_time += (now - last_update)
            last_update = now
            
            embed = create_music_embed(song, accumulated_time)
            await msg.edit(embed=embed)
    except (discord.NotFound, asyncio.CancelledError):
        pass
    finally:
        try:
            if duration > 0:
                embed = create_music_embed(song, duration)
                await msg.edit(embed=embed)
        except Exception:
            pass

async def start_idle_timer(vc, guild_id, timeout_seconds=300):
    try:
        await asyncio.sleep(timeout_seconds)
        if vc and vc.is_connected() and not vc.is_playing() and not vc.is_paused():
            await vc.disconnect()
            ch = channels.get(guild_id)
            if ch:
                await ch.send("歌放完你都不說話…星輝醬先退出來囉，想我的話隨時叫我進去陪你…")
    except asyncio.CancelledError:
        pass

async def start_empty_channel_monitor(vc, guild_id):
    try:
        while vc and vc.is_connected():
            await asyncio.sleep(10)
            if vc.channel:
                human_members = [m for m in vc.channel.members if not m.bot]
                if len(human_members) == 0:
                    await vc.disconnect()
                    ch = channels.get(guild_id)
                    if ch:
                        await ch.send("大家都走光了…連親愛的也不在了？那星輝醬也先退出來囉，等你回來…")
                    break
    except asyncio.CancelledError:
        pass

def play_next(vc, guild_id, loop, channel=None, current_song=None, retry_count=0, is_first_play=False):
    if channel:
        channels[guild_id] = channel

    if guild_id in progress_tasks and not progress_tasks[guild_id].done():
        progress_tasks[guild_id].cancel()

    if guild_id in idle_tasks and not idle_tasks[guild_id].done():
        idle_tasks[guild_id].cancel()

    if guild_id not in monitor_tasks or monitor_tasks[guild_id].done():
        monitor_tasks[guild_id] = asyncio.run_coroutine_threadsafe(start_empty_channel_monitor(vc, guild_id), loop)

    q = get_queue(guild_id)

    if current_song and retry_count == 0:
        get_history(guild_id).append(current_song)

    if is_looping(guild_id) and current_song and retry_count == 0:
        q.insert(0, current_song)

    if not q and not is_looping(guild_id):
        if is_secret_mode(guild_id):
            secret_song = fetch_secret_song(guild_id)
            if secret_song:
                q.append(secret_song)
        elif is_autoplay(guild_id):
            last_song = current_song or (get_history(guild_id)[-1] if get_history(guild_id) else None)
            if last_song:
                related_song = fetch_related_song(guild_id, last_song)
                if related_song:
                    q.append(related_song)

    if not q:
        idle_tasks[guild_id] = asyncio.run_coroutine_threadsafe(start_idle_timer(vc, guild_id, 300), loop)
        return

    song = q.pop(0)
    if current_song and not is_looping(guild_id) and retry_count == 0:
        curr_url = current_song.get('webpage_url') or current_song.get('url')
        song_url = song.get('webpage_url') or song.get('url')
        if curr_url and song_url and curr_url == song_url:
            if q:
                song = q.pop(0)
            else:
                idle_tasks[guild_id] = asyncio.run_coroutine_threadsafe(start_idle_timer(vc, guild_id, 300), loop)
                return

    if retry_count > 0:
        song = refresh_song_url(song)

    opts = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 -probesize 10000000 -analyzeduration 15000000 -user_agent "Mozilla/5.0"',
        'options': '-vn -bufsize 64k'
    }
    
    def after_playing(e):
        if e:
            err_str = str(e)
            if ('403' in err_str or 'Forbidden' in err_str) and retry_count < 2:
                q.insert(0, song)
                loop.call_soon_threadsafe(play_next, vc, guild_id, loop, None, None, retry_count + 1)
                return
        loop.call_soon_threadsafe(play_next, vc, guild_id, loop, None, song)

    try:
        vc.play(discord.FFmpegPCMAudio(song['url'], **opts), after=after_playing)
    except Exception as ex:
        ex_str = str(ex)
        if ('403' in ex_str or 'Forbidden' in ex_str) and retry_count < 2:
            q.insert(0, song)
            play_next(vc, guild_id, loop, None, None, retry_count + 1)
            return
        return

    ch = channels.get(guild_id)
    if ch and not is_first_play:
        from music.ui import PlayerView, create_music_embed
        
        async def send_and_track():
            embed = create_music_embed(song, 0.0)
            msg = await ch.send(embed=embed, view=PlayerView(vc, guild_id))
            progress_tasks[guild_id] = asyncio.create_task(start_progress_updater(msg, song, vc))

        asyncio.run_coroutine_threadsafe(send_and_track(), loop)

async def async_play_next(vc, guild_id, loop, current_song=None):
    play_next(vc, guild_id, loop, None, current_song)