import asyncio
from music import player,ui

async def check(voice):
    await asyncio.sleep(10)
    if voice.is_connected():
        if len(voice.channel.members) == 1:
            await voice.disconnect()
            print("語音頻道無人，自動離開")

async def update_embed(guild_id):
    if guild_id not in player.player_messages:
        return
    message = player.player_messages[guild_id]
    embed = ui.music_embed(player.current[guild_id],player.queues[guild_id])
    await message.edit(embed=embed)

def setup(tree,client):
    @client.event
    async def on_voice_state_update(member,before,after):
        if member.bot:
            return
        voice = member.guild.voice_client
        if voice and len(voice.channel.members) == 1:
            asyncio.create_task(check(voice))

    @tree.command(name="play",description="讓星輝醬為妳播放音樂！")
    async def play(interaction,query:str):
        await interaction.response.defer()
        try:
            if interaction.user.voice is None:
                await interaction.followup.send("請先加入語音頻道！")
                return

            
            voice_channel = interaction.user.voice.channel
            voice = interaction.guild.voice_client
            if voice is None:
                voice = await voice_channel.connect()
            guild_id = interaction.guild.id
            result = await player.play_music(voice,guild_id,query)

            if result["status"] == "queued":
                await interaction.followup.send(f"已加入播放列表：{result['title']}")
                await update_embed(guild_id)
                return
            
            embed = ui.music_embed(result,player.queues[guild_id])

            message = await interaction.followup.send(embed=embed,view=ui.MusicView(voice,guild_id))
            player.player_messages[guild_id]=message

        except Exception:
            await interaction.followup.send("播放音樂時發生錯誤！")