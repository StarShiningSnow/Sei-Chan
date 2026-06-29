from ai import ai_main,mode

def setup(tree):
    @tree.command(name="ask",description="直接和星輝醬對話吧！")
    async def ask(interaction,question:str):
        await interaction.response.defer()

        reply = await ai_main.chat(
            user_id=interaction.user.id,
            message=question,
            mode=mode.AIMode.ASK,
        )

        await interaction.followup.send(reply)