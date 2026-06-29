def setup(tree):
    @tree.command(name="ver",description="查詢版本")
    async def ver(interaction):
        await interaction.response.send_message("測試")