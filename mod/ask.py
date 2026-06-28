from ai import ai_main,mode

def setup(tree):
    @tree.command(name="ask",description="詢問AI")
    async def ask(interaction,question:str):
        await interaction.response.defer()

        reply = await ai_main.chat(
            user_id=interaction.user.id,
            username=interaction.user.display_name,
            message=question,
            mode=mode.AIMode.ASK,
        )

        await interaction.followup.send(reply)