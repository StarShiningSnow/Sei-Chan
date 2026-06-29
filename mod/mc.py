def setup(tree):
    @tree.command(name="mc",description="查詢伺服器")
    async def mc(interaction):
        await interaction.response.send_message("測試")