def setup(tree):
    @tree.command(name="map",description="檢視地圖")
    async def map(interaction):
        await interaction.response.send_message("測試")