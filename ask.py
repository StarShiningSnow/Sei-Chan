

def setup(tree):
    @tree.command(name="ask",description="詢問AI")
    async def ask(interaction,question:str):
        await interaction.response.send_message(question)