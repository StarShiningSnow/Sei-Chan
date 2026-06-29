def setup(tree):
    @tree.command(name="intro",description="自我介紹")
    async def intro(interaction):
        await interaction.response.send_message("測試")